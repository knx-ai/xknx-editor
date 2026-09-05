"""The temp-file import + atomic swap: a .knxproj is parsed/written into a sibling temp file, then
os.replace'd into place and opened, so we never rewrite the project file under an open SQLite
connection. Re-importing over the currently-open project used to raise "malformed database schema";
this covers that path end to end against the real fixture.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from editor_gui.plugins.base import Logger
from editor_gui.plugins.catalog.service import CatalogService
from editor_gui.plugins.logger.service import LogService
from editor_gui.plugins.project.service import ProjectService


def _fixture() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        cand = (
            parent
            / "packages/proj/tests/fixtures/xknx_test_project_no_password.knxproj"
        )
        if cand.exists():
            return cand
    return None


def _project(tmp_path: Path) -> ProjectService:
    proj = ProjectService(CatalogService(tmp_path / "c.xknxcatalog"))
    proj.set_logger(Logger(LogService(), "project"))
    return proj


def test_reimport_over_open_project_swaps_cleanly(tmp_path: Path) -> None:
    fx = _fixture()
    if fx is None:
        pytest.skip("knxproj fixture not available")
    proj = _project(tmp_path)
    dest = tmp_path / "p.xknx"

    proj.import_knxproj(fx, dest)
    assert proj.path == dest  # opened the imported project
    # Group addresses are project data (catalog-independent), so a real parse populates them even
    # when the bundled catalog is incomplete and the resolved device view stays empty.
    first_gas = len(proj.group_addresses)
    assert first_gas > 0

    # Re-import over the SAME open project file — the case that raced the schema DDL and crashed.
    proj.import_knxproj(fx, dest)
    assert len(proj.group_addresses) == first_gas

    # No temp artifact left behind, and the previously-crashing read paths work.
    assert not list(tmp_path.glob("*.import-*.tmp"))
    _ = proj.get_unassigned_devices()
    _ = proj.group_address_style


def test_import_leaves_no_temp_file(tmp_path: Path) -> None:
    fx = _fixture()
    if fx is None:
        pytest.skip("knxproj fixture not available")
    proj = _project(tmp_path)
    dest = tmp_path / "fresh.xknx"
    proj.import_knxproj(fx, dest)
    assert dest.exists()
    assert not list(tmp_path.glob("*.import-*.tmp"))
