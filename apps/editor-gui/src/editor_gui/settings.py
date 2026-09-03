"""Small settings store: JSON files in a central per-user data directory.

Used for lightweight, non-project preferences (e.g. the last connection settings) and the
catalog database that should survive restarts, in one central location regardless of the
current working directory. Not for project data — that lives in the ``.xknx`` document."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import platformdirs

_APP_NAME = "xknx-editor"


def config_dir() -> Path:
    """Central per-user data directory (settings, catalog DB, caches).

    Uses the OS per-user data location (``platformdirs``) so it is stable regardless of
    where the app is launched from. On first creation, a legacy cwd-relative ``config/``
    folder (the old location) is migrated over so existing settings and catalog survive.
    """
    path = Path(platformdirs.user_data_dir(_APP_NAME))
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        _migrate_legacy_config(path)
    return path


def _migrate_legacy_config(target: Path) -> None:
    """Copy a legacy ``./config`` next to the launch directory into ``target`` (one-time)."""
    legacy = Path.cwd() / "config"
    if not legacy.is_dir() or legacy.resolve() == target.resolve():
        return
    try:
        for item in legacy.iterdir():
            dest = target / item.name
            if dest.exists():
                continue
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
    except OSError:
        pass


def load_settings(name: str) -> dict[str, Any]:
    """Load ``<config_dir>/<name>.json`` as a dict, or an empty dict if missing/unreadable."""
    path = config_dir() / f"{name}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def save_settings(name: str, data: dict[str, Any]) -> None:
    """Write ``data`` to ``<config_dir>/<name>.json`` (best effort; failures are ignored)."""
    path = config_dir() / f"{name}.json"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except OSError:
        pass
