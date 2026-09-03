"""Tests for :mod:`xknxmono.product.app_id`."""

from xknxmono.product.app_id import ParsedAppId, parse_app_id


def test_parse_standard_id() -> None:
    parsed = parse_app_id("M-0083_A-0040-25-F9E1")
    assert parsed == ParsedAppId(
        manufacturer_id="M-0083",
        application_number=0x40,
        version=0x25,
        hash="F9E1",
    )


def test_version_is_hex() -> None:
    # A-0040-22 -> application_number 64, version 0x22 == 34 (matches the catalog).
    parsed = parse_app_id("M-0083_A-0040-22-FA09")
    assert parsed is not None
    assert parsed.application_number == 64
    assert parsed.version == 34


def test_manufacturer_case_normalised() -> None:
    parsed = parse_app_id("m-0083_A-0040-25-f9e1")
    assert parsed is not None
    assert parsed.manufacturer_id == "M-0083"
    assert parsed.hash == "F9E1"


def test_invalid_ids_return_none() -> None:
    assert parse_app_id("") is None
    assert parse_app_id("not-an-id") is None
    # Occurrence-suffixed ids are not plain application ids.
    assert parse_app_id("M-000C_A-7104-10-5844-O000A") is None


def test_same_application_across_versions() -> None:
    old = parse_app_id("M-0083_A-0040-25-F9E1")
    new = parse_app_id("M-0083_A-0040-26-652C")
    other = parse_app_id("M-0083_A-0041-25-1234")
    assert old is not None and new is not None and other is not None
    assert old.same_application(new)
    assert new.version > old.version
    assert not old.same_application(other)
