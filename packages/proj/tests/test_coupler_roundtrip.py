"""Coupler routing data must survive a full import -> export -> re-read cycle.

The importer reads four things straight from the raw project XML because ``xknxproject`` does not
surface them: a line's ``AdditionalGroupAddresses`` pass-through (on the ``Segment`` from
project/22+23, on the ``Line`` in 14+20), the ``Unfiltered`` flag on group addresses and whole
ranges, and a DeviceInstance's extra individual addresses (``AdditionalAddresses``). Dropping any of
them silently changes how a line/backbone coupler routes, so they are captured on import and
re-emitted on export.
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from sqlalchemy.orm import Session

from xknxeditor.proj import ProjectService, export_knxproj
from xknxeditor.proj.core import knxproj_import
from xknxeditor.proj.db import make_engine, url_for
from xknxeditor.proj.models import Device, DeviceAdditionalAddress, GroupAddress, Line


def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


class _FakeContents:
    """Duck-types the ``open_project_0`` that the raw-XML readers use."""

    def __init__(self, zero_xml: bytes) -> None:
        self._zero = zero_xml

    def open_project_0(self) -> io.BytesIO:
        return io.BytesIO(self._zero)


def _zero_xml(installation_body: str) -> bytes:
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<KNX xmlns="http://knx.org/xml/project/23">'
        "<Project><Installations><Installation>"
        f"{installation_body}"
        "</Installation></Installations></Project></KNX>"
    ).encode()


def _read_zero_from_knxproj(knxproj: Path) -> bytes:
    with zipfile.ZipFile(knxproj) as zf:
        name = next(n for n in zf.namelist() if n.endswith("/0.xml"))
        return zf.read(name)


# --- raw-XML parsing (import side) ----------------------------------------


def test_reads_pass_through_from_segment_and_line() -> None:
    """AdditionalGroupAddresses are collected whether they sit on the Segment (project/22+23) or
    directly on the Line (project/14+20); both fold into the same per-line pass-through set."""
    body = (
        "<Topology>"
        '<Area Address="1"><Line Address="2">'
        '<Segment Number="0" MediumTypeRefId="MT-0">'
        '<AdditionalGroupAddresses><GroupAddress Address="2049"/>'
        '<GroupAddress Address="2050"/></AdditionalGroupAddresses>'
        "</Segment></Line></Area>"
        '<Area Address="1"><Line Address="3">'
        '<AdditionalGroupAddresses><GroupAddress Address="3072"/></AdditionalGroupAddresses>'
        "</Line></Area>"
        "</Topology>"
    )
    extras = knxproj_import._read_device_extras(_FakeContents(_zero_xml(body)))

    assert extras.line_pass_through[(1, 2)] == [2049, 2050]
    assert extras.line_pass_through[(1, 3)] == [3072]


def test_reads_unfiltered_flags_and_additional_addresses() -> None:
    body = (
        "<Topology><Area Address='1'><Line Address='1'><Segment Number='0' "
        "MediumTypeRefId='MT-0'>"
        '<DeviceInstance Id="P-1-0_DI-1" Address="1">'
        '<AdditionalAddresses><Address Address="200" Name="tunnel-1"/>'
        '<Address Address="201" Name="tunnel-2" Comment="c"/></AdditionalAddresses>'
        "</DeviceInstance></Segment></Line></Area></Topology>"
        "<GroupAddresses><GroupRanges>"
        '<GroupRange RangeStart="1" RangeEnd="2047" Name="Main" Unfiltered="true">'
        '<GroupAddress Address="1" Name="flagged" Unfiltered="true"/>'
        '<GroupAddress Address="2" Name="plain"/>'
        "</GroupRange></GroupRanges></GroupAddresses>"
    )
    extras = knxproj_import._read_device_extras(_FakeContents(_zero_xml(body)))

    assert extras.unfiltered_ga == {1}
    assert extras.unfiltered_ranges == {(1, 2047)}
    entries = extras.additional_addresses["P-1-0_DI-1"]
    assert [(e.address, e.name, e.comment) for e in entries] == [
        (200, "tunnel-1", ""),
        (201, "tunnel-2", "c"),
    ]


# --- export placement + export -> re-read round-trip ----------------------


def _project_with_coupler_data(tmp_path: Path) -> Path:
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-CPL")
    area_id = svc.create_area(pid, 0, 2, "Area 1")
    line_id = svc.create_line(pid, area_id, 2, "Line 2")
    segment_id = next(
        line.segments[0].id
        for area in svc.topology(pid, 0).areas
        if area.id == area_id
        for line in area.lines
        if line.id == line_id
    )
    device_id = svc.add_device(
        pid,
        segment_id,
        "M-1_H-1_P-1",
        address=0,
        name="Coupler",
        hardware2program_ref_id="M-1_H-1_HP-1",
    )
    ga_id = svc.create_group_address(pid, 0, 0x0802, "flagged")
    svc.close(pid)

    with Session(make_engine(url_for(src))) as s:
        line = s.get(Line, line_id)
        assert line is not None
        line.additional_group_addresses = "2049,2050"
        ga = s.get(GroupAddress, ga_id)
        assert ga is not None
        ga.unfiltered = True
        device = s.get(Device, device_id)
        assert device is not None
        device.additional_addresses.append(
            DeviceAdditionalAddress(address=200, name="tunnel-1")
        )
        s.commit()
    return src


def _pass_through_container(root: ET.Element) -> str:
    """Local tag name of the element carrying ``AdditionalGroupAddresses`` (``Segment`` or ``Line``),
    searched across every line (the seeded default line has none)."""
    for line in root.iter():
        if _localname(line.tag) != "Line":
            continue
        for child in line:
            if _localname(child.tag) == "AdditionalGroupAddresses":
                return "Line"
            if _localname(child.tag) == "Segment":
                for seg_child in child:
                    if _localname(seg_child.tag) == "AdditionalGroupAddresses":
                        return "Segment"
    return ""


def test_export_places_pass_through_on_segment_for_project_23(tmp_path: Path) -> None:
    src = _project_with_coupler_data(tmp_path)
    out = tmp_path / "out.knxproj"
    export_knxproj(src, out, schema="23")  # project/23 nests devices under a Segment

    root = ET.fromstring(_read_zero_from_knxproj(out))
    assert _pass_through_container(root) == "Segment"


def test_export_places_pass_through_on_line_for_project_20(tmp_path: Path) -> None:
    src = _project_with_coupler_data(tmp_path)
    out = tmp_path / "out.knxproj"
    export_knxproj(src, out, schema="20")  # project/20 has no segments

    root = ET.fromstring(_read_zero_from_knxproj(out))
    assert _pass_through_container(root) == "Line"


def test_export_then_reread_preserves_all_coupler_data(tmp_path: Path) -> None:
    src = _project_with_coupler_data(tmp_path)
    out = tmp_path / "out.knxproj"
    export_knxproj(src, out)

    extras = knxproj_import._read_device_extras(
        _FakeContents(_read_zero_from_knxproj(out))
    )
    assert extras.line_pass_through[(2, 2)] == [2049, 2050]
    assert extras.unfiltered_ga == {0x0802}
    ((device_id, entries),) = extras.additional_addresses.items()
    assert device_id.endswith("_DI-1") or "_DI-" in device_id
    assert [(e.address, e.name) for e in entries] == [(200, "tunnel-1")]
