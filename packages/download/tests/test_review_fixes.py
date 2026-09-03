"""Tests for the download hardening fixes from the code review.

Each test pins a behaviour that was corrected against the KNX standard and the
decompiled ETS/Falcon reference (see the cited comments in the source).
"""

from __future__ import annotations

import pytest
from xknx.telegram.apci import UserMemoryRead, UserMemoryWrite

from xknxmono.download.crc import segment_crc
from xknxmono.download.errors import (
    LoadStateError,
    UnsupportedProcedureError,
    VerificationError,
)
from xknxmono.download.procedure import LoadProcedureRunner, _mcb_table_with_crc
from xknxmono.download.programmer import DeviceProgrammer

from .conftest import FakeDevice


def _mcb_entry(size: int, *, protected: bool) -> bytes:
    # Octets: [0..3] size (low 16 bits first, each half big-endian, per gy.c),
    # [4] flags (bit0 clear = CRC protected), [5] reserved, [6..7] CRC placeholder.
    low = (size & 0xFFFF).to_bytes(2, "big")
    high = (size >> 16).to_bytes(2, "big")
    flags = 0x00 if protected else 0x01
    return low + high + bytes([flags, 0x00, 0x00, 0x00])


def test_mcb_crc_single_entry_covers_whole_segment() -> None:
    segment = bytes(range(16))
    table = _mcb_entry(16, protected=True)
    out = _mcb_table_with_crc(table, segment)
    crc = segment_crc(segment)
    assert out[6:8] == bytes([(crc >> 8) & 0xFF, crc & 0xFF])


def test_mcb_crc_per_entry_partitions_the_segment() -> None:
    # Two entries: 4 protected octets, then 1 mutable octet (like the Gira
    # fixture the review cited). The protected CRC must cover only the first 4.
    segment = bytes(range(5))
    table = _mcb_entry(4, protected=True) + _mcb_entry(1, protected=False)
    out = _mcb_table_with_crc(table, segment)
    crc = segment_crc(segment[:4])
    assert out[6:8] == bytes([(crc >> 8) & 0xFF, crc & 0xFF])
    # The unprotected entry is left untouched (placeholder CRC 00 00).
    assert out[14:16] == b"\x00\x00"


def test_mcb_crc_falls_back_when_sizes_do_not_tile() -> None:
    # An entry whose declared size does not match the segment falls back to a
    # single CRC over the whole segment (never regress the validated behaviour).
    segment = bytes(range(16))
    table = _mcb_entry(99, protected=True)
    out = _mcb_table_with_crc(table, segment)
    crc = segment_crc(segment)
    assert out[6:8] == bytes([(crc >> 8) & 0xFF, crc & 0xFF])


async def test_write_memory_splits_at_64_kib_boundary() -> None:
    device = FakeDevice()
    programmer = DeviceProgrammer(device, max_apdu_length=55)
    # A write straddling 0x10000 must split into a Memory part below and a
    # UserMemory part at/above the boundary.
    await programmer.write_memory(0xFFFE, bytes(range(8)))
    memory_writes = [p for p in device.sent if type(p).__name__ == "MemoryWrite"]
    user_writes = [p for p in device.sent if isinstance(p, UserMemoryWrite)]
    assert memory_writes and user_writes
    assert max(p.address for p in memory_writes) < 0x10000
    assert min(p.address for p in user_writes) == 0x10000
    # Bytes land contiguously regardless of the split.
    assert bytes(device.memory[0xFFFE + i] for i in range(8)) == bytes(range(8))


async def test_read_memory_above_boundary_uses_user_memory() -> None:
    device = FakeDevice()
    device.memory.update({0x10000 + i: i for i in range(4)})
    programmer = DeviceProgrammer(device, max_apdu_length=55)
    assert await programmer.read_memory(0x10000, 4) == bytes(range(4))
    assert any(isinstance(p, UserMemoryRead) for p in device.sent)


async def test_write_property_rejects_zero_count() -> None:
    programmer = DeviceProgrammer(FakeDevice(), max_apdu_length=55)
    with pytest.raises(VerificationError, match="non-positive element count"):
        await programmer.write_property(0, 5, b"\x01\x02", count=0)


async def test_write_property_rejects_indivisible_data() -> None:
    programmer = DeviceProgrammer(FakeDevice(), max_apdu_length=55)
    with pytest.raises(VerificationError, match="not divisible"):
        await programmer.write_property(0, 5, b"\x01\x02\x03", count=2)


async def test_write_property_rejects_oversized_element() -> None:
    programmer = DeviceProgrammer(FakeDevice(), max_apdu_length=15)
    with pytest.raises(VerificationError, match="does not fit the APDU"):
        await programmer.write_property(0, 5, bytes(64), count=1)


async def test_read_table_reference_rejects_zero() -> None:
    device = FakeDevice()
    device.table_references[2] = 0
    programmer = DeviceProgrammer(device, max_apdu_length=55)
    with pytest.raises(LoadStateError, match="zero table reference"):
        await programmer.read_table_reference(2)


class _UnknownControl:
    """A load control this engine does not implement."""


class _RecordingManager:
    def __init__(self, device: FakeDevice) -> None:
        self._device = device
        self.opened = 0

    async def open(self) -> FakeDevice:
        self.opened += 1
        return self._device

    async def close(self) -> None:
        pass


async def test_prevalidate_rejects_unsupported_control_before_connecting() -> None:
    device = FakeDevice()
    manager = _RecordingManager(device)
    runner = LoadProcedureRunner(
        object(),  # type: ignore[arg-type]
        object(),  # type: ignore[arg-type]
        connection_manager=manager,
        controls=[_UnknownControl()],
    )
    with pytest.raises(UnsupportedProcedureError):
        await runner.run()
    # The connection is never opened - the device is left untouched.
    assert manager.opened == 0
