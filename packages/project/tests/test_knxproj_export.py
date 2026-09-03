"""Round-trip test for the simple .knxproj export: build a project via the core API, export it to
a ``.knxproj``, then re-import it (real xknxproject parse) and check topology/GAs/links survive."""

import re
import zipfile
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from xknxmono.project import ProjectService, export_knxproj, import_knxproj
from xknxmono.project.db import make_engine, url_for
from xknxmono.project.models import (
    Device,
    Function,
    FunctionGroupAddress,
    GroupAddress,
    Line,
    Space,
)


def test_export_import_round_trip(tmp_path: Path) -> None:
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-RT")

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
        "M-1_H-1_P-1",
        address=5,
        name="Dev",
        hardware2program_ref_id="M-1_H-1_HP-1",
        com_objects=[("M-1_A-1_O-1_R-1", None)],
    )
    ga_id = svc.create_group_address(pid, 0, 0x0801, "GA One")  # 1/0/1
    svc.set_group_address_datapoint_type(pid, ga_id, "DPST-1-1")
    co_id = next(
        co.id for d in svc.devices(pid) if d.id == device_id for co in d.com_objects
    )
    svc.link_com_object(pid, co_id, ga_id, sending=True)

    # Build a location tree via the public API so the export's Locations round-trip is covered:
    # a room holding the device and a function referencing the group address.
    room_id = svc.create_space(pid, 0, "Room", "Room 1")
    svc.set_device_space(pid, device_id, room_id)
    fn_id = svc.create_function(pid, room_id, "FT-1", "Light")
    svc.add_function_group_address(pid, fn_id, ga_id, role="role")
    svc.close(pid)

    out = tmp_path / "out.knxproj"
    export_knxproj(src, out)
    assert out.exists() and out.stat().st_size > 0

    round_path = tmp_path / "round.xknx"
    rpid = import_knxproj(out, round_path)
    rsvc = ProjectService()
    rsvc.open(round_path)

    inst = rsvc.topology(rpid, 0)
    addresses = {a.address for a in inst.areas}
    assert 1 in addresses  # our Area 1 survived (Area 0 backbone also present)
    gas = {g.text: g for g in rsvc.group_addresses(rpid)}
    assert "1/0/1" in gas
    assert gas["1/0/1"].name == "GA One"
    assert gas["1/0/1"].datapoint_type == "DPST-1-1"
    # the device and its sending link survived
    devices = rsvc.devices(rpid)
    assert any(d.product_ref_id == "M-1_H-1_P-1" for d in devices)
    links = rsvc.group_address_links(rpid, gas["1/0/1"].id)
    assert len(links) == 1
    assert links[0].is_sending

    # the location tree (space + its device + function) survived
    with Session(make_engine(url_for(round_path))) as session:
        rooms = session.query(Space).filter(Space.name == "Room 1").all()
        assert len(rooms) == 1
        assert session.query(Device).filter(Device.space_id == rooms[0].id).count() == 1
        funcs = session.query(Function).filter(Function.space_id == rooms[0].id).all()
        assert len(funcs) == 1
        assert funcs[0].name == "Light"
        assert (
            session.query(FunctionGroupAddress)
            .filter(FunctionGroupAddress.function_id == funcs[0].id)
            .count()
            == 1
        )


