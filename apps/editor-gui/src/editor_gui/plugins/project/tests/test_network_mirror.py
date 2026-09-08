"""SMB/network-drive fallback: a project whose home is on a location SQLite can't use is worked on
via a LOCAL mirror and written back to the home on close/switch/exit.

We can't mount a real share in a unit test, so we force the "network" branch by monkeypatching the
detection (`_needs_mirror`) and redirect the mirror store into ``tmp_path`` by patching the
facade's ``config_dir``.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from editor_gui.plugins.base import Logger
from editor_gui.plugins.catalog.service import CatalogService
from editor_gui.plugins.logger.service import LogService
from editor_gui.plugins.project import service as service_mod
from editor_gui.plugins.project.service import ProjectService


def _setup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[ProjectService, Path]:
    """A ProjectService whose mirror store is under tmp_path, plus a ``net`` dir that is treated as
    a network location (everything under it is mirrored)."""
    cfg = tmp_path / "cfg"
    monkeypatch.setattr(service_mod, "config_dir", lambda: cfg)
    net = tmp_path / "net"
    net.mkdir()

    def _is_net(home: Path) -> bool:
        return str(Path(home)).startswith(str(net))

    monkeypatch.setattr(ProjectService, "_needs_mirror", staticmethod(_is_net))
    proj = ProjectService(CatalogService(tmp_path / "c.xknxcatalog"))
    proj.set_logger(Logger(LogService(), "project"))
    return proj, net


def _ga_count(xknx: Path) -> int:
    con = sqlite3.connect(str(xknx))
    try:
        return con.execute("SELECT COUNT(*) FROM group_addresses").fetchone()[0]
    finally:
        con.close()


def test_new_mirrored_uses_local_working(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    proj, net = _setup(tmp_path, monkeypatch)
    home = net / "p.xknx"
    proj.new(home)
    assert proj.path == home
    assert proj.mirroring_active
    assert proj.working_path is not None and proj.working_path != home
    assert (tmp_path / "cfg" / "mirrors") in proj.working_path.parents
    assert not home.exists()  # nothing written to the "share" until close


def test_close_writes_back_to_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    proj, net = _setup(tmp_path, monkeypatch)
    home = net / "p.xknx"
    proj.new(home)
    proj.create_group_address(address="1/2/3", name="keep")
    assert not home.exists()
    proj.close()
    assert home.exists()  # written back
    assert not Path(f"{home}-journal").exists()  # clean, no stray journal
    assert _ga_count(home) == 1  # the edit made it to the share copy


def test_crash_recovery_reuses_unsynced_mirror(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    proj, net = _setup(tmp_path, monkeypatch)
    home = net / "p.xknx"
    proj.new(home)
    proj.create_group_address(address="4/5/6", name="unsynced")
    # Simulate a crash: the process dies without teardown, so home was never written but the local
    # mirror holds the committed edit. A fresh service opening the same home must reuse that mirror.
    assert not home.exists()
    proj2 = ProjectService(CatalogService(tmp_path / "c2.xknxcatalog"))
    proj2.set_logger(Logger(LogService(), "project"))
    assert proj2.can_open(home)  # mirror present even though home is missing
    proj2.open(home)
    assert [g.address for g in proj2.group_addresses] == ["4/5/6"]


def test_writeback_failure_keeps_mirror(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    proj, net = _setup(tmp_path, monkeypatch)
    log = LogService()
    proj.set_logger(Logger(log, "project"))
    home = net / "p.xknx"
    proj.new(home)
    proj.create_group_address(address="7/7/7", name="keep")
    working = proj.working_path
    assert working is not None

    def _boom(src: str, dst: str) -> None:
        raise OSError("share gone")

    monkeypatch.setattr(service_mod.shutil, "copyfile", _boom)
    proj.close()  # write-back fails; must not raise, must log, must keep the mirror
    assert any(r.level == "error" for r in log.get_records())
    assert working.exists()
    assert _ga_count(working) == 1  # local copy still holds the data


def test_local_project_not_mirrored(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    proj, _net = _setup(tmp_path, monkeypatch)
    home = tmp_path / "local.xknx"  # NOT under net -> not mirrored
    proj.new(home)
    assert not proj.mirroring_active
    assert proj.working_path == home
    assert home.exists()


def test_distinct_shares_same_filename_distinct_mirrors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    proj, net = _setup(tmp_path, monkeypatch)
    proj.new(net / "a" / "p.xknx")  # same basename, different share dir
    working_a = proj.working_path
    proj.new(net / "b" / "p.xknx")
    working_b = proj.working_path
    assert working_a is not None and working_b is not None and working_a != working_b


def test_save_as_to_network_writes_back(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    proj, net = _setup(tmp_path, monkeypatch)
    proj.new(tmp_path / "local.xknx")  # local, not mirrored
    proj.create_group_address(address="1/1/1", name="x")
    home = net / "saved.xknx"
    proj.save_as(home)
    assert proj.path == home
    assert proj.mirroring_active
    proj.close()
    assert _ga_count(home) == 1


def _knxproj_fixture() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        fx = parent / "packages/proj/tests/fixtures/xknx_test_project_no_password.knxproj"
        if fx.is_file():
            return fx
    return None


def test_import_to_network_mirrors_then_writes_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fx = _knxproj_fixture()
    if fx is None:
        pytest.skip("knxproj fixture not available")
    proj, net = _setup(tmp_path, monkeypatch)
    dest = net / "imported.xknx"
    proj.import_knxproj(fx, dest)
    assert proj.path == dest
    assert proj.mirroring_active
    # No SQLite written next to the network dest before close; a temp/db there would mean the import
    # wrote to the share.
    assert not dest.exists()
    proj.close()
    assert dest.exists()
