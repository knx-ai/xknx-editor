"""Per-user storage for the project-log (trace) decryption key.

Project-log comments are AES-encrypted with a key/IV/marker that are constant everywhere but shipped
in none of this project's source. A user with the KNX authoring tool installed extracts them from
their own ``Knx.Ets.Common.dll`` (via :func:`xknxeditor.proj.extract_trace_key`); the result is
stored per-user under :func:`settings.config_dir` and applied at startup. Without it, comments stay
encrypted (as stored). The values are not secret (identical everywhere), just not ours to ship.
"""

from __future__ import annotations

from editor_gui.settings import load_settings, save_settings
from xknxeditor.proj import reset_trace_key, set_trace_key

_NAME = "trace_key"


def load_cached_key() -> tuple[bytes, bytes, str] | None:
    """Return the cached ``(key, iv, marker)``, or ``None`` if unset/invalid."""
    data = load_settings(_NAME)
    try:
        return (
            bytes.fromhex(data["key"]),
            bytes.fromhex(data["iv"]),
            data["marker"],
        )
    except (KeyError, TypeError, ValueError):
        return None


def save_key(key: bytes, iv: bytes, marker: str) -> None:
    """Persist the key/IV (as hex) and marker and apply them immediately."""
    save_settings(_NAME, {"key": key.hex(), "iv": iv.hex(), "marker": marker})
    set_trace_key(key, iv, marker)


def clear_key() -> None:
    """Remove the cached key so comments are treated as opaque again."""
    save_settings(_NAME, {})
    reset_trace_key()


def apply_cached_key() -> bool:
    """Apply the cached key if present. Returns whether a key was applied."""
    key = load_cached_key()
    if key is None:
        return False
    set_trace_key(*key)
    return True