def test_export_keeps_unlinked_com_objects(tmp_path: Path) -> None:
    """An instantiated but UNLINKED com-object (e.g. a channel a function activated but that the user
    has not wired to a group address yet) must survive export/re-import — not only linked ones."""
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-UL")
    seg = svc.create_line(pid, svc.create_area(pid, 0, 1, "A"), 1, "L")
    segment_id = next(
        line.segments[0].id
        for area in svc.topology(pid, 0).areas
        for line in area.lines
        if line.id == seg
    )
    device_id = svc.add_device(
        pid,
        segment_id,
        "M-1_H-1_P-1",
        address=5,
        name="Dev",
        hardware2program_ref_id="M-1_H-1_HP-1",
        com_objects=[("M-1_A-1_O-1_R-1", None), ("M-1_A-1_O-2_R-1", None)],
    )
    ga_id = svc.create_group_address(pid, 0, 0x0801, "GA")
    co1 = next(
        co.id
        for d in svc.devices(pid)
        if d.id == device_id
        for co in d.com_objects
        if co.ref_id == "M-1_A-1_O-1_R-1"
    )
    svc.link_com_object(pid, co1, ga_id, sending=True)  # O-1 linked, O-2 left unlinked
    svc.close(pid)

    out = tmp_path / "out.knxproj"
    export_knxproj(src, out)

    # Inspect the exported 0.xml directly (a fake product can't be re-resolved by xknxproject):
    # both objects must be emitted, and only the linked one carries a Links attribute.
    with zipfile.ZipFile(out) as zf:
        zero = next(n for n in zf.namelist() if n.endswith("/0.xml"))
        xml = zf.read(zero).decode("utf-8")
    refs = re.findall(r"<(?:\w+:)?ComObjectInstanceRef\b[^>]*>", xml)
    joined = "\n".join(refs)
    assert (
        "O-1_R-1" in joined and "O-2_R-1" in joined
    )  # both instantiated objects emitted
    o2 = next(r for r in refs if "O-2_R-1" in r)
    assert (
        "Links=" not in o2
    )  # the unlinked object is emitted without a Links attribute
    o1 = next(r for r in refs if "O-1_R-1" in r)
    assert "Links=" in o1  # the linked object keeps its link


def test_export_emits_com_object_flag_overrides(tmp_path: Path) -> None:
    """A com-object flag override (e.g. forcing write_flag) must be emitted so it survives export;
    objects with default (None) flags emit no flag attribute (inherit the application default)."""
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-FL")
    seg = svc.create_line(pid, svc.create_area(pid, 0, 1, "A"), 1, "L")
    segment_id = next(
        line.segments[0].id
        for area in svc.topology(pid, 0).areas
        for line in area.lines
        if line.id == seg
    )
    device_id = svc.add_device(
        pid,
        segment_id,
        "M-1_H-1_P-1",
        address=5,
        name="Dev",
        hardware2program_ref_id="M-1_H-1_HP-1",
        com_objects=[("M-1_A-1_O-1_R-1", None), ("M-1_A-1_O-2_R-1", None)],
    )
    co1 = next(
        co.id
        for d in svc.devices(pid)
        if d.id == device_id
        for co in d.com_objects
        if co.ref_id == "M-1_A-1_O-1_R-1"
    )
    svc.set_com_object_flag(pid, co1, "write_flag", True)  # O-1: override write; O-2: no overrides
    svc.close(pid)

    out = tmp_path / "out.knxproj"
    export_knxproj(src, out)
    with zipfile.ZipFile(out) as zf:
        zero = next(n for n in zf.namelist() if n.endswith("/0.xml"))
        xml = zf.read(zero).decode("utf-8")
    refs = re.findall(r"<(?:\w+:)?ComObjectInstanceRef\b[^>]*>", xml)
    o1 = next(r for r in refs if "O-1_R-1" in r)
    o2 = next(r for r in refs if "O-2_R-1" in r)
    assert 'WriteFlag="Enabled"' in o1  # the override is emitted
    assert "Flag=" not in o2  # untouched object emits no flag attribute (inherits default)


def test_commissioning_state_round_trip(tmp_path: Path) -> None:
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-CS")
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
        "M-1_H-1_P-1",
        address=5,
        name="Dev",
        hardware2program_ref_id="M-1_H-1_HP-1",
    )
    svc.set_device_commissioning(
        pid,
        device_id,
        serial_number="ABC12345",
        last_download="2024-01-02T03:04:05.0Z",
        individual_address_loaded=True,
        application_program_loaded=True,
        parameters_loaded=True,
    )
    svc.close(pid)

    out = tmp_path / "out.knxproj"
    export_knxproj(src, out)
    round_path = tmp_path / "round.xknx"
    rpid = import_knxproj(out, round_path)
    rsvc = ProjectService()
    rsvc.open(round_path)

    dev = next(d for d in rsvc.devices(rpid) if d.product_ref_id == "M-1_H-1_P-1")
    assert dev.serial_number == "ABC12345"
    assert dev.last_download == "2024-01-02T03:04:05.0Z"
    assert dev.individual_address_loaded is True
    assert dev.application_program_loaded is True
    assert dev.parameters_loaded is True
    # flags left unset stay False (absent attribute -> not loaded)
    assert dev.communication_part_loaded is False
    assert dev.medium_config_loaded is False


