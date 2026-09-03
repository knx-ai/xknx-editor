from __future__ import annotations

import pytest

from xknxmono.models import VersionError, detect_version, load_xml, serialize_xml
from xknxmono.models.files import v23

MINIMAL_KNX_XML = b"""\
<?xml version="1.0" encoding="utf-8"?>
<KNX xmlns="http://knx.org/xml/project/23">
</KNX>
"""


def test_detect_version():
    version = detect_version(MINIMAL_KNX_XML)
    assert version == "23"


def test_detect_version_error():
    with pytest.raises(VersionError):
        detect_version(b"<Invalid/>")


def test_load_xml_auto_version():
    result = load_xml(MINIMAL_KNX_XML)
    assert isinstance(result, v23.Knx)


def test_load_xml_explicit_version():
    result = load_xml(MINIMAL_KNX_XML, version="23")
    assert isinstance(result, v23.Knx)


def test_serialize_xml():
    obj = v23.Knx()
    result = serialize_xml(obj, "23")
    assert b"<KNX" in result or b"<Knx" in result
    assert b'xmlns="http://knx.org/xml/project/23"' in result


def test_roundtrip():
    original = load_xml(MINIMAL_KNX_XML)
    serialized = serialize_xml(original, "23")
    restored = load_xml(serialized, "23")
    assert type(restored) is type(original)
