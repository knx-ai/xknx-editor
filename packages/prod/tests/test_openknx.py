"""Wrapping OpenKNX / monolithic KNX product XML into an importable in-memory .knxprod.

OpenKNX ships apps as a monolithic ``<KNX>`` product XML (raw or in a release ZIP) with no
``.knxprod`` and no signature. These helpers wrap it into the standard package our loader consumes.
"""

from __future__ import annotations

import io
import zipfile

import pytest

from xknxeditor.prod.errors import ArchiveError
from xknxeditor.prod.openknx import (
    knxprod_from_source,
    monolithic_to_knxprod,
    openknx_release_to_knxprod,
)

# A minimal monolithic product XML in the shape OpenKNXproducer emits (Catalog + ApplicationPrograms
# + Hardware under one Manufacturer, no <MasterData>).
_MONOLITHIC = b"""<?xml version="1.0" encoding="utf-8"?>
<KNX xmlns="http://knx.org/xml/project/20" CreatedBy="OpenKNXproducer">
  <ManufacturerData>
    <Manufacturer RefId="M-00FA">
      <Catalog>
        <CatalogSection Id="M-00FA_CS-OpenKNX" Name="OpenKNX" Number="OpenKNX"/>
      </Catalog>
      <ApplicationPrograms>
        <ApplicationProgram Id="M-00FA_A-A002-36-0000" Name="Demo" MaskVersion="MV-07B0"/>
      </ApplicationPrograms>
      <Hardware>
        <Hardware Id="M-00FA_H-demo-1" Name="Demo HW"/>
      </Hardware>
    </Manufacturer>
  </ManufacturerData>
</KNX>
"""
_MASTER = b"<KNX><MasterData/></KNX>"


def _entries(knxprod: bytes) -> dict[str, bytes]:
    with zipfile.ZipFile(io.BytesIO(knxprod)) as zf:
        return {n: zf.read(n) for n in zf.namelist()}


def test_monolithic_wrap_builds_standard_package():
    files = _entries(monolithic_to_knxprod(_MONOLITHIC, _MASTER))
    assert files["knx_master.xml"] == _MASTER
    assert set(files) == {
        "knx_master.xml",
        "M-00FA/Catalog.xml",
        "M-00FA/Hardware.xml",
        "M-00FA/M-00FA_A-A002-36-0000.xml",
    }
    # The application file keeps the programs; Catalog/Hardware copies have them sliced out.
    assert b"<ApplicationProgram " in files["M-00FA/M-00FA_A-A002-36-0000.xml"]
    assert b"<ApplicationProgram " not in files["M-00FA/Catalog.xml"]
    assert b"<Catalog>" in files["M-00FA/Catalog.xml"]  # section still present


def test_monolithic_wrap_rejects_non_product_xml():
    with pytest.raises(ArchiveError):
        monolithic_to_knxprod(b"<KNX></KNX>", _MASTER)


def test_release_zip_wrap():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        # OpenKNX release layout (Windows tool -> backslash separators).
        zf.writestr(
            "data\\content.xml",
            b'<Content><ETSapp Name="Demo" XmlFile="Demo.xml"/></Content>',
        )
        zf.writestr("data\\Demo.xml", _MONOLITHIC)
        zf.writestr("firmware.uf2", b"\x00\x01")
    files = _entries(openknx_release_to_knxprod(buf.getvalue(), _MASTER))
    assert "M-00FA/M-00FA_A-A002-36-0000.xml" in files


def test_source_sniffing():
    # 1) A real .knxprod (has knx_master.xml) is returned unchanged.
    real = monolithic_to_knxprod(_MONOLITHIC, _MASTER)
    assert knxprod_from_source(real, _MASTER) == real
    # 2) A raw monolithic XML is wrapped.
    assert "knx_master.xml" in _entries(knxprod_from_source(_MONOLITHIC, _MASTER))
    # 3) An OpenKNX release ZIP is wrapped.
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(
            "data/content.xml", b'<Content><ETSapp XmlFile="Demo.xml"/></Content>'
        )
        zf.writestr("data/Demo.xml", _MONOLITHIC)
    assert "knx_master.xml" in _entries(knxprod_from_source(buf.getvalue(), _MASTER))
    # 4) Garbage is rejected.
    with pytest.raises(ArchiveError):
        knxprod_from_source(b"not a product", _MASTER)
