"""A module-based device's com-object instances must keep their identity across import/export.

For a module-based application, ``ComObjectInstanceRef/@RefId`` carries the module instance the
object belongs to (``MD-1_M-1_MI-2_O-2-0_R-0``). xknxproject's ``com_object_ref_id`` is the
application-program *definition* it resolves to, which is deliberately module-instance-stripped
(``..._MD-1_O-2-0_R-0``) and is therefore shared by every instance of the same module.

Storing only the definition collapses the instances onto one another: on a real Atios KNX bridge,
106 module com-objects on one device share just 7 definitions. Re-emitting that on export produces
an archive whose refs no longer resolve to a ModuleInstance.
"""

from __future__ import annotations

import zipfile
from pathlib import Path
from types import SimpleNamespace
from typing import cast
from xml.etree import ElementTree as ET

from sqlalchemy.orm import Session

from xknxeditor.proj.core.knxproj_export import export_knxproj
from xknxeditor.proj.core.knxproj_import import _build_com_object
from xknxeditor.proj.core.service import ProjectService
from xknxeditor.proj.db import make_engine, url_for
from xknxeditor.proj.models import ComObject, Device

_APP = "M-02DC_A-0000-10-DB14"


def _coir(ref_id: str, com_object_ref_id: str | None):
    """A stand-in for xknxproject's ComObjectInstanceRef (only the fields the builder reads)."""
    return SimpleNamespace(
        ref_id=ref_id,
        com_object_ref_id=com_object_ref_id,
        channel=None,
        read_flag=None,
        write_flag=None,
        communication_flag=None,
        transmit_flag=None,
        update_flag=None,
        read_on_init_flag=None,
    )


def test_import_keeps_the_module_instance_ref() -> None:
    """The stripped definition id is still stored in ref_id; the instance id must survive too."""
    row = _build_com_object(
        cast(
            "object",
            _coir("MD-1_M-1_MI-2_O-2-0_R-0", f"{_APP}_MD-1_O-2-0_R-0"),
        )  # type: ignore[arg-type]
    )
    assert row.ref_id == f"{_APP}_MD-1_O-2-0_R-0"  # definition, unchanged behaviour
    assert row.instance_ref_id == "MD-1_M-1_MI-2_O-2-0_R-0"  # instance, previously lost


def test_import_distinguishes_instances_that_share_a_definition() -> None:
    """Two instances of the same module resolve to one definition - they must stay distinct."""
    a = _build_com_object(
        cast("object", _coir("MD-1_M-1_MI-2_O-2-0_R-0", f"{_APP}_MD-1_O-2-0_R-0"))  # type: ignore[arg-type]
    )
    b = _build_com_object(
        cast("object", _coir("MD-1_M-1_MI-10_O-2-0_R-0", f"{_APP}_MD-1_O-2-0_R-0"))  # type: ignore[arg-type]
    )
    assert a.ref_id == b.ref_id  # the collapse that used to be all we stored
    assert a.instance_ref_id != b.instance_ref_id


def test_non_module_object_is_unaffected() -> None:
    row = _build_com_object(
        cast("object", _coir("O-3_R-4", f"{_APP}_O-3_R-4"))  # type: ignore[arg-type]
    )
    assert row.ref_id == f"{_APP}_O-3_R-4"
    assert row.instance_ref_id == "O-3_R-4"


def _export_com_object_refs(tmp_path: Path, rows: list[tuple[str, str]]) -> list[str]:
    """Build a one-device project carrying ``(ref_id, instance_ref_id)`` objects; return emitted RefIds."""
    src = tmp_path / "p.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-MOD")
    area_id = svc.create_area(pid, 0, 1, "Area 1")
    line_id = svc.create_line(pid, area_id, 1, "Line 1")
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
        "M-02DC_H-1-3_P-ADE",
        address=1,
        name="Bridge",
        hardware2program_ref_id="M-02DC_H-1-3_HP-0000-10-DB14",
    )
    svc.close(pid)

    with Session(make_engine(url_for(src))) as s:
        device = s.get(Device, device_id)
        assert device is not None
        for ref_id, instance_ref_id in rows:
            s.add(
                ComObject(
                    device_id=device.id,
                    ref_id=ref_id,
                    instance_ref_id=instance_ref_id,
                )
            )
        s.commit()

    out = tmp_path / "out.knxproj"
    export_knxproj(src, out)
    with zipfile.ZipFile(out) as z:
        name = next(n for n in z.namelist() if n.endswith("/0.xml"))
        root = ET.fromstring(z.read(name))
    return [
        el.get("RefId") or ""
        for el in root.iter()
        if el.tag.split("}")[-1] == "ComObjectInstanceRef"
    ]


def test_export_emits_the_module_qualified_ref(tmp_path: Path) -> None:
    """Each instance keeps its own RefId instead of collapsing onto the shared definition."""
    emitted = _export_com_object_refs(
        tmp_path,
        [
            (f"{_APP}_MD-1_O-2-0_R-0", "MD-1_M-1_MI-2_O-2-0_R-0"),
            (f"{_APP}_MD-1_O-2-0_R-0", "MD-1_M-1_MI-10_O-2-0_R-0"),
        ],
    )
    assert sorted(emitted) == [
        "MD-1_M-1_MI-10_O-2-0_R-0",
        "MD-1_M-1_MI-2_O-2-0_R-0",
    ]
    assert len(set(emitted)) == 2  # the collapse would have produced one distinct id


def test_export_falls_back_to_ref_id_without_an_instance_id(tmp_path: Path) -> None:
    """Objects created in the editor (not imported) carry no instance id; behaviour is unchanged."""
    emitted = _export_com_object_refs(tmp_path, [(f"{_APP}_O-3_R-4", "")])
    assert emitted == ["O-3_R-4"]
