"""Tests for the ``.knxproj`` importer.

The mapping logic is exercised through the public ``import_knxproj`` with its parse step patched to
return a lightweight fake parser that duck-types the ``xknxproject`` attributes the importer reads —
no binary fixture, no dependency on xknxproject's own parsing (which is its responsibility, not
ours). A separate smoke test runs the real ``import_knxproj`` against a local ``.knxproj`` when one
is available, and is skipped otherwise.
"""

import zlib
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from zipfile import BadZipFile

import pytest
from sqlalchemy.orm import Session
from xknxproject.exceptions import InvalidPasswordException, UnexpectedFileContent

from xknxeditor.proj import ProjectService, import_knxproj
from xknxeditor.proj.core import knxproj_import
from xknxeditor.proj.core.addressing import GroupAddressStyle
from xknxeditor.proj.db import make_engine, url_for
from xknxeditor.proj.models import ComObjectLink, GroupRange


def _coir(**kw: Any) -> SimpleNamespace:
    defaults: dict[str, Any] = {
        "com_object_ref_id": None,
        "ref_id": "O-1_R-1",
        "channel": None,
        "read_flag": None,
        "write_flag": None,
        "communication_flag": None,
        "transmit_flag": None,
        "update_flag": None,
        "read_on_init_flag": None,
        "links": None,
    }
    return SimpleNamespace(**{**defaults, **kw})


def _fake_parser() -> SimpleNamespace:
    device = SimpleNamespace(
        address=5,
        identifier="P-TEST-0_DI-1",
        individual_address="1.1.5",
        name="Dev",
        product_ref="M-1_H-1_P-1",
        hardware_program_ref="M-1_H-1_HP-1",
        description="A device",
        order_number="ORD-1",
        hardware_name="HW One",
        product_name="Prod One",
        manufacturer_name="ACME",
        com_object_instance_refs=[
            _coir(
                com_object_ref_id="M-1_A-1_O-1_R-1",
                channel="CH-1",
                write_flag=True,
                communication_flag=True,
                transmit_flag=True,
                links=["GA-1", "GA-2"],
            )
        ],
        parameter_instance_refs={"M-1_A-1_P-1": SimpleNamespace(value="3")},
        module_instances=[],
    )
    line = SimpleNamespace(
        address=1, name="Line 1", medium_type="MT-0", devices=[device]
    )
    area = SimpleNamespace(address=1, name="Area 1", lines=[line])
    middle = SimpleNamespace(
        range_start=1, range_end=255, name="Middle", group_ranges=[]
    )
    main = SimpleNamespace(
        range_start=1, range_end=2047, name="Main", group_ranges=[middle]
    )
    gas = [
        SimpleNamespace(
            raw_address=1,
            name="GA One",
            dpt={"main": 1, "sub": 1},
            identifier="GA-1",
            description="GA desc",
            comment="GA comment",
            data_secure_key="k",
        ),
        SimpleNamespace(
            raw_address=2,
            name="GA Two",
            dpt={"main": 5, "sub": None},
            identifier="GA-2",
            description="",
            comment="",
            data_secure_key=None,
        ),
    ]
    room = SimpleNamespace(
        identifier="SP-ROOM",
        name="Wohnzimmer",
        space_type=SimpleNamespace(value="Room"),
        number="1",
        usage_text="Living",
        description="",
        spaces=[],
        devices=["1.1.5"],
        functions=["F-1"],
    )
    building = SimpleNamespace(
        identifier="SP-B",
        name="Haus",
        space_type=SimpleNamespace(value="Building"),
        number="",
        usage_text="",
        description="",
        spaces=[room],
        devices=[],
        functions=[],
    )
    function = SimpleNamespace(
        identifier="F-1",
        function_type="FT-1",
        name="Light",
        usage_text="Lighting",
        space_id="SP-ROOM",
        group_addresses=[
            SimpleNamespace(ref_id="GA-1", address="0/0/1", role="Switch")
        ],
    )
    return SimpleNamespace(
        project_info=SimpleNamespace(
            name="Test",
            group_address_style=SimpleNamespace(value="ThreeLevel"),
            guid="GUID-1",
            created_by="ETS6",
            last_modified="2020-01-01",
            schema_version="20",
            tool_version="6.0.0",
        ),
        areas=[area],
        group_ranges=[main],
        group_addresses=gas,
        spaces=[building],
        functions=[function],
    )


