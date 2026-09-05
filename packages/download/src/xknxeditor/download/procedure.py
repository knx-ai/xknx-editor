"""Interpret a Load Procedure and execute it over a device connection.

A Load Procedure is an ordered list of Load Controls parsed from the application
program (Load Controls are described in KNX Standard v3.0.0, Volume 2 Cookbook,
02_03_01 "Load Controls"). :class:`LoadProcedureRunner` walks that list and turns
each control into the corresponding bus operation, reading bulk data from the
:class:`DownloadImage` where a control refers to it. The download procedures
themselves - complete download, partial download and unload - follow Chapter 3/5/3
"Configuration Procedures", sections 3.5.2, 3.5.3 and 3.5.4.

Load State Machine control follows the property based Realisation Type 1 (writing
load events to ``PID_LOAD_STATE_CONTROL`` of the addressed interface object, see
Chapter 3/5/1 "Resources", section 4.23); the memory mapped variant used by very
old (BCU) device models is out of scope.

Connection handling follows the point-to-point management connection lifecycle: the transport connection is
opened on a Connect control and closed on Disconnect; a Restart tears it down
(after a cooldown the next control reconnects); and any bus control encountered
without an open connection opens one first (auto-connect). This lifecycle is only
active when the runner is given a :class:`ConnectionManager`; with a fixed
programmer the connection is assumed to stay open (Connect/Disconnect are no-ops).
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from xknxeditor.namespaces.intermediate.ld_ctrl_abs_segment_t import LdCtrlAbsSegment
from xknxeditor.namespaces.intermediate.ld_ctrl_clear_lcfilter_table_t import (
    LdCtrlClearLcfilterTable,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_compare_base_t import LdCtrlCompareBase
from xknxeditor.namespaces.intermediate.ld_ctrl_compare_mem_t import LdCtrlCompareMem
from xknxeditor.namespaces.intermediate.ld_ctrl_compare_prop_t import LdCtrlCompareProp
from xknxeditor.namespaces.intermediate.ld_ctrl_compare_rel_mem_t import (
    LdCtrlCompareRelMem,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_connect_t import LdCtrlConnect
from xknxeditor.namespaces.intermediate.ld_ctrl_delay_t import LdCtrlDelay
from xknxeditor.namespaces.intermediate.ld_ctrl_disconnect_t import LdCtrlDisconnect
from xknxeditor.namespaces.intermediate.ld_ctrl_invoke_function_prop_t import (
    LdCtrlInvokeFunctionProp,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_load_completed_t import (
    LdCtrlLoadCompleted,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_load_image_mem_t import (
    LdCtrlLoadImageMem,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_load_image_prop_t import (
    LdCtrlLoadImageProp,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_load_image_rel_mem_t import (
    LdCtrlLoadImageRelMem,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_load_t import LdCtrlLoad
from xknxeditor.namespaces.intermediate.ld_ctrl_master_reset_t import LdCtrlMasterReset
from xknxeditor.namespaces.intermediate.ld_ctrl_mem_addr_space_t import (
    LdCtrlMemAddrSpace,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_read_function_prop_t import (
    LdCtrlReadFunctionProp,
)
from xknxeditor.namespaces.intermediate.ld_ctrl_rel_segment_t import LdCtrlRelSegment
from xknxeditor.namespaces.intermediate.ld_ctrl_restart_t import LdCtrlRestart
from xknxeditor.namespaces.intermediate.ld_ctrl_task_ctrl1_t import LdCtrlTaskCtrl1
from xknxeditor.namespaces.intermediate.ld_ctrl_task_ctrl2_t import LdCtrlTaskCtrl2
from xknxeditor.namespaces.intermediate.ld_ctrl_task_ptr_t import LdCtrlTaskPtr
from xknxeditor.namespaces.intermediate.ld_ctrl_task_segment_t import LdCtrlTaskSegment
from xknxeditor.namespaces.intermediate.ld_ctrl_unload_t import LdCtrlUnload
from xknxeditor.namespaces.intermediate.ld_ctrl_write_mem_t import LdCtrlWriteMem
from xknxeditor.namespaces.intermediate.ld_ctrl_write_prop_t import LdCtrlWriteProp
from xknxeditor.namespaces.intermediate.ld_ctrl_write_rel_mem_t import LdCtrlWriteRelMem

from . import gaps, load_state
from .crc import segment_crc
from .errors import (
    DownloadError,
    ImageError,
    UnsupportedProcedureError,
    VerificationError,
)
from .merge import resolve_download_controls
from .preflight import PreflightReport, PropertyDiff, SegmentDiff
from .programmer import DEFAULT_MAX_APDU_LENGTH, DeviceProgrammer
from .scope import DownloadScope, control_in_scope

if TYPE_CHECKING:
    from xknxeditor.prod import Application

    from .image import DownloadImage
    from .programmer import ConnectionManager

logger = logging.getLogger(__name__)

# Default cooldown (seconds) to wait after a Restart before reconnecting.
DEFAULT_RESTART_COOLDOWN = 3.0

# Memory Control Block table property and its per-segment entry layout (KNX
# Standard v3.0.0, Chapter 3/5/1 "Resources", section 4.2.27 "PID_MCB_TABLE"):
# an 8 octet entry per segment, CRC-protected when bit 0 of octet 4 is clear, with
# the segment CRC in octets 6..7 (big-endian).
_PID_MCB_TABLE = 27
_MCB_ENTRY_SIZE = 8

# The Router interface object (a line/backbone coupler): its relative memory holds the group-address
# filter table (System B), carried as the image's dedicated filter-table field.
_ROUTER_OBJECT_TYPE = 6


def _bytes_match(
    read_back: bytes, expected: bytes, mask: bytes | None, length: int
) -> bool:
    """Whether the first ``length`` octets of ``read_back`` equal ``expected``.

    With a ``mask`` only the set bits of each octet have to match (KNX Standard v3.0.0, 3/5/1
    Compare controls); without a mask it is a plain equality over ``length``."""
    if mask:
        return all(
            read_back[i] & mask[i] == expected[i] & mask[i] for i in range(length)
        )
    return read_back[:length] == expected[:length]


def _unsupported_compare_reason(control: object) -> str | None:
    """A reason string if a Compare control uses a semantic this engine does not implement, else None.

    Plain (optionally masked) equality compares are executed. The Invert, Range and
    RetryInterval/TimeOut semantics (KNX Standard v3.0.0, 3/5/1 Compare controls) are NOT, so a
    control that sets any of them is rejected up front rather than silently verified with the wrong
    result (Invert would invert the outcome; Range/Retry change what "match" means)."""
    if not isinstance(control, LdCtrlCompareBase):
        return None
    unsupported: list[str] = []
    if control.invert:
        unsupported.append("Invert (compare passes on inequality)")
    if control.range is not None:
        unsupported.append("Range (value-in-interval compare)")
    if control.retry_interval or control.time_out:
        unsupported.append("RetryInterval/TimeOut (poll until the state is reached)")
    if not unsupported:
        return None
    return (
        f"compare control {type(control).__name__!r} uses "
        + ", ".join(unsupported)
        + "; only plain (optionally masked) equality compares are implemented, so this would "
        "verify with the wrong result and is not executed"
    )


_MCB_CRC_PROTECTED_OCTET = 4
_MCB_CRC_OFFSET = 6


def _mcb_table_with_crc(data: bytes, segment: bytes) -> bytes:
    """Patch the segment CRC into each CRC-protected Memory Control Block entry.

    ``data`` is the MCB table value (8 octet entries, plus any trailing padding);
    ``segment`` is the loaded object segment the CRCs protect. Each entry declares
    its own sub-segment size in octets 0..3 and carries the CRC (octets 6..7) over
    just that sub-segment; the sub-segments tile the object data in order, so a
    device with several segments in one object gets one CRC per segment rather
    than one CRC over everything (KNX 3/5/1 4.2.27; matches Hawk gd.cs SegmentCRCs,
    which reads the size via gy.c at 8*n and advances the offset cumulatively).
    The size is a 32-bit value stored as two 16-bit big-endian halves, low half
    first (gy.c order). Only entries whose CRC-protected flag (bit 0 of octet 4)
    is clear get their CRC octets filled.

    If the declared sizes do not tile the segment exactly, fall back to a single
    CRC over the whole segment - the behaviour validated byte-perfect on real
    single-segment devices (e.g. System B 1.1.41), so an unexpected size encoding
    can never regress it.
    """
    out = bytearray(data)
    starts = list(range(0, len(out) - _MCB_ENTRY_SIZE + 1, _MCB_ENTRY_SIZE))
    sizes = [
        int.from_bytes(out[s : s + 2], "big")
        | (int.from_bytes(out[s + 2 : s + 4], "big") << 16)
        for s in starts
    ]
    per_entry = bool(sizes) and sum(sizes) == len(segment)
    offset = 0
    for start, size in zip(starts, sizes, strict=True):
        sub_segment = segment[offset : offset + size] if per_entry else segment
        offset += size
        if out[start + _MCB_CRC_PROTECTED_OCTET] & 1:
            continue
        crc = segment_crc(sub_segment)
        out[start + _MCB_CRC_OFFSET] = (crc >> 8) & 0xFF
        out[start + _MCB_CRC_OFFSET + 1] = crc & 0xFF
    return bytes(out)


# Load Controls handled entirely on the client side, without any bus effect.
# LdCtrlDeclarePropDesc only declares a property's description (type, element
# count, access) to the client object model so later property writes know its
# layout; it sends no telegram (A_PropertyValue_Write already carries count and
# data here), so it is a no-op for this engine.
_CLIENT_SIDE = (
    "LdCtrlMaxLength",
    "LdCtrlSetControlVariable",
    "LdCtrlMapError",
    "LdCtrlProgressText",
    "LdCtrlClearCachedObjectTypes",
    "LdCtrlDeclarePropDesc",
)

# Load Controls this engine executes on the bus (the isinstance branches of
# :meth:`LoadProcedureRunner._execute`). Used to pre-validate a resolved,
# scoped procedure before touching the device, so an unsupported control is
# reported up front instead of after earlier controls have already unloaded or
# written the device (a real master procedure can contain e.g.
# ``LdCtrlClearLCFilterTable``, which is not implemented).
_SUPPORTED_CONTROLS = frozenset(
    {
        "LdCtrlConnect",
        "LdCtrlDisconnect",
        "LdCtrlDelay",
        "LdCtrlRestart",
        "LdCtrlMasterReset",
        "LdCtrlUnload",
        "LdCtrlLoad",
        "LdCtrlLoadCompleted",
        "LdCtrlWriteMem",
        "LdCtrlLoadImageMem",
        "LdCtrlCompareMem",
        "LdCtrlWriteRelMem",
        "LdCtrlCompareRelMem",
        "LdCtrlLoadImageRelMem",
        "LdCtrlWriteProp",
        "LdCtrlLoadImageProp",
        "LdCtrlCompareProp",
        "LdCtrlInvokeFunctionProp",
        "LdCtrlReadFunctionProp",
        "LdCtrlAbsSegment",
        "LdCtrlRelSegment",
        "LdCtrlTaskSegment",
        "LdCtrlTaskPtr",
        "LdCtrlTaskCtrl1",
        "LdCtrlTaskCtrl2",
        # xsdata class name (type(control).__name__), not the XML "LdCtrlClearLCFilterTable".
        "LdCtrlClearLcfilterTable",
    }
)


def _application_id(application: Application) -> bytes:
    """Assemble the 5 octet application id (manufacturer, type, version)."""
    manufacturer = application.manufacturer_id.split("-")[-1]
    manufacturer_id = int(manufacturer, 16)
    program = application.program
    return (
        manufacturer_id.to_bytes(2, "big")
        + program.application_number.to_bytes(2, "big")
        + bytes([program.application_version & 0xFF])
    )


class LoadProcedureRunner:
    """Execute an application's Load Procedure over a device connection."""

    def __init__(
        self,
        application: Application,
        image: DownloadImage,
        programmer: DeviceProgrammer | None = None,
        *,
        connection_manager: ConnectionManager | None = None,
        max_apdu_length: int = DEFAULT_MAX_APDU_LENGTH,
        restart_cooldown: float = DEFAULT_RESTART_COOLDOWN,
        controls: Sequence[object] | None = None,
        scope: DownloadScope = DownloadScope.FULL,
        expected_descriptor: int | None = None,
        negotiate_apdu: bool = False,
        apdu_overhead: int = 0,
    ) -> None:
        """Initialize the runner.

        Provide either a fixed ``programmer`` (the connection stays open for the
        whole run; Connect/Disconnect are no-ops) or a ``connection_manager``
        (the runner opens/closes the connection per Connect/Disconnect and after
        a Restart, and auto-connects before any bus control). ``controls`` is the
        resolved Load Control list; when omitted the application's own procedure
        is flattened. ``scope`` selects a full or partial download.

        With a ``connection_manager``, when ``expected_descriptor`` is given the
        device's mask version (device descriptor type 0) is read once on the first
        connection and must match, guarding against programming the wrong device;
        when ``negotiate_apdu`` is set the device's maximum APDU length is read
        once and used for the rest of the run (chunked writes then use larger
        telegrams). Both are skipped for a fixed ``programmer``.
        """
        if programmer is None and connection_manager is None:
            raise DownloadError("provide a programmer or a connection manager")
        self.application = application
        self.image = image
        self.scope = scope
        self.restarted = False
        self._programmer = programmer
        self._manager = connection_manager
        self._max_apdu_length = (
            programmer.max_apdu_length if programmer is not None else max_apdu_length
        )
        self._apdu_overhead = (
            programmer.apdu_overhead if programmer is not None else apdu_overhead
        )
        self._restart_cooldown = restart_cooldown
        self._restart_at: float | None = None
        # A one-shot cooldown that overrides the default for the next reconnect
        # (used when a Master Reset reports a longer device process time).
        self._pending_cooldown: float | None = None
        self._expected_descriptor = expected_descriptor
        self._negotiate_apdu = negotiate_apdu
        self._descriptor_checked = False
        self._negotiated_apdu: int | None = None
        self._controls = (
            list(controls)
            if controls is not None
            else resolve_download_controls(application)
        )
        # Position of the control currently being executed, for diagnostics.
        self._position: tuple[int, int] | None = None

    async def run(self, progress: Callable[[int, int], None] | None = None) -> None:
        """Execute the Load Procedure, honouring the selected download scope.

        ``progress`` (optional) is called ``progress(done, total)`` after each executed
        control, where ``total`` is the number of in-scope controls, so a UI can show
        download progress.
        """
        in_scope = [c for c in self._controls if self._in_scope(c)]
        self._prevalidate(in_scope)
        total = len(in_scope)
        logger.info(
            "download run start: %s, %d of %d load controls in scope",
            self._target(),
            total,
            len(self._controls),
        )
        for done, control in enumerate(in_scope, start=1):
            self._position = (done, total)
            await self._execute(control)
            if progress is not None:
                progress(done, total)
        self._position = None

    async def preflight(self) -> PreflightReport:
        """Report what the download would change, without changing anything.

        Walks the same scoped Load Controls as :meth:`run` but performs no write
        and drives no Load State Machine: for each control that would write, the
        device's current bytes are read and compared against the data the download
        would write. Compare controls (the application fingerprint gate) still run
        - they only read. The connection is opened read-only and closed again.
        """
        segments: list[SegmentDiff] = []
        properties: list[PropertyDiff] = []
        in_scope = [c for c in self._controls if self._in_scope(c)]
        self._prevalidate(in_scope)
        logger.info(
            "download preflight start: %s, %d of %d load controls in scope",
            self._target(),
            len(in_scope),
            len(self._controls),
        )
        try:
            for done, control in enumerate(in_scope, start=1):
                self._position = (done, len(in_scope))
                await self._preflight_control(control, segments, properties)
        finally:
            self._position = None
            await self._close()
        return PreflightReport(segments=tuple(segments), properties=tuple(properties))

    def _in_scope(self, control: object) -> bool:
        """Whether a control participates in the requested download scope."""
        return control_in_scope(control, self.scope)

    def _prevalidate(self, in_scope: list[object]) -> None:
        """Reject an unsupported control before any device state is changed.

        Scans the resolved, scoped controls up front so a procedure containing a
        control this engine cannot execute fails before the connection is opened
        or any Load State Machine is unloaded, rather than partway through
        (leaving the device unloaded). Client-side no-ops are accepted.
        """
        for position, control in enumerate(in_scope, start=1):
            name = type(control).__name__
            if name in _SUPPORTED_CONTROLS or name in _CLIENT_SIDE:
                # A supported control may still use a compare semantic (Invert/Range/Retry) this
                # engine does not implement; reject it up front rather than mis-verify on the bus.
                reason = _unsupported_compare_reason(control)
                if reason is None:
                    continue
                self._position = (position, len(in_scope))
                error = self._unsupported(control, reason=reason)
                self._position = None
                raise error
            self._position = (position, len(in_scope))
            error = self._unsupported(control)
            self._position = None
            raise error

    def _target(self) -> str:
        """A short, log-friendly identity of the download target for diagnostics."""
        try:
            app = _application_id(self.application).hex()
        except (ValueError, AttributeError):
            app = "unknown"
        return f"app={app} scope={self.scope.name}"

    def _unsupported(
        self, control: object, *, reason: str | None = None
    ) -> UnsupportedProcedureError:
        """Build (and log) a diagnostic error for a control this engine can't run.

        The message names the KNX Standard service the control maps to (via
        :mod:`xknxeditor.download.gaps`), the position in the procedure and the
        target, so a bug report shows immediately what is still missing.
        """
        name = type(control).__name__
        detail = reason if reason is not None else gaps.describe_missing(name)
        where = ""
        if self._position is not None:
            where = f" at in-scope load control {self._position[0]}/{self._position[1]}"
        message = (
            f"{detail}{where} [{self._target()}]. Please file a bug report with this "
            f"message, the device order number and the mask version so the missing "
            f"step can be implemented."
        )
        logger.warning("unsupported load control: %s", message)
        return UnsupportedProcedureError(message)

    async def _bus(self) -> DeviceProgrammer:
        """Return the connected programmer, opening a connection if needed."""
        if self._programmer is not None:
            return self._programmer
        if self._manager is None:
            raise DownloadError("no connection available")
        await self._await_restart_cooldown()
        logger.debug("opening device connection")
        connection = await self._manager.open()
        self._programmer = DeviceProgrammer(
            connection,
            max_apdu_length=self._max_apdu_length,
            apdu_overhead=self._apdu_overhead,
        )
        await self._prepare_device(self._programmer)
        return self._programmer

    async def _prepare_device(self, programmer: DeviceProgrammer) -> None:
        """Guard the device mask and negotiate the APDU length, once per run.

        Runs on the first opened connection: reads the device descriptor to
        confirm the mask matches ``expected_descriptor`` (guarding against
        programming the wrong device) and reads the device's maximum APDU length
        to use larger telegrams. The negotiated length is remembered and reapplied
        after a reconnect, so it is read only once.
        """
        if self._expected_descriptor is not None and not self._descriptor_checked:
            actual = await programmer.read_device_descriptor()
            if actual != self._expected_descriptor:
                raise VerificationError(
                    f"device mask mismatch: expected descriptor "
                    f"{self._expected_descriptor:#06x}, device reports {actual:#06x}. "
                    f"Refusing to program - check the individual address points at "
                    f"the intended device."
                )
            self._descriptor_checked = True
            logger.info("device mask confirmed: descriptor %#06x", actual)
        if self._negotiate_apdu:
            if self._negotiated_apdu is None:
                device_max = await programmer.read_max_apdu_length()
                self._negotiated_apdu = max(
                    DEFAULT_MAX_APDU_LENGTH,
                    min(device_max, self._max_apdu_length),
                )
                logger.info(
                    "negotiated APDU length: %d (device reports %d)",
                    self._negotiated_apdu,
                    device_max,
                )
            programmer.max_apdu_length = self._negotiated_apdu

    async def _close(self) -> None:
        """Close the current connection when the runner manages the lifecycle."""
        if self._manager is not None and self._programmer is not None:
            logger.debug("closing device connection")
            await self._manager.close()
            self._programmer = None

    async def _await_restart_cooldown(self) -> None:
        """Wait out the restart cooldown before reconnecting, if one is pending."""
        if self._restart_at is None:
            return
        cooldown = (
            self._pending_cooldown
            if self._pending_cooldown is not None
            else self._restart_cooldown
        )
        elapsed = time.monotonic() - self._restart_at
        remaining = cooldown - elapsed
        if remaining > 0:
            logger.debug("restart cooldown: waiting %.2fs before reconnect", remaining)
            await asyncio.sleep(remaining)
        self._restart_at = None
        self._pending_cooldown = None

    async def _resolve_index(self, control: object) -> int:
        """Resolve the interface object index a control addresses.

        A control identifies its object by explicit ``obj_idx``, by
        ``obj_type`` + zero-based ``occurrence`` (resolved on the device), or by
        ``lsm_idx`` which, for property based management, is the object index.
        """
        obj_idx = getattr(control, "obj_idx", None)
        if obj_idx is not None:
            return obj_idx
        obj_type = getattr(control, "obj_type", None)
        if obj_type is not None:
            occurrence = getattr(control, "occurrence", 0)
            programmer = await self._bus()
            return await programmer.locate_object(obj_type, occurrence)
        lsm_idx = getattr(control, "lsm_idx", None)
        if lsm_idx is not None:
            return lsm_idx
        raise self._unsupported(
            control,
            reason=(
                f"load control {type(control).__name__!r} addresses no interface "
                f"object (neither obj_idx, obj_type nor lsm_idx is set)"
            ),
        )

    async def _execute(self, control: object) -> None:
        """Dispatch a single Load Control to the matching bus operation."""
        where = f" [{self._position[0]}/{self._position[1]}]" if self._position else ""
        logger.debug("execute load control: %s%s", type(control).__name__, where)
        if isinstance(control, LdCtrlConnect):
            await self._bus()
            return
        if isinstance(control, LdCtrlDisconnect):
            await self._close()
            return
        if isinstance(control, LdCtrlDelay):
            await asyncio.sleep(control.milli_seconds / 1000)
            return
        if isinstance(control, LdCtrlRestart):
            programmer = await self._bus()
            await programmer.restart()
            self.restarted = True
            # A Restart tears down the connection device-side; drop it and
            # arm the cooldown so the next control reconnects after a pause.
            await self._close()
            self._restart_at = time.monotonic()
            return
        if isinstance(control, LdCtrlMasterReset):
            programmer = await self._bus()
            process_time = await programmer.master_reset(
                control.erase_code, control.channel_number
            )
            self.restarted = True
            # Like a Restart, the device drops the connection; additionally it
            # reports how long it stays unreachable, so honour that as the
            # one-shot reconnect cooldown when it exceeds the default.
            await self._close()
            self._restart_at = time.monotonic()
            # Process Time is a 2 octet unsigned value in *seconds* (DPT 7.005,
            # KNX 3/5/2 3.7.1.2.2), so use it directly - not milliseconds.
            self._pending_cooldown = max(self._restart_cooldown, process_time)
            return
        if isinstance(control, LdCtrlUnload):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            await programmer.send_load_event(
                index, load_state.unload(), load_state.LoadState.UNLOADED
            )
            return
        if isinstance(control, LdCtrlLoad):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            await programmer.send_load_event(
                index, load_state.start_loading(), load_state.LoadState.LOADING
            )
            return
        if isinstance(control, LdCtrlLoadCompleted):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            await programmer.send_load_event(
                index, load_state.load_complete(), load_state.LoadState.LOADED
            )
            return
        if isinstance(control, LdCtrlWriteMem):
            await self._write_mem(control)
            return
        if isinstance(control, LdCtrlLoadImageMem):
            # LoadImageMem reads device memory into the image (read-back /
            # compare), it does not write.
            _require_standard(control.address_space)
            programmer = await self._bus()
            await programmer.read_memory(control.address, control.size)
            return
        if isinstance(control, LdCtrlCompareMem):
            _require_standard(control.address_space)
            await self._compare_mem(control.address, control.inline_data, control.mask)
            return
        if isinstance(control, LdCtrlWriteRelMem):
            await self._write_rel_mem(control)
            return
        if isinstance(control, LdCtrlCompareRelMem):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            base = await programmer.read_table_reference(index)
            await self._compare_mem(
                base + control.offset, control.inline_data, control.mask
            )
            return
        if isinstance(control, LdCtrlLoadImageRelMem):
            # Read-back into the image (see LoadImageMem); it does not write.
            index = await self._resolve_index(control)
            programmer = await self._bus()
            base = await programmer.read_table_reference(index)
            await programmer.read_memory(base + control.offset, control.size)
            return
        if isinstance(control, LdCtrlWriteProp):
            await self._write_prop(control)
            return
        if isinstance(control, LdCtrlLoadImageProp):
            # LoadImageProp reads an interface object property into the image
            # (read-back / compare), it does not write.
            index = await self._resolve_index(control)
            programmer = await self._bus()
            await programmer.read_property(
                index,
                control.prop_id,
                count=control.count,
                start_index=control.start_element,
            )
            return
        if isinstance(control, LdCtrlCompareProp):
            await self._compare_prop(control)
            return
        if isinstance(control, LdCtrlInvokeFunctionProp):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            await programmer.invoke_function_property(
                index, control.prop_id, control.inline_data or b""
            )
            return
        if isinstance(control, LdCtrlReadFunctionProp):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            await programmer.read_function_property(index, control.prop_id)
            return
        if isinstance(control, LdCtrlAbsSegment):
            await self._abs_segment(control)
            return
        if isinstance(control, LdCtrlRelSegment):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            await programmer.send_load_event(
                index,
                load_state.data_relative_allocation(
                    control.size, mode=control.mode, fill=control.fill
                ),
                load_state.LoadState.LOADING,
            )
            return
        if isinstance(control, LdCtrlTaskSegment):
            await self._task_segment(control)
            return
        if isinstance(control, LdCtrlTaskPtr):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            await programmer.send_load_event(
                index,
                load_state.task_pointer(
                    control.init_ptr, control.save_ptr, control.serial_ptr
                ),
                load_state.LoadState.LOADING,
            )
            return
        if isinstance(control, LdCtrlTaskCtrl1):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            await programmer.send_load_event(
                index,
                load_state.task_control_1(control.address, control.count),
                load_state.LoadState.LOADING,
            )
            return
        if isinstance(control, LdCtrlTaskCtrl2):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            await programmer.send_load_event(
                index,
                load_state.task_control_2(
                    control.callback, control.address, control.seg0, control.seg1
                ),
                load_state.LoadState.LOADING,
            )
            return
        if isinstance(control, LdCtrlClearLcfilterTable):
            # Clear the line-coupler filter table. A coupler download writes the whole
            # filter table right after (LdCtrlRelSegment + LdCtrlWriteRelMem over the full
            # 8192/3584-byte resource, zero bits included — see the coupler load procedures
            # in the KNX master data, e.g. MV-2920/MV-0900), so an explicit clear is
            # redundant for a full download and is a no-op here. The function-property /
            # memory clear only matters for a partial filter-table update, which this engine
            # does not perform. The filter-table bytes themselves must be supplied in the
            # image (see GroupCommunication.filter_table); otherwise the following
            # WriteRelMem/WriteMem fails with "no image data".
            return
        if type(control).__name__ in _CLIENT_SIDE:
            return
        raise self._unsupported(control)

    async def _write_mem(self, control: LdCtrlWriteMem) -> None:
        """Write a WriteMem control to memory.

        The data is the control's inline data, or - when none is given - the
        download image slice at the control's address (an image backed write).
        """
        _require_standard(control.address_space)
        programmer = await self._bus()
        if control.inline_data is not None:
            logger.debug(
                "write_mem inline: addr=%#06x len=%d verify=%s",
                control.address,
                len(control.inline_data),
                control.verify,
            )
            await programmer.write_memory(
                control.address, control.inline_data, verify=control.verify
            )
            return
        # BCU1 coupler: the filter table lives in the LcFilter absolute address space and is carried
        # as the image's dedicated filter-table field, not a normal memory segment. Write it (clipped
        # to the control's resource size) at the control's absolute address.
        if (
            control.address_space is LdCtrlMemAddrSpace.LC_FILTER
            and self.image.filter_table is not None
        ):
            await programmer.write_memory(
                control.address,
                self.image.filter_table[: control.size],
                verify=control.verify,
            )
            return
        runs = self.image.masked_writes(control.address, control.size)
        if runs is None:
            raise ImageError(
                f"no image data for address range {control.address:#06x}.."
                f"{control.address + control.size:#06x}"
            )
        logger.debug(
            "write_mem image-backed: addr=%#06x size=%d runs=%d verify=%s",
            control.address,
            control.size,
            len(runs),
            control.verify,
        )
        for address, data in runs:
            await programmer.write_memory(address, data, verify=control.verify)

    async def _write_rel_mem(self, control: LdCtrlWriteRelMem) -> None:
        """Write a WriteRelMem control relative to the object's table base.

        The image mirrors a relative segment in its own relative address space
        (the segment sits at its relative base, e.g. ``0``); only the device write
        adds the table base read from the object at run time. So the image is
        looked up at ``control.offset`` and each run is written at ``base + run``.
        """
        index = await self._resolve_index(control)
        programmer = await self._bus()
        base = await programmer.read_table_reference(index)
        logger.debug(
            "write_rel_mem: obj-index=%d table-base=%#06x offset=%#06x size=%d",
            index,
            base,
            control.offset,
            control.size,
        )
        if control.inline_data is not None:
            await programmer.write_memory(
                base + control.offset, control.inline_data, verify=control.verify
            )
            return
        runs = self._relative_runs(control)
        if runs is None:
            raise ImageError(
                f"no image data for relative range {control.offset:#06x}.."
                f"{control.offset + control.size:#06x}"
            )
        for run_offset, data in runs:
            await programmer.write_memory(
                base + run_offset, data, verify=control.verify
            )

    def _relative_runs(
        self, control: LdCtrlWriteRelMem
    ) -> list[tuple[int, bytes]] | None:
        """Return the relative ``(offset, data)`` runs a WriteRelMem writes.

        Prefers a relative segment keyed by the control's interface object type
        (the System B group communication tables); otherwise falls back to the
        flat image at ``control.offset`` (the parameter relative segment).
        """
        object_type = getattr(control, "obj_type", None)
        # A coupler's filter table (Router object type 6) is carried as its own image field.
        if object_type == _ROUTER_OBJECT_TYPE and self.image.filter_table is not None:
            return [(0, self.image.filter_table)]
        if object_type is not None:
            segment = self.image.relative_segment(object_type)
            if segment is not None:
                return segment.masked_runs()
        return self.image.masked_writes(control.offset, control.size)

    async def _compare_mem(
        self, address: int, expected: bytes, mask: bytes | None = None
    ) -> None:
        """Read memory and compare it against expected data (mask-aware, like _compare_prop)."""
        programmer = await self._bus()
        read_back = await programmer.read_memory(address, len(expected))
        matched = _bytes_match(read_back, expected, mask, len(expected))
        logger.debug(
            "compare_mem: addr=%#06x len=%d masked=%s -> %s",
            address,
            len(expected),
            mask is not None,
            "match" if matched else "MISMATCH",
        )
        if not matched:
            raise VerificationError(
                f"memory compare failed at {address:#06x}: "
                f"expected {expected.hex()} read {read_back.hex()}"
            )

    def _property_write_data(self, index: int, control: LdCtrlWriteProp) -> bytes:
        """The octets a WriteProp writes: inline data, else the image's property.

        For the Memory Control Block table (PID_MCB_TABLE) the per-segment CRC is
        computed over the segment data and patched into each 8 octet entry, since
        the application program carries only a zero CRC placeholder there.
        """
        data = (
            control.inline_data
            if control.inline_data is not None
            else self._image_property_data(index, control.prop_id)
        )
        if control.prop_id == _PID_MCB_TABLE:
            segment = self.image.object_segments.get(index)
            if segment is not None:
                data = _mcb_table_with_crc(data, segment)
        return data

    async def _write_prop(self, control: LdCtrlWriteProp) -> None:
        """Write a WriteProp control to a property.

        The data is the control's inline data, or - when none is given - the
        matching property data from the download image (an image backed write:
        inline data if present, else the image's property data).
        """
        index = await self._resolve_index(control)
        data = self._property_write_data(index, control)
        programmer = await self._bus()
        await programmer.write_property(
            index,
            control.prop_id,
            data,
            count=control.count,
            start_index=control.start_element,
        )
        if control.verify:
            read_back = await programmer.read_property(
                index,
                control.prop_id,
                count=control.count,
                start_index=control.start_element,
            )
            if read_back != data:
                raise VerificationError(
                    f"property verification failed for object {index} "
                    f"property {control.prop_id}"
                )

    def _image_property_data(self, object_index: int, property_id: int) -> bytes:
        """Find the download image's property data for an object and property.

        Matches on the resolved device object index (or an object-agnostic image
        property). Note: the image keys properties by object index, not by
        (object type, occurrence), so a product with several instances of the
        same object type that carry *different* per-instance property images is
        not distinguished here - the first matching property wins. No such device
        has been observed; a fix would resolve by (object type, occurrence).
        """
        for prop in self.image.properties:
            if prop.property_id != property_id:
                continue
            if prop.object_index in (object_index, None):
                return prop.data
        raise ImageError(
            f"no image property data for object {object_index} property {property_id}"
        )

    async def _compare_prop(self, control: LdCtrlCompareProp) -> None:
        """Read a property and compare it against expected data.

        The compare is mask driven when the control carries a ``mask`` (only the
        marked bits of each octet have to match, e.g. the application-number bytes
        of the application id while manufacturer and version are ignored). The
        device's property length is authoritative: a procedure often carries the
        property's maximum element size padded with trailing zeros while the device
        reports only its actual length, so only the overlapping prefix is compared.
        """
        index = await self._resolve_index(control)
        programmer = await self._bus()
        read_back = await programmer.read_property(
            index,
            control.prop_id,
            count=control.count,
            start_index=control.start_element,
        )
        expected = control.inline_data
        # A device that returns no data (absent property / rejected read) must
        # not pass the compare vacuously - the overlapping-prefix rule below
        # would otherwise match against an empty prefix.
        if not read_back:
            raise VerificationError(
                f"property compare for object {index} property {control.prop_id} "
                "read no data from the device"
            )
        mask = control.mask
        length = min(len(read_back), len(expected))
        if not _bytes_match(read_back, expected, mask, length):
            raise VerificationError(
                f"property compare failed for object {index} property "
                f"{control.prop_id}: expected {expected.hex()} "
                f"read {read_back.hex()}"
            )

    async def _abs_segment(self, control: LdCtrlAbsSegment) -> None:
        """Allocate an absolute segment, then write the image data for its range.

        A procedure may carry no explicit memory-write controls (property based
        System B products): the download image is written into the segments the
        procedure allocates. So after allocating the segment we write the image
        slice that covers it - the segment address and size match an image
        segment exactly. Segments the image does not cover are only allocated.
        """
        segment_type = load_state.SegmentType(control.seg_type)
        index = await self._resolve_index(control)
        programmer = await self._bus()
        await programmer.send_load_event(
            index,
            load_state.alloc_absolute_segment(
                segment_type,
                control.address,
                control.size,
                access_attributes=control.access,
                memory_type=control.mem_type,
                memory_attributes=control.seg_flags,
            ),
            load_state.LoadState.LOADING,
        )
        # Per the KNX Load Controls (KNX Standard v3.0.0, 2/3/1) an AbsSegment
        # allocation is followed by a verified memory write of the segment data -
        # but only the bytes the image actually produced (its mask). Bytes the
        # encoder did not write stay at their current device value.
        runs = self.image.masked_writes(control.address, control.size)
        if runs:
            for address, data in runs:
                await programmer.write_memory(address, data, verify=True)

    async def _task_segment(self, control: LdCtrlTaskSegment) -> None:
        """Allocate the task segment via a load event."""
        index = await self._resolve_index(control)
        programmer = await self._bus()
        await programmer.send_load_event(
            index,
            load_state.alloc_task_segment(
                control.address,
                self.application.program.pei_type,
                _application_id(self.application),
            ),
            load_state.LoadState.LOADING,
        )

    async def _preflight_control(
        self,
        control: object,
        segments: list[SegmentDiff],
        properties: list[PropertyDiff],
    ) -> None:
        """Read-only preview of a single control (see :meth:`preflight`).

        Only controls with a write effect are previewed (by reading the current
        device bytes and recording a diff); compare controls still run as a gate.
        Load state events, allocations, restart, delays and read-back controls
        have no write to preview and are ignored.
        """
        if isinstance(control, LdCtrlConnect):
            await self._bus()
            return
        if isinstance(control, LdCtrlDisconnect):
            await self._close()
            return
        if isinstance(control, LdCtrlWriteMem):
            _require_standard(control.address_space)
            if control.inline_data is not None:
                await self._diff_memory(control.address, control.inline_data, segments)
            else:
                await self._diff_masked(control.address, control.size, segments)
            return
        if isinstance(control, LdCtrlWriteRelMem):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            base = await programmer.read_table_reference(index)
            if control.inline_data is not None:
                await self._diff_memory(
                    base + control.offset, control.inline_data, segments
                )
            else:
                await self._diff_masked_rel(base, control, segments)
            return
        if isinstance(control, LdCtrlAbsSegment):
            # An allocation whose range the image covers is an image backed write;
            # preview only the bytes the image actually writes (its mask).
            await self._diff_masked(control.address, control.size, segments)
            return
        if isinstance(control, LdCtrlWriteProp):
            index = await self._resolve_index(control)
            planned = self._property_write_data(index, control)
            await self._diff_property(
                index,
                control.prop_id,
                control.count,
                control.start_element,
                planned,
                properties,
            )
            return
        if isinstance(control, LdCtrlCompareMem):
            _require_standard(control.address_space)
            await self._compare_mem(control.address, control.inline_data, control.mask)
            return
        if isinstance(control, LdCtrlCompareRelMem):
            index = await self._resolve_index(control)
            programmer = await self._bus()
            base = await programmer.read_table_reference(index)
            await self._compare_mem(
                base + control.offset, control.inline_data, control.mask
            )
            return
        if isinstance(control, LdCtrlCompareProp):
            await self._compare_prop(control)
            return
        # Anything left is either a control with no write to preview (fine) or a
        # step this engine does not implement. Do not fail the read-only preview,
        # but log the gap so a bug report shows the preview was incomplete.
        name = type(control).__name__
        if name not in gaps.PREFLIGHT_NO_WRITE:
            logger.warning(
                "preflight cannot preview %s [%s]: %s",
                name,
                self._target(),
                gaps.describe_missing(name),
            )

    async def _diff_memory(
        self, address: int, planned: bytes, segments: list[SegmentDiff]
    ) -> None:
        """Read current memory at ``address`` and record a diff against ``planned``."""
        programmer = await self._bus()
        current = await programmer.read_memory(address, len(planned))
        segments.append(
            SegmentDiff(address=address, current=current, planned=bytes(planned))
        )

    async def _diff_masked(
        self, address: int, size: int, segments: list[SegmentDiff]
    ) -> None:
        """Diff each masked write run the image would apply within ``[address, size)``."""
        runs = self.image.masked_writes(address, size)
        if not runs:
            return
        programmer = await self._bus()
        for run_address, planned in runs:
            current = await programmer.read_memory(run_address, len(planned))
            segments.append(
                SegmentDiff(
                    address=run_address, current=current, planned=bytes(planned)
                )
            )

    async def _diff_masked_rel(
        self, base: int, control: LdCtrlWriteRelMem, segments: list[SegmentDiff]
    ) -> None:
        """Diff a relative segment: image at ``offset``, device at ``base + run``.

        Mirrors :meth:`_write_rel_mem` - the image holds the segment in its own
        relative address space, and the device address adds the run-time table base.
        """
        runs = self._relative_runs(control)
        if not runs:
            return
        programmer = await self._bus()
        for run_offset, planned in runs:
            current = await programmer.read_memory(base + run_offset, len(planned))
            segments.append(
                SegmentDiff(
                    address=base + run_offset,
                    current=current,
                    planned=bytes(planned),
                )
            )

    async def _diff_property(
        self,
        object_index: int,
        property_id: int,
        count: int,
        start_element: int,
        planned: bytes,
        properties: list[PropertyDiff],
    ) -> None:
        """Read the current property value and record a diff against ``planned``."""
        programmer = await self._bus()
        current = await programmer.read_property(
            object_index,
            property_id,
            count=count,
            start_index=start_element,
        )
        properties.append(
            PropertyDiff(
                object_index=object_index,
                property_id=property_id,
                current=current,
                planned=bytes(planned),
            )
        )


