"""Additive schema migration: reopening a project written by an older schema must add the columns
the model has since gained, so full-entity queries keep working (no "no such column")."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from sqlalchemy import inspect

from xknxeditor.proj.core.service import ProjectService
from xknxeditor.proj.db import make_engine, url_for


def test_reopen_adds_missing_columns(tmp_path: Path) -> None:
    path = tmp_path / "proj.xknx"
    svc = ProjectService()
    pid = svc.create(path)
    svc.close(pid)

    # Simulate a file written before these columns existed.
    con = sqlite3.connect(path)
    con.execute("ALTER TABLE devices DROP COLUMN serial_number")
    con.execute("ALTER TABLE devices DROP COLUMN parameters_loaded")
    con.execute("ALTER TABLE group_addresses DROP COLUMN unfiltered")
    con.execute("ALTER TABLE lines DROP COLUMN additional_group_addresses")
    con.commit()
    con.close()

    # Reopening must migrate (add) them back and leave the project queryable.
    svc2 = ProjectService()
    pid2 = svc2.open(path)
    assert (
        svc2.devices(pid2) == []
    )  # full-entity query works again (no OperationalError)

    cols = inspect(make_engine(url_for(path)))
    device_cols = {c["name"] for c in cols.get_columns("devices")}
    assert {"serial_number", "parameters_loaded"} <= device_cols
    assert "unfiltered" in {c["name"] for c in cols.get_columns("group_addresses")}
    assert "additional_group_addresses" in {
        c["name"] for c in cols.get_columns("lines")
    }


def test_reopen_migrates_json_column_to_valid_default(tmp_path: Path) -> None:
    """A JSON column added to an existing table must default to valid JSON (``[]`` for
    ``default=list``), not ``''`` — otherwise reading a migrated row crashes in ``json.loads``."""
    from sqlalchemy.orm import Session

    from xknxeditor.proj.models import Device, ModuleInstance

    path = tmp_path / "proj.xknx"
    svc = ProjectService()
    pid = svc.create(path)
    seg = svc.create_line(pid, svc.create_area(pid, 0, 1, "A"), 1, "L")
    segment_id = next(
        line.segments[0].id
        for area in svc.topology(pid, 0).areas
        for line in area.lines
        if line.id == seg
    )
    device_id = svc.add_device(pid, segment_id, "M-1_H-1_P-1", address=5, name="D")
    with Session(make_engine(url_for(path))) as session:
        device = session.get(Device, device_id)
        assert device is not None
        device.module_instances.append(
            ModuleInstance(instance_id="MI-1", ref_id="MD-1")
        )
        session.commit()
    svc.close(pid)

    # Simulate a file written before the module-instance JSON/text columns existed.
    con = sqlite3.connect(path)
    con.execute("ALTER TABLE module_instances DROP COLUMN arguments")
    con.execute("ALTER TABLE module_instances DROP COLUMN repeat_index")
    con.commit()
    con.close()

    ProjectService().open(path)  # triggers the additive migration
    with Session(make_engine(url_for(path))) as session:
        mi = session.query(ModuleInstance).one()
        assert (
            mi.arguments == []
        )  # valid JSON default, not None/'' -> no json.loads crash
        assert mi.repeat_index == ""


def test_reopen_stamps_user_version(tmp_path: Path) -> None:
    from xknxeditor.proj.db import SCHEMA_VERSION

    path = tmp_path / "proj.xknx"
    svc = ProjectService()
    svc.close(svc.create(path))
    con = sqlite3.connect(path)
    try:
        (version,) = con.execute("PRAGMA user_version").fetchone()
    finally:
        con.close()
    assert version == SCHEMA_VERSION