def _import_fake(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[ProjectService, str, Path]:
    # Replace the xknxproject-backed parse with our fake so the public entry point is exercised.
    # ``_parse`` returns ``(parser, extras)``; the fake has no raw XML, so extras are empty.
    def _fake(
        *_a: object, **_k: object
    ) -> tuple[SimpleNamespace, knxproj_import._RawExtras]:
        return _fake_parser(), knxproj_import._RawExtras()

    monkeypatch.setattr(knxproj_import, "_parse", _fake)
    dest = tmp_path / "imported.xknx"
    pid = import_knxproj("unused.knxproj", dest, project_id="P-TEST")
    svc = ProjectService()
    svc.open(dest)
    return svc, pid, dest


def test_project_metadata(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    svc, pid, _ = _import_fake(tmp_path, monkeypatch)
    project = svc.project(pid)
    assert project.name == "Test"
    assert project.group_address_style == GroupAddressStyle.THREE_LEVEL


def test_topology(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    svc, pid, _ = _import_fake(tmp_path, monkeypatch)
    inst = svc.topology(pid, 0)
    assert [a.address for a in inst.areas] == [1]
    line = inst.areas[0].lines[0]
    assert line.address == 1
    assert line.segments[0].medium_type == "MT-0"


def test_device(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    svc, pid, _ = _import_fake(tmp_path, monkeypatch)
    devices = svc.devices(pid)
    assert len(devices) == 1
    dev = devices[0]
    assert dev.product_ref_id == "M-1_H-1_P-1"
    assert dev.hardware2program_ref_id == "M-1_H-1_HP-1"
    assert svc.individual_address(pid, dev.id) == "1.1.5"
    assert [(p.ref_id, p.value) for p in dev.parameters] == [("M-1_A-1_P-1", "3")]
    assert len(dev.com_objects) == 1
    co = dev.com_objects[0]
    assert (
        co.ref_id == "M-1_A-1_O-1_R-1"
    )  # app-prefixed form the GUI's DynamicUI expects
    assert co.channel_id == "CH-1"
    assert (co.write_flag, co.communication_flag, co.read_flag) == (True, True, None)


def test_group_addresses_and_dpt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    svc, pid, _ = _import_fake(tmp_path, monkeypatch)
    gas = {g.address: g for g in svc.group_addresses(pid)}
    assert gas[1].name == "GA One"
    assert gas[1].datapoint_type == "DPST-1-1"
    assert gas[2].datapoint_type == "DPT-5"  # no sub-type


def test_group_ranges_preserve_names(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, _, dest = _import_fake(tmp_path, monkeypatch)
    engine = make_engine(url_for(dest))
    with Session(engine) as session:
        ranges = session.query(GroupRange).order_by(GroupRange.range_start).all()
        names = {(r.range_start, r.range_end): r.name for r in ranges}
        assert names[(1, 2047)] == "Main"
        assert names[(1, 255)] == "Middle"
        # the group address at value 1 sits under the smallest (leaf) range that contains it
        middle = next(r for r in ranges if (r.range_start, r.range_end) == (1, 255))
        assert {ga.address for ga in middle.group_addresses} == {1, 2}
    engine.dispose()


def test_group_ranges_read(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    svc, pid, _ = _import_fake(tmp_path, monkeypatch)
    roots = svc.group_ranges(pid, 0)
    assert len(roots) == 1
    main = roots[0]
    assert main.name == "Main"
    assert (main.range_start, main.range_end) == (1, 2047)
    assert len(main.children) == 1
    middle = main.children[0]
    assert middle.name == "Middle"
    assert {ga.address for ga in middle.group_addresses} == {1, 2}


def test_project_metadata_extra(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    svc, pid, _ = _import_fake(tmp_path, monkeypatch)
    p = svc.project(pid)
    assert p.created_by == "ETS6"
    assert p.tool_version == "6.0.0"
    assert p.guid == "GUID-1"
    assert p.schema_version == "20"


def test_device_metadata(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    svc, pid, _ = _import_fake(tmp_path, monkeypatch)
    dev = svc.devices(pid)[0]
    info = svc.device(pid, dev.id)
    assert info.order_number == "ORD-1"
    assert info.hardware_name == "HW One"
    assert info.manufacturer_name == "ACME"
    assert info.description == "A device"


def test_group_address_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    svc, pid, _ = _import_fake(tmp_path, monkeypatch)
    gas = {g.address: g for g in svc.group_addresses(pid)}
    assert gas[1].description == "GA desc"
    assert gas[1].comment == "GA comment"
    assert gas[1].data_secure is True
    assert gas[2].data_secure is False


def test_space_tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    svc, pid, _ = _import_fake(tmp_path, monkeypatch)
    roots = svc.space_tree(pid, 0)
    assert len(roots) == 1
    building = roots[0]
    assert building.space_type == "Building"
    assert building.name == "Haus"
    assert len(building.children) == 1
    room = building.children[0]
    assert room.space_type == "Room"
    # the device placed in the room
    assert [d.individual_address for d in room.devices] == ["1.1.5"]
    # the function assigned to the room, with its GA and role
    assert len(room.functions) == 1
    fn = room.functions[0]
    assert fn.name == "Light"
    assert [(g.text, g.role) for g in fn.group_addresses] == [("0/0/1", "Switch")]


def test_links_sending_flag(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _, _, dest = _import_fake(tmp_path, monkeypatch)
    engine = make_engine(url_for(dest))
    with Session(engine) as session:
        links = session.query(ComObjectLink).all()
        assert len(links) == 2
        by_addr = {link.group_address.address: link.is_sending for link in links}
        assert by_addr == {
            1: True,
            2: False,
        }  # first link of the com-object is the sender
    engine.dispose()


@pytest.mark.parametrize(
    "raised",
    [zlib.error("bad"), BadZipFile("bad"), RuntimeError("Bad password for file")],
)
def test_parse_failure_with_password_is_invalid_password(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, raised: Exception
) -> None:
    def _boom(*_a: object, **_k: object) -> SimpleNamespace:
        raise raised

    monkeypatch.setattr(knxproj_import, "_parse", _boom)
    with pytest.raises(InvalidPasswordException):
        import_knxproj("x.knxproj", tmp_path / "o.xknx", password="whatever")


def test_parse_failure_without_password_is_unexpected_content(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _boom(*_a: object, **_k: object) -> SimpleNamespace:
        raise zlib.error("garbage")

    monkeypatch.setattr(knxproj_import, "_parse", _boom)
    with pytest.raises(UnexpectedFileContent):
        import_knxproj("x.knxproj", tmp_path / "o.xknx")


def test_missing_password_propagates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _boom(*_a: object, **_k: object) -> SimpleNamespace:
        raise InvalidPasswordException("Password required.")

    monkeypatch.setattr(knxproj_import, "_parse", _boom)
    with pytest.raises(InvalidPasswordException):
        import_knxproj("x.knxproj", tmp_path / "o.xknx")


def test_reimport_overwrites_existing_dest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _fake(
        *_a: object, **_k: object
    ) -> tuple[SimpleNamespace, knxproj_import._RawExtras]:
        return _fake_parser(), knxproj_import._RawExtras()

    monkeypatch.setattr(knxproj_import, "_parse", _fake)
    dest = tmp_path / "reimport.xknx"
    import_knxproj("x.knxproj", dest, project_id="P-1")
    # A second import to the same file must overwrite, not clash on unique rows (installation index).
    import_knxproj("x.knxproj", dest, project_id="P-2")
    svc = ProjectService()
    assert svc.open(dest) == "P-2"


def test_failed_parse_preserves_existing_dest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _fake(
        *_a: object, **_k: object
    ) -> tuple[SimpleNamespace, knxproj_import._RawExtras]:
        return _fake_parser(), knxproj_import._RawExtras()

    monkeypatch.setattr(knxproj_import, "_parse", _fake)
    dest = tmp_path / "keep.xknx"
    import_knxproj("x.knxproj", dest, project_id="P-KEEP")
    before = dest.read_bytes()

    def _boom(*_a: object, **_k: object) -> SimpleNamespace:
        raise zlib.error("garbage")

    monkeypatch.setattr(knxproj_import, "_parse", _boom)
    with pytest.raises(UnexpectedFileContent):
        import_knxproj("x.knxproj", dest)
    assert (
        dest.read_bytes() == before
    )  # the failed import must not touch the existing project


# End-to-end against a real, bundled ETS project (xknxproject's own MIT-licensed, unencrypted
# sample). This exercises the real xknxproject parse + OUR mapping (topology/GAs/links), which the
# fake-parser tests above deliberately skip — it is what caught e.g. the project/11 master-data bug.
_REAL = Path(__file__).parent / "fixtures" / "xknx_test_project_no_password.knxproj"


def test_import_real_file(tmp_path: Path) -> None:
    dest = tmp_path / "real.xknx"
    pid = import_knxproj(_REAL, dest)
    svc = ProjectService()
    svc.open(dest)
    assert svc.devices(pid)
    assert svc.group_addresses(pid)
