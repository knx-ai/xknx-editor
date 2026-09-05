"""Tests for the low level device programmer."""

from __future__ import annotations

import pytest
from xknx.telegram.apci import MemoryRead, MemoryWrite, PropertyValueWrite

from xknxeditor.download.errors import LoadStateError, VerificationError
from xknxeditor.download.load_state import LoadState, start_loading
from xknxeditor.download.programmer import PID_OBJECT_TYPE, DeviceProgrammer

from .conftest import FakeDevice


class _CappingConnection:
    """A connection that answers A_Memory_Read with at most ``cap`` octets.

    Models a device that limits its memory-read reply below the negotiated APDU.
    """

    def __init__(self, memory: bytes, cap: int) -> None:
        self._memory = memory
        self._cap = cap
        self.request_counts: list[int] = []

    async def send_data(self, payload: object, wait_for_ack: bool = True) -> None:
        raise AssertionError("unexpected send_data")

    async def request(self, payload: object, expected: object) -> object:
        from xknx.telegram import IndividualAddress, Telegram
        from xknx.telegram.apci import MemoryResponse

        assert isinstance(payload, MemoryRead)
        n = min(payload.count, self._cap)
        self.request_counts.append(payload.count)
        data = self._memory[payload.address : payload.address + n]
        return Telegram(
            destination_address=IndividualAddress("1.1.1"),
            payload=MemoryResponse(address=payload.address, data=data),
        )


async def test_read_memory_tolerates_short_replies() -> None:
    memory = bytes(range(20))
    connection = _CappingConnection(memory, cap=4)
    programmer = DeviceProgrammer(connection, max_apdu_length=55)  # asks up to 52
    result = await programmer.read_memory(0, 20)
    assert result == memory  # reassembled from 4-octet replies
    # After the first short reply the read stops over-asking (caps at 4).
    assert connection.request_counts[0] > 4
    assert all(count <= 4 for count in connection.request_counts[1:])


async def test_read_memory_raises_on_empty_reply() -> None:
    connection = _CappingConnection(b"", cap=0)
    programmer = DeviceProgrammer(connection, max_apdu_length=15)
    with pytest.raises(VerificationError, match="no memory response"):
        await programmer.read_memory(0, 8)


def test_memory_chunk_size_respects_apdu() -> None:
    assert DeviceProgrammer(FakeDevice(), max_apdu_length=15).memory_chunk_size == 12
    assert DeviceProgrammer(FakeDevice(), max_apdu_length=55).memory_chunk_size == 52


def test_memory_chunk_size_accounts_for_secure_overhead() -> None:
    # A Data Secure session adds 13 octets, so the plaintext ceiling shrinks by
    # 13 before the memory overhead is applied: 55 - 13 - 3 = 39.
    programmer = DeviceProgrammer(FakeDevice(), max_apdu_length=55, apdu_overhead=13)
    assert programmer.memory_chunk_size == 39
    # A tiny APDU still yields at least a 1-octet chunk.
    assert (
        DeviceProgrammer(
            FakeDevice(), max_apdu_length=15, apdu_overhead=13
        ).memory_chunk_size
        == 1
    )


async def test_write_memory_is_chunked() -> None:
    device = FakeDevice()
    programmer = DeviceProgrammer(device, max_apdu_length=15)
    data = bytes(range(30))

    await programmer.write_memory(0x4000, data)

    writes = [p for p in device.sent if isinstance(p, MemoryWrite)]
    assert [len(w.data) for w in writes] == [12, 12, 6]
    assert [w.address for w in writes] == [0x4000, 0x400C, 0x4018]
    read_back = bytes(device.memory[0x4000 + i] for i in range(30))
    assert read_back == data


async def test_read_memory_reassembles_chunks() -> None:
    device = FakeDevice()
    device.memory.update({0x100 + i: i for i in range(20)})
    programmer = DeviceProgrammer(device, max_apdu_length=15)

    assert await programmer.read_memory(0x100, 20) == bytes(range(20))


async def test_write_memory_verify_success() -> None:
    device = FakeDevice()
    programmer = DeviceProgrammer(device)
    await programmer.write_memory(0x10, b"\x01\x02\x03", verify=True)


