"""Segment CRC used by the Memory Control Block (MCB) table.

Per KNX Standard v3.0.0, Chapter 3/5/1 "Resources", section 4.2.27
"PID_MCB_TABLE (PID = 27)", each loaded segment referenced by the Memory Control
Block Table is protected by a 16 bit CRC over the segment's data; the download
writes that CRC into the MCB entry so the device can verify the segment.

That section specifies the CRC as CRC-16/CCITT with truncated polynomial
``0x1021``, input and output not reflected and no final xor, and gives the check
value ``0xE5CC`` for the string ``"123456789"``. That check value corresponds to
the initial value ``0x1D0F`` (the augmented CCITT variant) used here - the "FFFFh"
initial value quoted in the prose does not reproduce the specified check value.
"""

from __future__ import annotations

from collections.abc import Iterable

_POLYNOMIAL = 0x1021
_INITIAL = 0x1D0F


def segment_crc(data: Iterable[int]) -> int:
    """Return the 16 bit MCB CRC over ``data`` (an iterable of octets)."""
    crc = _INITIAL
    for octet in data:
        crc ^= (octet & 0xFF) << 8
        for _ in range(8):
            crc = (
                ((crc << 1) ^ _POLYNOMIAL) & 0xFFFF
                if crc & 0x8000
                else (crc << 1) & 0xFFFF
            )
    return crc