# Memory address spaces this engine writes as a flat absolute A_Memory access. STANDARD is the
# normal device memory; LC_FILTER (a BCU1 coupler's filter-table region) and LC_SLAVE (its
# slave-side BCU config region) both live in ordinary EEPROM addressed absolutely and are written by
# the same A_Memory_Write (KNX Standard v3.0.0, 3/5/1 Resources; both are plain memory, distinct
# from properties/relative memory). USER memory needs the A_UserMemory services and is not
# implemented.
_ABSOLUTE_MEMORY_SPACES = frozenset(
    {
        LdCtrlMemAddrSpace.STANDARD,
        LdCtrlMemAddrSpace.LC_FILTER,
        LdCtrlMemAddrSpace.LC_SLAVE,
    }
)


def _require_standard(address_space: LdCtrlMemAddrSpace) -> None:
    """Reject memory operations outside the flat absolute address spaces (STANDARD/LcFilter/LcSlave)."""
    if address_space not in _ABSOLUTE_MEMORY_SPACES:
        message = (
            f"memory address space {address_space.value!r} is not implemented; only the standard, "
            f"LcFilter and LcSlave (all flat absolute A_Memory) address spaces are handled (KNX "
            f"Standard v3.0.0, 3/5/1 Resources). User memory needs the A_UserMemory services; "
            f"please file a bug report with the product data so it can be added."
        )
        logger.warning("unsupported load control: %s", message)
        raise UnsupportedProcedureError(message)
