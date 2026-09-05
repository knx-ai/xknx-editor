"""Tests for Device Object dossier decoding."""

from __future__ import annotations

from xknxeditor.recover.dossier import _ascii


def test_ascii_extracts_order_number_stem_from_wrapped_bytes() -> None:
    # Hager AKH-0800: 0x22 '"' prefix, "0800", FFFF, structural tail. The longest
    # printable run (which includes the leading quote) carries the order number.
    assert _ascii(bytes.fromhex("2230383030FFFF020F31")) == '"0800'


def test_ascii_returns_whole_printable_value() -> None:
    assert _ascii(b"ITR524-16A\x00\x00") == "ITR524-16A"


def test_ascii_falls_back_to_hex_without_printable_run() -> None:
    assert _ascii(bytes([0x01, 0xFF, 0x02])) == "01FF02"


def test_ascii_empty_is_none() -> None:
    assert _ascii(b"\x00\x00") is None
