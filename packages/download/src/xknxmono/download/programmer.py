"""Low level device programming operations over a point-to-point connection.

The :class:`DeviceProgrammer` turns the primitive application layer services
provided by ``xknx`` into the operations a Load Procedure needs: chunked memory
writes, property writes, and driving a Load State Machine with read-back
verification. Those services are defined in KNX Standard v3.0.0, Chapter 3/3/7
"Application Layer": A_Memory_Read (section 3.5.3), A_Memory_Write (section 3.5.4),
A_PropertyValue_Read/A_PropertyValue_Write, and A_DeviceDescriptor_Read
(section 3.4.2.1). Memory reads/writes are split to the connection's maximum APDU
length.

It talks to any object implementing :class:`BusConnection`; at runtime this is
``xknx.management.P2PConnection``, in tests it is a fake.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Protocol

from xknx.telegram.apci import (
    DeviceDescriptorRead,
    DeviceDescriptorResponse,
    FunctionPropertyCommand,
    FunctionPropertyStateRead,
    FunctionPropertyStateResponse,
    MemoryRead,
    MemoryResponse,
    MemoryWrite,
    PropertyValueRead,
    PropertyValueResponse,
    PropertyValueWrite,
    Restart,
    RestartMasterReset,
    RestartMasterResetResponse,
    UserMemoryRead,
    UserMemoryResponse,
    UserMemoryWrite,
)

from . import load_state
from .errors import DownloadError, LoadStateError, VerificationError

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from xknx.telegram import Telegram
    from xknx.telegram.apci import APCI

# Octets consumed by TPCI/APCI/count/address in a standard A_Memory_Write ASDU.
_MEMORY_OVERHEAD = 3
# A_Memory_Write encodes the byte count in 6 bits.
_MAX_MEMORY_CHUNK = 0x3F
# Octets consumed by APCI/object/property/count/index in A_PropertyValue_Write.
_PROPERTY_OVERHEAD = 5
# A_PropertyValue_Write encodes the element count in 4 bits.
_MAX_PROPERTY_ELEMENTS = 0xF
# Default APDU length every KNX device has to support.
DEFAULT_MAX_APDU_LENGTH = 15
# Upper bound used when negotiating the APDU length up from the default.
MAX_NEGOTIATED_APDU_LENGTH = 254
# Device Object property carrying the device's maximum APDU length (2 octets).
PID_MAX_APDU_LENGTH = 56
# Property id carrying an interface object's type (PID_OBJECT_TYPE).
PID_OBJECT_TYPE = 1
# Property id carrying a loadable part's table base address (PID_TABLE_REFERENCE).
PID_TABLE_REFERENCE = 7
# Highest interface object index scanned when locating an object by type.
_MAX_OBJECT_INDEX = 255
# A_Memory_Read/Write carry a 16-bit address, so they only reach the first 64
# KiB; at and above this boundary A_UserMemory_Read/Write (3-byte address) are
# used. ETS splits a transfer straddling the boundary into a Standard part below
# and a UserMemory part at/above it (Hawk eo.cs, e.g. the 65536 split around
# lines 16704-16707 and 16647). See KNX 3/5/1 4.2 and 3/3/7 3.5.
_USER_MEMORY_BOUNDARY = 0x10000


class BusConnection(Protocol):
    """Subset of ``xknx.management.P2PConnection`` used for programming."""

    async def send_data(self, payload: APCI, wait_for_ack: bool = True) -> None:
        """Send a payload and, by default, wait for the transport layer ACK."""
        ...

    async def request(self, payload: APCI, expected: type[APCI] | None) -> Telegram:
        """Send a payload and wait for the device's response telegram."""
        ...


class ConnectionManager(Protocol):
    """Opens and closes point-to-point connections for a Load Procedure.

    A Load Procedure opens the connection on a Connect control and closes it on
    a Disconnect (and after a Restart). Implementations map ``open`` to a fresh
    T_Connect and ``close`` to T_Disconnect.
    """

    async def open(self) -> BusConnection:
        """Open a connection to the device and return it."""
        ...

    async def close(self) -> None:
        """Close the currently open connection, if any."""
        ...


