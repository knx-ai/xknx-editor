"""Regression: per-frame service reads must be IO-guarded so they bail while a background import
holds the IO lock (rewriting the schema on a worker thread). An unguarded read races the DDL and
SQLite raises "malformed database schema (...) - index ... already exists", which crashed the app
mid-render (via get_unassigned_devices / group_address_style).
"""

from __future__ import annotations

from pathlib import Path

from editor_gui.plugins.base import Logger
from editor_gui.plugins.catalog.service import CatalogService
from editor_gui.plugins.logger.service import LogService
from editor_gui.plugins.project.service import ProjectService
from xknxmono.project.core.addressing import GroupAddressStyle


def _project(tmp_path: Path) -> ProjectService:
    proj = ProjectService(CatalogService(tmp_path / "c.xknxcatalog"))
    proj.set_logger(Logger(LogService(), "project"))
    proj.new(tmp_path / "p.xknx")
    return proj


def test_unassigned_devices_bails_while_import_holds_lock(tmp_path: Path) -> None:
    proj = _project(tmp_path)
    # Simulate a background import holding the shared IO lock (as import_knxproj does).
    proj._io_lock.acquire()
    try:
        assert proj.get_unassigned_devices() == []  # bails, does not query the DB
    finally:
        proj._io_lock.release()


def test_group_address_style_bails_while_import_holds_lock(tmp_path: Path) -> None:
    proj = _project(tmp_path)
    proj._io_lock.acquire()
    try:
        assert (
            proj.group_address_style == GroupAddressStyle.THREE_LEVEL
        )  # default, no DB query
    finally:
        proj._io_lock.release()


def test_reads_work_normally_without_the_lock(tmp_path: Path) -> None:
    # Sanity: unguarded (lock free) the same reads return real data.
    proj = _project(tmp_path)
    assert proj.get_unassigned_devices() == []  # fresh project, no devices
    assert proj.group_address_style in set(GroupAddressStyle)