def test_commissioning_set_is_undoable(tmp_path: Path) -> None:
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-CSU")
    seg = svc.topology(pid, 0).areas[0].lines[0].segments[0].id
    device_id = svc.add_device(pid, seg, "M-1_H-1_P-1", address=1, name="Dev")
    svc.set_device_commissioning(pid, device_id, parameters_loaded=True)
    assert svc.device(pid, device_id).parameters_loaded is True
    svc.undo(pid)
    assert svc.device(pid, device_id).parameters_loaded is False


def test_export_emits_unfiltered_and_additional_group_addresses(tmp_path: Path) -> None:
    # KNX PR #651 project-side fields: GroupAddress/GroupRange "Unfiltered" and the line's coupler
    # "AdditionalGroupAddresses". We prepare storage + export; set them directly (no UI yet) and
    # assert the exported installation XML carries them.
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-651")
    area_id = svc.create_area(pid, 0, 1, "Area 1")
    line_id = svc.create_line(pid, area_id, 1, "Line 1")
    ga_id = svc.create_group_address(pid, 0, 0x0801, "GA One")  # 1/0/1
    svc.close(pid)

    with Session(make_engine(url_for(src))) as s:
        s.get(GroupAddress, ga_id).unfiltered = True  # type: ignore[union-attr]
        s.get(Line, line_id).additional_group_addresses = "2049,2050"  # type: ignore[union-attr]
        s.commit()

    out = tmp_path / "out.knxproj"
    export_knxproj(src, out)
    with zipfile.ZipFile(out) as z:
        zero = next(
            z.read(n).decode("utf-8") for n in z.namelist() if n.endswith("/0.xml")
        )
    assert 'Unfiltered="true"' in zero
    assert "<AdditionalGroupAddresses" in zero
    assert 'Address="2049"' in zero and 'Address="2050"' in zero


def test_export_bundles_extra_files_and_master(tmp_path: Path) -> None:
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-MFR")
    svc.close(pid)

    out = tmp_path / "out.knxproj"
    master = b'<?xml version="1.0"?>\n<KNX><MasterData Merged="1"/></KNX>'
    hardware = b"<Hardware/>"
    export_knxproj(
        src,
        out,
        extra_files={
            "M-9999/Hardware.xml": hardware,
            "M-9999.signature": b"sig",
            # colliding with an own path must be ignored, not overwrite our master
            "knx_master.xml": b"IGNORED",
        },
        master_xml=master,
    )

    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
        assert "M-9999/Hardware.xml" in names
        assert "M-9999.signature" in names
        assert zf.read("M-9999/Hardware.xml") == hardware
        # the colliding "knx_master.xml" key is ignored: only our master, written once
        assert names.count("knx_master.xml") == 1
        assert zf.read("knx_master.xml") == master


def test_certificate_signer_embeds_certificate(tmp_path: Path) -> None:
    """A certificate_signer is called with the folder signature and its output is embedded."""
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-CERT")
    svc.close(pid)

    seen: dict[str, object] = {}

    def signer(pid_arg: str, folder_signature: bytes, project_name: str) -> bytes:
        seen["pid"] = pid_arg
        seen["sig"] = folder_signature
        seen["name"] = project_name
        return b'CERT KNX:"P-CERT.certificate"\n\tSIGN=DEADBEEF\n'

    out = tmp_path / "out.knxproj"
    export_knxproj(src, out, certificate_signer=signer)

    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
        assert f"{pid}.certificate" in names
        assert zf.read(f"{pid}.certificate").startswith(b"CERT KNX:")
        # the signer receives the raw base64 folder signature, exactly what the .signature file
        # holds (ETS writes it with no BOM)
        assert seen["pid"] == pid
        assert seen["sig"] == zf.read(f"{pid}.signature")
        assert not zf.read(f"{pid}.signature").startswith(b"\xef\xbb\xbf")
        assert seen["name"] == "New project"


