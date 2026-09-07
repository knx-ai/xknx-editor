"""A project database on a location SQLite can't use (network share, read-only dir) must fail with
a clear, typed :class:`ProjectStorageError` — not a raw ``OperationalError`` mid-DDL."""

from __future__ import annotations

from pathlib import Path

import pytest

from xknxeditor.proj import ProjectStorageError, ensure_sqlite_writable
from xknxeditor.proj.db import make_engine, url_for


def test_ensure_sqlite_writable_ok_and_cleans_up(tmp_path: Path) -> None:
    ensure_sqlite_writable(tmp_path / "p.xknx")  # must not raise on a normal local dir
    # The throwaway probe (and any journal sidecar) must be gone.
    assert list(tmp_path.iterdir()) == []


def test_ensure_sqlite_writable_rejects_unusable_location(tmp_path: Path) -> None:
    # Parent is a FILE, so the directory can't exist — a deterministic stand-in for a location
    # SQLite cannot open (the real case is a network share, which we can't mount in a unit test).
    blocker = tmp_path / "blocker"
    blocker.write_bytes(b"")
    with pytest.raises(ProjectStorageError):
        ensure_sqlite_writable(blocker / "p.xknx")


def test_make_engine_translates_open_failure(tmp_path: Path) -> None:
    blocker = tmp_path / "blocker"
    blocker.write_bytes(b"")
    with pytest.raises(ProjectStorageError):
        make_engine(url_for(blocker / "p.xknx"))
