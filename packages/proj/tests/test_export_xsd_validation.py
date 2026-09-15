"""The exported ``0.xml`` must validate against the official KNX ``knx_project`` XSD for BOTH
project/20 (ETS5) and project/23 (ETS6), and a full export -> re-import cycle must preserve the
round-trip attributes xknxproject drops (``GroupAddress@Global``/``@Central``, ``Space@Usage``,
``Segment DomainAddress``, ``Trade@CompletionStatus``/``@Context``, ``Function`` comment/description).

The XSDs live under ``.references/`` (not shipped with the repo), so the whole module skips when they
are absent, and skips individually if ``xmlschema`` is not installed.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from xknxeditor.proj import ProjectService, export_knxproj, import_knxproj
from xknxeditor.proj.db import make_engine, url_for
from xknxeditor.proj.models import (
    Device,
    Function,
    GroupAddress,
    Segment,
    Space,
    Trade,
    TradeDevice,
)

xmlschema = pytest.importorskip("xmlschema")

_REPO_ROOT = Path(__file__).resolve().parents[3]


def _xsd_path(schema: str) -> Path:
    return _REPO_ROOT / ".references" / f"knx_project_v{schema}.xsd"


def _zero_xml(knxproj: Path) -> bytes:
    with zipfile.ZipFile(knxproj) as zf:
        name = next(n for n in zf.namelist() if n.endswith("/0.xml"))
        return zf.read(name)


def _project_with_roundtrip_attrs(tmp_path: Path) -> Path:
    """A project exercising every round-trip attribute the exporter re-emits from stored state."""
    src = tmp_path / "src.xknx"
    svc = ProjectService()
    pid = svc.create(src, "P-XSD")
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
        address=5,
        name="Switch",
        hardware2program_ref_id="M-1_H-1_HP-1",
    )
    ga_id = svc.create_group_address(pid, 0, 0x0802, "ga")
    svc.close(pid)

    with Session(make_engine(url_for(src))) as s:
        ga = s.get(GroupAddress, ga_id)
        assert ga is not None
        ga.central = True
        ga.is_global = True
        device = s.get(Device, device_id)
        assert device is not None
        segment = s.get(Segment, device.segment_id)
        assert segment is not None
        segment.domain_address = 12345
        installation = device.segment.line.area.installation
        # ``@Usage`` must be an XSD NCName (no colon); genuine ETS ids look like ``SU-<int>``.
        space = Space(space_type="Room", name="Kitchen", usage="SU-1", order=0)
        space.functions.append(
            Function(name="Light", comment="fn-comment", description="fn-desc", order=0)
        )
        installation.spaces.append(space)
        trade = Trade(
            name="Elec",
            number="1",
            completion_status="Editing",
            context="ctx",
            order=0,
        )
        trade.devices.append(TradeDevice(device=device, order=0))
        installation.trades.append(trade)
        s.commit()
    return src


@pytest.mark.parametrize("schema", ["20", "23"])
def test_export_validates_against_xsd(tmp_path: Path, schema: str) -> None:
    xsd_file = _xsd_path(schema)
    if not xsd_file.exists():
        pytest.skip(f"{xsd_file} not present (.references is not shipped)")
    src = _project_with_roundtrip_attrs(tmp_path)
    out = tmp_path / f"out{schema}.knxproj"
    export_knxproj(src, out, schema=schema)
    # ``validate`` raises XMLSchemaValidationError on any schema violation.
    xmlschema.XMLSchema(str(xsd_file)).validate(_zero_xml(out))


@pytest.mark.parametrize("schema", ["20", "23"])
def test_roundtrip_attrs_survive_full_reimport(tmp_path: Path, schema: str) -> None:
    src = _project_with_roundtrip_attrs(tmp_path)
    out = tmp_path / f"out{schema}.knxproj"
    export_knxproj(src, out, schema=schema)
    round_path = tmp_path / f"round{schema}.xknx"
    import_knxproj(out, round_path)

    with Session(make_engine(url_for(round_path))) as s:
        ga = s.query(GroupAddress).filter_by(name="ga").one()
        assert (ga.central, ga.is_global) == (True, True)

        segment = s.query(Segment).filter(Segment.domain_address.isnot(None)).one()
        assert segment.domain_address == 12345

        space = s.query(Space).filter_by(name="Kitchen").one()
        assert space.usage == "SU-1"

        function = s.query(Function).filter_by(name="Light").one()
        assert (function.comment, function.description) == ("fn-comment", "fn-desc")

        trade = s.query(Trade).filter_by(name="Elec").one()
        assert (trade.completion_status, trade.context) == ("Editing", "ctx")