def test_certificate_signer_returning_none_skips_certificate(tmp_path: Path) -> None:
    """A signer returning None (e.g. no license) leaves the archive without a certificate."""
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-NOCERT")
    svc.close(pid)

    out = tmp_path / "out.knxproj"
    export_knxproj(src, out, certificate_signer=lambda *_: None)

    with zipfile.ZipFile(out) as zf:
        assert f"{pid}.certificate" not in zf.namelist()


def test_generated_master_carries_id_version_and_empty_signature(
    tmp_path: Path,
) -> None:
    """The generated ``knx_master.xml`` must carry the ``MasterData`` id/version that ETS
    expects and an empty (to-be-signed) signature. This is what makes the export a valid
    input for an external master-data signer.
    """
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-MASTER")
    svc.close(pid)

    out = tmp_path / "out.knxproj"
    export_knxproj(src, out, master_version=224)

    with zipfile.ZipFile(out) as zf:
        master = zf.read("knx_master.xml").decode("utf-8")
    m = re.search(r"<MasterData\b[^>]*>", master)
    assert m is not None
    el = m.group(0)
    assert 'Id="MD-1"' in el
    assert 'Version="224"' in el
    assert 'Signature=""' in el


def test_master_source_reuses_signed_master_offline(tmp_path: Path) -> None:
    """Passing ``master_source`` reuses that archive's signed ``knx_master.xml`` verbatim (no
    network), so the exported master keeps its valid signature.
    """
    # Build a stand-in signed source archive (project/20 namespace, signed MasterData attr).
    signed_master = (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<KNX xmlns="http://knx.org/xml/project/20">'
        b'<MasterData Id="MD-1" Version="521" Signature="QUJD"/></KNX>'
    )
    source = tmp_path / "signed.knxproj"
    with zipfile.ZipFile(source, "w") as zf:
        zf.writestr("knx_master.xml", signed_master)

    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-REUSE")
    svc.close(pid)

    out = tmp_path / "out.knxproj"
    export_knxproj(src, out, master_source=source)

    with zipfile.ZipFile(out) as zf:
        assert zf.read("knx_master.xml") == signed_master


def test_export_schema14_namespace_and_round_trip(tmp_path: Path) -> None:
    """A schema='14' export uses the project/14 namespace and still re-imports (ETS5 shape)."""
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-E5")
    area_id = svc.create_area(pid, 0, 1, "Area 1")
    line_id = svc.create_line(pid, area_id, 1, "Line 1")
    segment_id = next(
        line.segments[0].id
        for area in svc.topology(pid, 0).areas
        if area.id == area_id
        for line in area.lines
        if line.id == line_id
    )
    svc.add_device(
        pid,
        segment_id,
        "M-1_H-1_P-1",
        address=5,
        name="Dev",
        hardware2program_ref_id="M-1_H-1_HP-1",
        com_objects=[("M-1_A-1_O-1_R-1", None)],
    )
    ga_id = svc.create_group_address(pid, 0, 0x0801, "GA One")  # 1/0/1
    svc.set_group_address_datapoint_type(pid, ga_id, "DPST-1-1")
    svc.close(pid)

    out = tmp_path / "out5.knxproj"
    export_knxproj(src, out, schema="14")

    with zipfile.ZipFile(out) as zf:
        project_xml = zf.read("P-E5/project.xml").decode("utf-8")
        master_xml = zf.read("knx_master.xml").decode("utf-8")
    assert "http://knx.org/xml/project/14" in project_xml
    assert "http://knx.org/xml/project/20" not in project_xml
    assert "http://knx.org/xml/project/14" in master_xml

    # xknxproject reads the ETS5-shaped archive back.
    round_path = tmp_path / "round5.xknx"
    rpid = import_knxproj(out, round_path)
    rsvc = ProjectService()
    rsvc.open(round_path)
    gas = {g.text: g for g in rsvc.group_addresses(rpid)}
    assert "1/0/1" in gas
    assert gas["1/0/1"].name == "GA One"