async def test_write_memory_verify_detects_mismatch() -> None:
    class DroppingDevice(FakeDevice):
        async def send_data(self, payload: object, wait_for_ack: bool = True) -> None:
            if isinstance(payload, MemoryWrite):
                return  # silently drop the write
            await super().send_data(payload, wait_for_ack)  # type: ignore[arg-type]

    programmer = DeviceProgrammer(DroppingDevice())
    with pytest.raises(VerificationError, match="verification failed"):
        await programmer.write_memory(0x10, b"\x01\x02\x03", verify=True)


async def test_property_round_trip() -> None:
    device = FakeDevice()
    programmer = DeviceProgrammer(device)
    await programmer.write_property(5, 0x33, b"\xaa\xbb")
    assert await programmer.read_property(5, 0x33) == b"\xaa\xbb"


async def test_write_property_chunks_large_value() -> None:
    device = FakeDevice()
    programmer = DeviceProgrammer(device, max_apdu_length=15)
    # 20 one-byte elements, 10 data octets fit a frame -> two frames of 10
    await programmer.write_property(5, 0x10, bytes(20), count=20)
    writes = [p for p in device.sent if isinstance(p, PropertyValueWrite)]
    assert [w.count for w in writes] == [10, 10]
    assert [w.start_index for w in writes] == [1, 11]


async def test_write_memory_verify_reads_back_each_block() -> None:
    device = FakeDevice()
    programmer = DeviceProgrammer(device, max_apdu_length=15)  # 12 byte chunks
    await programmer.write_memory(0x10, bytes(20), verify=True)
    reads = [p for p in device.sent if isinstance(p, MemoryRead)]
    assert len(reads) == 2  # one read-back per written block


async def test_read_table_reference() -> None:
    device = FakeDevice()
    device.table_references[2] = 0x1234
    assert await DeviceProgrammer(device).read_table_reference(2) == 0x1234


def test_memory_chunk_size_never_below_one() -> None:
    assert DeviceProgrammer(FakeDevice(), max_apdu_length=2).memory_chunk_size == 1


async def test_locate_object_by_type_and_occurrence() -> None:
    device = FakeDevice(object_types={0: 0, 1: 0x0100, 2: 0x0100})
    programmer = DeviceProgrammer(device)

    # occurrence is zero-based: 0 == first instance, 1 == second
    assert await programmer.locate_object(0x0100, occurrence=0) == 1
    assert await programmer.locate_object(0x0100, occurrence=1) == 2
    # second lookup is served from the cache without further reads
    reads_before = len(device.sent)
    assert await programmer.locate_object(0x0100, occurrence=0) == 1
    assert len(device.sent) == reads_before


async def test_locate_object_reads_object_type_property() -> None:
    device = FakeDevice(object_types={0: 0x0000, 1: 0x0007})
    programmer = DeviceProgrammer(device)
    await programmer.locate_object(0x0007)
    assert any(getattr(p, "property_id", None) == PID_OBJECT_TYPE for p in device.sent)


async def test_locate_object_missing_raises() -> None:
    device = FakeDevice(object_types={0: 0x0000})
    programmer = DeviceProgrammer(device)
    with pytest.raises(LoadStateError, match="not found"):
        await programmer.locate_object(0x9999)


async def test_send_load_event_reaches_expected_state() -> None:
    device = FakeDevice()
    programmer = DeviceProgrammer(device)
    await programmer.send_load_event(3, start_loading(), LoadState.LOADING)
    assert device.load_states[3] == LoadState.LOADING


async def test_send_load_event_error_state_raises() -> None:
    class ErrorDevice(FakeDevice):
        def _handle_property_write(self, payload: object) -> None:
            self.load_states[payload.object_index] = LoadState.ERROR  # type: ignore[attr-defined]

    programmer = DeviceProgrammer(ErrorDevice())
    with pytest.raises(LoadStateError, match="ERROR"):
        await programmer.send_load_event(3, start_loading(), LoadState.LOADING)


async def test_send_load_event_timeout_raises() -> None:
    class StuckDevice(FakeDevice):
        def _handle_property_write(self, payload: object) -> None:
            return  # never changes state, stays UNLOADED

    programmer = DeviceProgrammer(StuckDevice())
    with pytest.raises(LoadStateError, match="did not reach"):
        await programmer.send_load_event(
            3, start_loading(), LoadState.LOADING, retries=2, retry_delay=0
        )


async def test_restart() -> None:
    device = FakeDevice()
    await DeviceProgrammer(device).restart()
    assert device.restarted
