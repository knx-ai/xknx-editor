"""Regression tests for two round-trip bugs a Codex review flagged in the coupler / additional-address
handling.

1. Undo of a device removal must restore the device's ``DeviceAdditionalAddress`` rows. The snapshot
   walks every cascade-owned child, so the restore-model registry must cover them; a stale registry
   raised ``KeyError`` on undo.
2. ``AdditionalAddresses/Address/@Address`` is optional in project/22+23 but required in project/14+20.
   An address-less entry (only expressible in 22/23) must be dropped when exporting to an older schema
   rather than emitted attribute-less, which would be schema-invalid.
"""

from __future__ import annotations

import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from sqlalchemy.orm import Session

from xknxeditor.proj import ProjectService, export_knxproj
from xknxeditor.proj.db import make_engine, url_for
from xknxeditor.proj.models import Device, DeviceAdditionalAddress


def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _read_zero_from_knxproj(knxproj: Path) -> bytes:
    with zipfile.ZipFile(knxproj) as zf:
        name = next(n for n in zf.namelist() if n.endswith("/0.xml"))
        return zf.read(name)


def _device_with_addresses(tmp_path: Path) -> tuple[Path, int]:
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-ADDR")
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
    svc.close(pid)
    return src, device_id


def test_undo_remove_device_restores_additional_addresses(tmp_path: Path) -> None:
    src, device_id = _device_with_addresses(tmp_path)
    with Session(make_engine(url_for(src))) as s:
        device = s.get(Device, device_id)
        assert device is not None
        device.additional_addresses.append(
            DeviceAdditionalAddress(address=200, name="tunnel-1")
        )
        s.commit()

    svc = ProjectService()
    pid = svc.open(src)
    svc.remove_device(pid, device_id)
    svc.undo(
        pid
    )  # must not raise KeyError on the cascade-owned DeviceAdditionalAddress
    svc.close(pid)

    with Session(make_engine(url_for(src))) as s:
        device = s.get(Device, device_id)
        assert device is not None
        assert [(a.address, a.name) for a in device.additional_addresses] == [
            (200, "tunnel-1")
        ]


def _addresses_in(root: ET.Element) -> list[ET.Element]:
    return [e for e in root.iter() if _localname(e.tag) == "Address"]


def test_addressless_additional_address_dropped_for_project_20(tmp_path: Path) -> None:
    src, device_id = _device_with_addresses(tmp_path)
    with Session(make_engine(url_for(src))) as s:
        device = s.get(Device, device_id)
        assert device is not None
        # An address-less reserved entry, valid only in project/22+23.
        device.additional_addresses.append(
            DeviceAdditionalAddress(address=None, name="reserved")
        )
        device.additional_addresses.append(
            DeviceAdditionalAddress(address=201, name="tunnel-2")
        )
        s.commit()

    out20 = tmp_path / "out20.knxproj"
    export_knxproj(src, out20, schema="20")
    addrs20 = _addresses_in(ET.fromstring(_read_zero_from_knxproj(out20)))
    # The address-less entry is dropped; only the real one survives (schema-valid).
    assert [a.get("Address") for a in addrs20] == ["201"]

    out23 = tmp_path / "out23.knxproj"
    export_knxproj(src, out23, schema="23")
    addrs23 = _addresses_in(ET.fromstring(_read_zero_from_knxproj(out23)))
    # project/23 allows an optional Address, so the reserved entry is preserved.
    names23 = [a.get("Name") for a in addrs23]
    assert "reserved" in names23
    assert "tunnel-2" in names23
