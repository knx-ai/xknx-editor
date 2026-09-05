"""Per-user storage for the genuine .knxproj signing key.

The signing library ships only a placeholder key; a genuine key (extracted from the user's ETS
``Knx.Ets.XmlSigning.dll`` via :func:`xknxeditor.proj.extract_converter_key`, or pasted by hand) is
stored per-user under :func:`settings.config_dir` and applied to the signer at startup. The file
holds the converter private key in plaintext hex — it is the user's own (and publicly known) key,
never committed to the repo or written into a project.
"""

from __future__ import annotations

from editor_gui.settings import load_settings, save_settings
from xknxeditor.proj import reset_signing_key, set_signing_key

_NAME = "signing_key"


def load_cached_key() -> tuple[int, int, int] | None:
    """Return the cached ``(modulus, private_exponent, public_exponent)``, or ``None`` if unset."""
    data = load_settings(_NAME)
    try:
        return (
            int(data["modulus"], 16),
            int(data["private_exponent"], 16),
            int(data["public_exponent"], 16),
        )
    except (KeyError, TypeError, ValueError):
        return None


def save_key(modulus: int, private_exponent: int, public_exponent: int = 65537) -> None:
    """Persist the key (as hex) and apply it to the signer immediately."""
    save_settings(
        _NAME,
        {
            "modulus": f"{modulus:x}",
            "private_exponent": f"{private_exponent:x}",
            "public_exponent": f"{public_exponent:x}",
        },
    )
    set_signing_key(modulus, private_exponent, public_exponent)


def clear_key() -> None:
    """Remove the cached key and revert the signer to its placeholder."""
    save_settings(_NAME, {})
    reset_signing_key()


def apply_cached_key() -> bool:
    """Apply the cached key to the signer if present. Returns whether a key was applied."""
    key = load_cached_key()
    if key is None:
        return False
    set_signing_key(*key)
    return True
