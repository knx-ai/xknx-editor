"""Open a local file in the OS default handler (used to show exported HTML label sheets)."""

from __future__ import annotations

import webbrowser
from pathlib import Path


def open_path(path: str) -> bool:
    """Open ``path`` in the OS default application. Returns whether the request was dispatched.

    Uses :func:`webbrowser.open` on the ``file://`` URI, which is cross-platform stdlib and the right
    handler for HTML output. Best-effort: never raises."""
    try:
        return webbrowser.open(Path(path).resolve().as_uri())
    except (OSError, ValueError):
        return False
