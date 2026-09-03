"""Tests for the .knxprod ingest, especially dedup that must stay consistent with the DB.

Regression: the store used to skip ingest whenever the hash-named file existed, so deleting the
catalog DB while keeping the file cache left re-imports as no-ops (the DB stayed empty and every
project device was skipped). Dedup is now DB-driven.
"""

from __future__ import annotations

from pathlib import Path

from xknxmono.catalog import CatalogService
from xknxmono.catalog.db import knxprod_dir_for

_FIXTURE = (
    Path(__file__).parents[3]
    / "packages/product/tests/fixtures/gira_2gang_button_interface.knxprod"
)


def test_import_populates_catalog(tmp_path: Path) -> None:
    svc = CatalogService(tmp_path / "cat.xknxcatalog")
    svc.import_knxprod(_FIXTURE.read_bytes())
    assert len(svc.list_products()) > 0


def test_reimport_repopulates_after_db_reset(tmp_path: Path) -> None:
    # First import fills the DB and writes the file cache.
    content = _FIXTURE.read_bytes()
    db = tmp_path / "cat.xknxcatalog"
    CatalogService(db).import_knxprod(content)
    stored = list(knxprod_dir_for(db).glob("*.knxprod"))
    assert stored, "the .knxprod should have been cached to the store"

    # Simulate the user deleting only the catalog DB (the file cache survives).
    db.unlink()
    svc = CatalogService(db)  # fresh, empty DB — same store dir, file still present
    assert svc.list_products() == []

    # Re-import must repopulate the DB even though the store file already exists.
    svc.import_knxprod(content)
    assert len(svc.list_products()) > 0


def test_reimport_rewrites_missing_store_file(tmp_path: Path) -> None:
    # Opposite drift: DB has the data but the cached file was deleted -> re-import restores it.
    content = _FIXTURE.read_bytes()
    db = tmp_path / "cat.xknxcatalog"
    svc = CatalogService(db)
    svc.import_knxprod(content)
    for f in knxprod_dir_for(db).glob("*.knxprod"):
        f.unlink()
    path = svc.import_knxprod(content)
    assert path.exists()
