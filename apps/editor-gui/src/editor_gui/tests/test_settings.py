"""Tests for the JSON settings store (used by recent files, connection, catalog language, MCP)."""

from __future__ import annotations

from pathlib import Path

import pytest

from editor_gui import settings


@pytest.fixture(autouse=True)
def _tmp_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "config_dir", lambda: tmp_path)


def test_round_trip() -> None:
    settings.save_settings("app", {"recent_files": ["/a.xknx", "/b.xknx"]})
    assert settings.load_settings("app")["recent_files"] == ["/a.xknx", "/b.xknx"]


def test_missing_returns_empty() -> None:
    assert settings.load_settings("does-not-exist") == {}


def test_corrupt_file_returns_empty(tmp_path: Path) -> None:
    (tmp_path / "broken.json").write_text("{not json", encoding="utf-8")
    assert settings.load_settings("broken") == {}


def test_non_dict_json_returns_empty(tmp_path: Path) -> None:
    (tmp_path / "list.json").write_text("[1, 2, 3]", encoding="utf-8")
    assert settings.load_settings("list") == {}
