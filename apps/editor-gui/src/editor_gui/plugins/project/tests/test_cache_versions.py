"""Regression test: the lazy view caches (devices / topology / group addresses) must invalidate
independently.

They used to share a single ``_cache_version``. After an edit, whichever cache was read first
rebuilt and stamped the shared version, so the *other* caches then saw ``version ==`` and returned
stale data until the next edit. Reading ``devices`` right after adding a group address, for example,
hid the new GA from ``group_addresses``.
"""

from __future__ import annotations

from pathlib import Path

from editor_gui.plugins.base import Logger
from editor_gui.plugins.catalog.service import CatalogService
from editor_gui.plugins.logger.service import LogService
from editor_gui.plugins.project.service import ProjectService


def _project(tmp_path: Path) -> ProjectService:
    proj = ProjectService(CatalogService(tmp_path / "c.xknxcatalog"))
    proj.set_logger(Logger(LogService(), "project"))
    proj.new(tmp_path / "p.xknx")
    return proj


def test_group_addresses_not_stale_after_reading_devices(tmp_path: Path) -> None:
    proj = _project(tmp_path)
    proj.create_group_address(address="1/1/1", name="first")

    # Read a *different* cache first — this used to stamp the shared version and hide later edits.
    _ = proj.devices
    proj.create_group_address(address="31/7/201", name="second")
    _ = proj.devices  # poison: rebuilds devices, would stamp the shared version

    addresses = {g.address for g in proj.group_addresses}
    assert "31/7/201" in addresses
    assert "1/1/1" in addresses


def test_topology_not_stale_after_reading_group_addresses(tmp_path: Path) -> None:
    proj = _project(tmp_path)
    _ = proj.group_addresses
    area_id = proj.create_area(7, "Area 7")
    assert area_id is not None
    _ = proj.group_addresses  # poison

    assert any(a.area_number == 7 for a in proj.get_areas())