def test_export_rejects_unknown_schema(tmp_path: Path) -> None:
    import pytest

    src = tmp_path / "src.xknx"
    svc = ProjectService()
    svc.create(src, "P-BAD")
    svc.close("P-BAD")
    with pytest.raises(ValueError, match="unsupported export schema"):
        export_knxproj(src, tmp_path / "x.knxproj", schema="99")


def _mini_project(tmp_path: Path, pid: str) -> Path:
    src = tmp_path / f"{pid}.xknx"
    svc = ProjectService()
    svc.create(src, pid)
    ga = svc.create_group_address(pid, 0, 0x0801, "GA One")
    svc.set_group_address_datapoint_type(pid, ga, "DPST-1-1")
    svc.close(pid)
    return src


def test_export_carries_tool_identity_per_schema(tmp_path: Path) -> None:
    """ETS 5 -> project/20 CreatedBy=ETS5; ETS 6 -> project/22 CreatedBy=ETS6; both re-import."""
    for schema, ns, tool in (
        ("20", "project/20", "ETS5"),
        ("23", "project/23", "ETS6"),
    ):
        src = _mini_project(tmp_path, f"P-T{schema}")
        out = tmp_path / f"out{schema}.knxproj"
        export_knxproj(src, out, schema=schema)
        with zipfile.ZipFile(out) as zf:
            root = zf.read(f"P-T{schema}/project.xml").decode("utf-8")
        assert f"http://knx.org/xml/{ns}" in root
        assert f'CreatedBy="{tool}"' in root
        assert 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' in root
        # xknxproject reads it back.
        round_path = tmp_path / f"round{schema}.xknx"
        rpid = import_knxproj(out, round_path)
        rsvc = ProjectService()
        rsvc.open(round_path)
        assert "1/0/1" in {g.text for g in rsvc.group_addresses(rpid)}


def test_relidref_strips_application_parent() -> None:
    """ComObjectInstanceRef RefId must be the RELIDREF form ETS resolves (O-n_R-m), not the full id.

    Emitting the full id makes ETS unable to link the com-object to the app and it drops the whole
    device on import (the bug behind "project imports but has no devices").
    """
    from xknxmono.project.core.knxproj_export import _relidref

    assert _relidref("M-0083_A-003A-24-BB4E_O-120_R-538") == "O-120_R-538"
    assert _relidref("M-0002_A-A061-14-F8BA_O-0_R-3") == "O-0_R-3"
    assert _relidref("O-7_R-9") == "O-7_R-9"  # already relative -> unchanged


def test_export_rejects_mismatched_manufacturer_schema(tmp_path: Path) -> None:
    """A project/23 export with project/20 manufacturer data (or mixed data) is rejected up front,
    instead of writing an archive ETS refuses with 'Invalid import data'."""
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-MIX")
    svc.close(pid)
    out = tmp_path / "out.knxproj"
    v20_hardware = (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<KNX xmlns="http://knx.org/xml/project/20"><ManufacturerData/></KNX>'
    )
    with pytest.raises(ValueError, match="project/20"):
        export_knxproj(
            src,
            out,
            schema="23",  # force native /23, no master to align down
            extra_files={"M-0001/Hardware.xml": v20_hardware},
        )


def test_export_project_name_override(tmp_path: Path) -> None:
    """``project_name`` sets the exported ProjectInformation Name without touching the source."""
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-NM")
    svc.close(pid)
    out = tmp_path / "out.knxproj"
    export_knxproj(src, out, project_name="Musterhaus")
    with zipfile.ZipFile(out) as zf:
        project_xml = zf.read(f"{pid}/project.xml").decode("utf-8")
    assert 'Name="Musterhaus"' in project_xml
    # source project name is unchanged (transient override)
    svc2 = ProjectService()
    svc2.open(src)
    assert svc2.project(pid).name == "New project"
