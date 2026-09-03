"""Validate the exported ``.knxproj`` XML against the bundled KNX project XSD.

Catches structural regressions (missing required attributes, wrong types, invalid enums) without an
ETS round-trip — e.g. a function ``GroupAddressRef`` written without the schema-required ``Name`` /
``Puid`` used to pass our own re-import but crashed ETS. The schema is the ground truth for that
class of bug; this exercises every write path (topology, group addresses, group-range folders,
building spaces, functions) in one project.
"""

import zipfile
from pathlib import Path

import xmlschema

import xknxmono.models
from xknxmono.project import ProjectService, export_knxproj

_SCHEMAS = Path(xknxmono.models.__file__).parent / "schemas"


def _comprehensive_project(path: Path) -> str:
    svc = ProjectService()
    pid = svc.create(path, "P-SCHEMA")
    area = svc.create_area(pid, 0, 1, "Area 1")
    line = svc.create_line(pid, area, 1, "Line 1")
    segment = next(
        ln.segments[0].id
        for a in svc.topology(pid, 0).areas
        if a.id == area
        for ln in a.lines
        if ln.id == line
    )
    device = svc.add_device(
        pid,
        segment,
        "M-1_H-1_P-1",
        address=5,
        name="Dev",
        hardware2program_ref_id="M-1_H-1_HP-1",
        com_objects=[("M-1_A-1_O-1_R-1", None)],
    )
    ga = svc.create_group_address(pid, 0, 0x0801, "GA One")
    svc.set_group_address_datapoint_type(pid, ga, "DPST-1-1")
    co = next(c.id for d in svc.devices(pid) if d.id == device for c in d.com_objects)
    svc.link_com_object(pid, co, ga, sending=True)
    # group-range folders (main + middle), building spaces, device placement, and a function
    main = svc.create_group_range(pid, 0, None, "Beleuchtung")
    svc.create_group_range(pid, 0, main, "EG")
    building = svc.create_space(pid, 0, "Building", "Haus")
    room = svc.create_space(pid, 0, "Room", "Wohnzimmer", building)
    svc.set_device_space(pid, device, room)
    fn = svc.create_function(pid, room, "FT-1", "Licht")
    svc.add_function_group_address(pid, fn, ga, role="Switch")
    svc.close(pid)
    return pid


def _schema_errors(out: Path, xsd: str) -> dict[str, list[str]]:
    schema = xmlschema.XMLSchema(str(_SCHEMAS / xsd))
    errors: dict[str, list[str]] = {}
    with zipfile.ZipFile(out) as zf:
        for name in zf.namelist():
            if name.endswith("project.xml") or name.endswith("/0.xml"):
                xml = zf.read(name).decode("utf-8")
                errors[name] = [
                    f"{getattr(e, 'path', '?')}: {getattr(e, 'reason', '') or e}"
                    for e in schema.iter_errors(xml)
                ]
    return errors


def test_export_is_schema_valid_v20(tmp_path: Path) -> None:
    src = tmp_path / "p.xknx"
    _comprehensive_project(src)
    out = tmp_path / "p.knxproj"
    export_knxproj(src, out, schema="20")
    errors = _schema_errors(out, "knx_project_v20.xsd")
    assert errors, "expected project.xml and 0.xml to be present"
    for name, errs in errors.items():
        assert not errs, f"{name} violates knx_project_v20.xsd:\n" + "\n".join(errs)


def test_export_is_schema_valid_v23(tmp_path: Path) -> None:
    src = tmp_path / "p.xknx"
    _comprehensive_project(src)
    out = tmp_path / "p.knxproj"
    export_knxproj(src, out, schema="23")
    for name, errs in _schema_errors(out, "knx_project_v23.xsd").items():
        assert not errs, f"{name} violates knx_project_v23.xsd:\n" + "\n".join(errs)