class DeviceProgrammer:
    """Perform programming operations over an open point-to-point connection."""

    def __init__(
        self,
        connection: BusConnection,
        *,
        max_apdu_length: int = DEFAULT_MAX_APDU_LENGTH,
        apdu_overhead: int = 0,
    ) -> None:
        """Initialize with a connected bus connection and the negotiated APDU length.

        ``apdu_overhead`` is the number of octets a lower layer adds around each
        APDU on the wire (13 for a KNX Data Secure session, 0 otherwise). It is
        subtracted from ``max_apdu_length`` when sizing chunks so the fully
        encoded frame still fits the device's APDU length.
        """
        self.connection = connection
        self.max_apdu_length = max_apdu_length
        self.apdu_overhead = apdu_overhead
        self._object_index_cache: dict[tuple[int, int], int] = {}
        # Some devices cap an A_Memory_Read reply below the negotiated APDU. Once a
        # short reply reveals that cap, later reads request no more than it, so a
        # read never stalls re-asking oversized blocks.
        self._memory_read_cap: int | None = None

    @property
    def _plain_apdu_length(self) -> int:
        """Usable plaintext APDU length after the wire overhead (at least 1)."""
        return max(1, self.max_apdu_length - self.apdu_overhead)

    @property
    def memory_chunk_size(self) -> int:
        """Largest memory payload that fits into a single telegram (at least 1)."""
        return max(
            1, min(self._plain_apdu_length - _MEMORY_OVERHEAD, _MAX_MEMORY_CHUNK)
        )

    async def read_device_descriptor(self) -> int:
        """Read device descriptor type 0 (the mask version)."""
        telegram = await self.connection.request(
            DeviceDescriptorRead(descriptor=0), DeviceDescriptorResponse
        )
        payload = telegram.payload
        if not isinstance(payload, DeviceDescriptorResponse):
            raise VerificationError("no device descriptor response received")
        return payload.value

    async def read_max_apdu_length(self) -> int:
        """Read the device's maximum APDU length from the Device Object.

        PID_MAX_APDU_LENGTH (property 56 of the Device Object, interface object
        index 0) holds the largest APDU the device accepts, in octets. Falls back
        to the mandatory default when the device does not expose it.
        """
        data = await self.read_property(0, PID_MAX_APDU_LENGTH)
        if not data:
            return DEFAULT_MAX_APDU_LENGTH
        return int.from_bytes(data, "big")

    def _block_count(self, address: int, remaining: int) -> int:
        """Octets to transfer next: the APDU chunk, clamped to the 64 KiB boundary.

        A single A_Memory_/A_UserMemory_ transfer must not straddle the 64 KiB
        boundary (the address space and APCI change there), so a block that would
        cross it is cut at the boundary (Hawk eo.cs splits the same way).
        """
        count = min(self.memory_chunk_size, remaining)
        if address < _USER_MEMORY_BOUNDARY < address + count:
            count = _USER_MEMORY_BOUNDARY - address
        return count

    async def read_memory(self, address: int, size: int) -> bytes:
        """Read ``size`` octets starting at ``address``, chunked to the APDU length.

        Tolerant of a device that answers an A_Memory_Read with fewer octets than
        requested (some cap the reply below the negotiated APDU): the returned
        octets are valid, so the read advances by however many came back and asks
        for the rest, remembering the cap so it does not keep over-asking. Only a
        completely empty reply (no progress) is an error.
        """
        result = bytearray()
        offset = 0
        logger.debug("read_memory: addr=%#06x size=%d", address, size)
        while offset < size:
            block_address = address + offset
            count = self._block_count(block_address, size - offset)
            if self._memory_read_cap is not None:
                count = min(count, self._memory_read_cap)
            data = await self._read_block(block_address, count)
            if not data:
                # Some devices (observed on BIM M112 / mask 0701) answer certain A_Memory_Read
                # counts with a zero-length reply while serving smaller counts fine. Back the block
                # size off and retry rather than aborting the whole read; only a genuine
                # no-response at the minimum count is fatal.
                while not data and count > 1:
                    count = max(1, count // 2)
                    self._memory_read_cap = count
                    data = await self._read_block(block_address, count)
                if not data:
                    raise VerificationError(
                        f"no memory response for address {block_address:#06x}"
                    )
            if len(data) < count:
                self._memory_read_cap = len(data)
            result.extend(data)
            offset += len(data)
        return bytes(result)

    async def _read_block(self, address: int, count: int) -> bytes:
        """Read one block via A_Memory_Read or A_UserMemory_Read by address.

        Returns the response octets, which may be fewer than ``count`` (a valid
        short reply); the caller handles that. Only more octets than requested is
        a protocol violation.
        """
        if address >= _USER_MEMORY_BOUNDARY:
            request: APCI = UserMemoryRead(address=address, count=count)
            expected: type[APCI] = UserMemoryResponse
        else:
            request = MemoryRead(address=address, count=count)
            expected = MemoryResponse
        telegram = await self.connection.request(request, expected)
        payload = telegram.payload
        if not isinstance(payload, MemoryResponse | UserMemoryResponse):
            raise VerificationError(f"no memory response for address {address:#06x}")
        if len(payload.data) > count:
            raise VerificationError(
                f"over-long memory response at {address:#06x}: "
                f"asked {count} got {len(payload.data)}"
            )
        return payload.data

    async def write_memory(
        self, address: int, data: bytes, *, verify: bool = False
    ) -> None:
        """Write ``data`` starting at ``address``, chunked to the APDU length.

        With ``verify`` each block is read back and compared right after it is
        written (per KNX 3/5/2), so a lost EEPROM write is caught immediately.
        """
        offset = 0
        logger.debug(
            "write_memory: addr=%#06x len=%d verify=%s", address, len(data), verify
        )
        while offset < len(data):
            block_address = address + offset
            count = self._block_count(block_address, len(data) - offset)
            block = data[offset : offset + count]
            await self._write_block(block_address, block)
            if verify:
                read_back = await self.read_memory(block_address, len(block))
                if read_back != block:
                    raise VerificationError(
                        f"memory verification failed at {block_address:#06x}: "
                        f"wrote {block.hex()} read {read_back.hex()}"
                    )
            offset += count

    async def _write_block(self, address: int, block: bytes) -> None:
        """Write one block via A_Memory_Write or A_UserMemory_Write by address."""
        if address >= _USER_MEMORY_BOUNDARY:
            await self.connection.send_data(
                UserMemoryWrite(address=address, data=block)
            )
        else:
            await self.connection.send_data(MemoryWrite(address=address, data=block))

    async def read_property(
        self,
        object_index: int,
        property_id: int,
        *,
        count: int = 1,
        start_index: int = 1,
    ) -> bytes:
        """Read a property value from an interface object."""
        telegram = await self.connection.request(
            PropertyValueRead(
                object_index=object_index,
                property_id=property_id,
                count=count,
                start_index=start_index,
            ),
            PropertyValueResponse,
        )
        response = _validate_property_response(
            telegram.payload, object_index, property_id, "read"
        )
        return response.data

    async def write_property(
        self,
        object_index: int,
        property_id: int,
        data: bytes,
        *,
        count: int = 1,
        start_index: int = 1,
    ) -> bytes:
        """Write a property value and return the resulting value.

        A_PropertyValue_Write is confirmed by A_PropertyValue_Response carrying
        the resulting value, so this waits for that response (via ``request``)
        rather than only the transport ACK - otherwise the buffered response
        would be mistaken for the answer to the next request.

        The element count is encoded in four bits and the data must fit the APDU,
        so a value spanning more than 15 elements or one frame is written in
        successive element ranges; the last response is returned.
        """
        if count <= 0:
            raise VerificationError(
                f"property write for object {object_index} property {property_id} "
                "has a non-positive element count (an unresolved wildcard count is "
                "not supported)"
            )
        if count > 1 and len(data) % count:
            raise VerificationError(
                f"property data ({len(data)} octets) is not divisible by the "
                f"element count {count} for object {object_index} property {property_id}"
            )
        element_size = (len(data) // count) if count > 1 else len(data)
        max_bytes = max(1, self._plain_apdu_length - _PROPERTY_OVERHEAD)
        if element_size > max_bytes:
            raise VerificationError(
                f"a single property element ({element_size} octets) does not fit "
                f"the APDU ({max_bytes} octets) for object {object_index} "
                f"property {property_id}; element fragmentation is not implemented"
            )
        if element_size:
            per_frame = max(1, min(_MAX_PROPERTY_ELEMENTS, max_bytes // element_size))
        else:
            per_frame = _MAX_PROPERTY_ELEMENTS

        result = b""
        element = 0
        while element < count:
            frame_count = min(per_frame, count - element)
            frame_data = (
                data[element * element_size : (element + frame_count) * element_size]
                if element_size
                else data
            )
            result = await self._write_property_frame(
                object_index,
                property_id,
                frame_data,
                frame_count,
                start_index + element,
            )
            element += frame_count
        return result

    async def _write_property_frame(
        self,
        object_index: int,
        property_id: int,
        data: bytes,
        count: int,
        start_index: int,
    ) -> bytes:
        """Send a single A_PropertyValue_Write and return the resulting value."""
        telegram = await self.connection.request(
            PropertyValueWrite(
                object_index=object_index,
                property_id=property_id,
                count=count,
                start_index=start_index,
                data=data,
            ),
            PropertyValueResponse,
        )
        response = _validate_property_response(
            telegram.payload, object_index, property_id, "write", require_nonzero=True
        )
        return response.data

    async def invoke_function_property(
        self, object_index: int, property_id: int, data: bytes
    ) -> bytes:
        """Call a Function Property and return the resulting state.

        A_FunctionPropertyCommand invokes a use-case specific function on an
        interface object and is confirmed by A_FunctionPropertyState_Response
        carrying a return code and the resulting state (KNX Standard v3.0.0,
        3/3/7 section 3.4.7.1). A non-zero return code means the device rejected
        the command.
        """
        telegram = await self.connection.request(
            FunctionPropertyCommand(
                object_index=object_index, property_id=property_id, data=data
            ),
            FunctionPropertyStateResponse,
        )
        return self._function_property_result(telegram, object_index, property_id)

    async def read_function_property(
        self, object_index: int, property_id: int
    ) -> bytes:
        """Read a Function Property state and return it.

        A_FunctionPropertyState_Read reads the state of a function property and is
        answered by A_FunctionPropertyState_Response (KNX Standard v3.0.0, 3/3/7
        section 3.4.7.2).
        """
        telegram = await self.connection.request(
            FunctionPropertyStateRead(
                object_index=object_index, property_id=property_id
            ),
            FunctionPropertyStateResponse,
        )
        return self._function_property_result(telegram, object_index, property_id)

    @staticmethod
    def _function_property_result(
        telegram: Telegram, object_index: int, property_id: int
    ) -> bytes:
        """Validate a Function Property response and return its state data."""
        payload = telegram.payload
        if not isinstance(payload, FunctionPropertyStateResponse):
            raise VerificationError(
                f"no function property response for object {object_index} "
                f"property {property_id}"
            )
        if payload.return_code != 0:
            raise LoadStateError(
                f"function property {property_id} on object {object_index} "
                f"returned error code {payload.return_code:#04x}"
            )
        return payload.data

    async def read_table_reference(self, object_index: int) -> int:
        """Read a loadable part's table base address (PID_TABLE_REFERENCE).

        The reference width depends on the realisation type - 2 octets for the
        memory-mapped BCU/System 7 families, 4 octets (PDT_GENERIC_04, KNX 3/5/1
        4.2.7) for System B - so the raw value is taken as-is rather than fixed
        to one width. A zero reference means the segment has not been allocated
        (or allocation failed) and must not be used as a write target (KNX 3/5/3
        3.5.1.4).
        """
        data = await self.read_property(object_index, PID_TABLE_REFERENCE)
        if not data:
            raise VerificationError(f"empty table reference for object {object_index}")
        reference = int.from_bytes(data, "big")
        if reference == 0:
            raise LoadStateError(
                f"object {object_index} reports a zero table reference "
                "(segment not allocated)"
            )
        logger.debug(
            "read_table_reference: object=%d base=%#06x", object_index, reference
        )
        return reference

    async def locate_object(self, object_type: int, occurrence: int = 0) -> int:
        """Resolve the object index of the ``occurrence``-th object of a type.

        ``occurrence`` is zero-based, matching the product application program XML (``Occurrence="0"``
        is the first instance). Scans interface objects reading ``PID_OBJECT_TYPE``
        until the requested occurrence is found. Cached per programmer instance.
        """
        cached = self._object_index_cache.get((object_type, occurrence))
        if cached is not None:
            return cached
        ordinal = 0
        for index in range(_MAX_OBJECT_INDEX + 1):
            try:
                data = await self.read_property(index, PID_OBJECT_TYPE)
            except (VerificationError, DownloadError):
                break
            if len(data) < 2:
                break
            found_type = int.from_bytes(data[:2], "big")
            if found_type == object_type:
                if ordinal == occurrence:
                    self._object_index_cache[(object_type, occurrence)] = index
                    return index
                ordinal += 1
        raise LoadStateError(
            f"interface object type {object_type} occurrence {occurrence} not found"
        )

    async def read_load_state(self, object_index: int) -> load_state.LoadState:
        """Read the current state of an object's Load State Machine."""
        data = await self.read_property(object_index, load_state.PID_LOAD_STATE_CONTROL)
        if not data:
            raise LoadStateError(f"empty load state for object {object_index}")
        return _decode_load_state(data[0], object_index)

    async def send_load_event(
        self,
        object_index: int,
        event: bytes,
        expected: load_state.LoadState,
        *,
        retries: int = 30,
        retry_delay: float = 1.0,
    ) -> None:
        """Write a load event and verify the machine reaches ``expected``.

        ``LOAD_COMPLETE`` triggers a checksum calculation that can take a while,
        and a device may report a transient ``UNLOADING``/``LOAD_COMPLETING``
        state first, so the state is polled up to ``retries`` times.
        """
        resulting = await self.write_property(
            object_index, load_state.PID_LOAD_STATE_CONTROL, event
        )
        state = (
            _decode_load_state(resulting[0], object_index)
            if resulting
            else await self.read_load_state(object_index)
        )
        logger.debug(
            "send_load_event: object=%d target=%s initial=%s",
            object_index,
            expected.name,
            state.name,
        )
        for _ in range(max(retries, 0)):
            if state == expected:
                return
            if state == load_state.LoadState.ERROR:
                raise LoadStateError(
                    f"object {object_index} entered ERROR state "
                    f"(expected {expected.name})"
                )
            await asyncio.sleep(retry_delay)
            state = await self.read_load_state(object_index)
        if state != expected:
            raise LoadStateError(
                f"object {object_index} did not reach {expected.name}, "
                f"last state {state.name}"
            )

    async def restart(self) -> None:
        """Restart the device (also closes the transport connection).

        Sent without waiting for a transport ACK on purpose: a Basic Restart has
        no application-layer response and the device tears the connection down
        immediately, so it often restarts before (or instead of) ACKing. Waiting
        for the ACK would usually time out and just delay the teardown the caller
        already performs. The connection-oriented confirmation the standard
        mentions (3/3/7 3.4.2.2) is therefore not relied upon here; a Master
        Reset, which *is* application-layer confirmed, uses the response path.
        """
        logger.debug("restart: sending Basic Restart (no ACK)")
        await self.connection.send_data(Restart(), wait_for_ack=False)

    async def master_reset(self, erase_code: int, channel_number: int) -> int:
        """Perform a Master Reset and return the device's process time in seconds.

        A Master Reset is an A_Restart with restart_type = 1, carrying an erase
        code and channel number (KNX Standard v3.0.0, 3/3/7 section 3.4.2.2; the
        erase codes are defined with DM_Restart in 3/5/2). Unlike a Basic Restart
        it is confirmed at the application layer by A_Restart_Master_Reset_Response
        with an error code and the process time the device needs before it is
        reachable again. A non-zero error code means the device refused the reset.
        The device restarts afterwards, tearing down the connection.
        """
        telegram = await self.connection.request(
            RestartMasterReset(erase_code=erase_code, channel_number=channel_number),
            RestartMasterResetResponse,
        )
        logger.debug(
            "master_reset: erase_code=%d channel=%d", erase_code, channel_number
        )
        payload = telegram.payload
        if not isinstance(payload, RestartMasterResetResponse):
            raise LoadStateError("no master reset response received")
        if payload.error_code != 0:
            raise LoadStateError(
                f"device refused master reset (erase code {erase_code}, channel "
                f"{channel_number}): error code {payload.error_code:#04x}"
            )
        return payload.process_time


def _validate_property_response(
    payload: APCI | None,
    object_index: int,
    property_id: int,
    operation: str,
    *,
    require_nonzero: bool = False,
) -> PropertyValueResponse:
    """Return the response, or raise if it is missing or mismatched.

    A response echoes the addressed object and property; a differing echo means a
    stale/buffered telegram was mistaken for the answer. With ``require_nonzero``
    a count (nr_of_elem) of 0 is treated as the device rejecting the access (KNX
    3/3/7 3.4.4.1/3.4.4.2). Reads leave it off: a 0-element/empty response is how
    a device reports an absent property, which callers such as object location and
    APDU-length negotiation handle by falling back rather than failing.
    """
    if not isinstance(payload, PropertyValueResponse):
        raise VerificationError(
            f"no property {operation} response for object {object_index} "
            f"property {property_id}, got {payload!r}"
        )
    if payload.object_index != object_index or payload.property_id != property_id:
        raise VerificationError(
            f"property {operation} response addresses object "
            f"{payload.object_index} property {payload.property_id}, "
            f"expected object {object_index} property {property_id}"
        )
    if require_nonzero and payload.count == 0:
        raise VerificationError(
            f"device rejected property {operation}: object {object_index} "
            f"property {property_id} returned 0 elements"
        )
    return payload


def _decode_load_state(value: int, object_index: int) -> load_state.LoadState:
    """Map a raw load state octet to :class:`LoadState`, erroring on unknowns."""
    try:
        return load_state.LoadState(value)
    except ValueError as exc:
        raise LoadStateError(
            f"object {object_index} reported unknown load state {value:#04x}"
        ) from exc
