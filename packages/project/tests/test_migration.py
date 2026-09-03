"""Additive schema migration: reopening a project written by an older schema must add the columns
the model has since gained, so full-entity queries keep working (no "no such column")."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from sqlalchemy import inspect

from xknxmono.project.core.service import ProjectService
from xknxmono.project.db import make_engine, url_for


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


def test_reopen_stamps_user_version(tmp_path: Path) -> None:
    from xknxmono.project.db import SCHEMA_VERSION

    path = tmp_path / "proj.xknx"
    svc = ProjectService()
    svc.close(svc.create(path))
    con = sqlite3.connect(path)
    try:
        (version,) = con.execute("PRAGMA user_version").fetchone()
    finally:
        con.close()
    assert version == SCHEMA_VERSION
