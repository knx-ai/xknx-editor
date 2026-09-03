"""Tests for the Memory Control Block segment CRC.

The golden CRC is validated byte-exact against a real System B device (the MCB
table entry for its parameter segment reads 0x47c9).
"""

from __future__ import annotations

from xknxmono.download.crc import segment_crc
from xknxmono.download.procedure import _mcb_table_with_crc


def test_segment_crc_matches_hardware() -> None:
    segment = bytes.fromhex("577a456e060300ff000000000000003c")
    assert segment_crc(segment) == 0x47C9


def test_segment_crc_empty() -> None:
    # Initial value of the augmented CCITT variant.
    assert segment_crc(b"") == 0x1D0F


def test_mcb_table_patches_crc_into_entry() -> None:
    segment = bytes.fromhex("577a456e060300ff000000000000003c")
    # 8 octet entry (CRC-protected: octet 4 bit 0 clear) plus two trailing octets
    mcb = bytes.fromhex("00000010003200000000")
    assert _mcb_table_with_crc(mcb, segment) == bytes.fromhex("00000010003247c90000")


def test_mcb_table_skips_unprotected_entry() -> None:
    segment = bytes.fromhex("577a456e060300ff000000000000003c")
    # octet 4 bit 0 set -> not CRC-protected, CRC octets left untouched
    mcb = bytes.fromhex("0000001001320000")
    assert _mcb_table_with_crc(mcb, segment) == mcb
