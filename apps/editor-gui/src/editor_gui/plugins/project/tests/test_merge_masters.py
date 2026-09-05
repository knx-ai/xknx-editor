"""Guards for ``_merge_masters`` signature preservation.

A genuine ``knx_master.xml`` carries a ``MasterData`` ``Signature`` over its exact bytes. The
importer rejects the whole import ("Invalid import data") when that signature no longer matches, so the
merge must return the base blob **verbatim** unless a real cross-source merge forces a rewrite.
"""

from __future__ import annotations

from editor_gui.plugins.project.knxproj_manufacturer import _merge_masters

_NS = "http://knx.org/xml/project/20"


def _master(manufacturers: list[str], signature: str) -> bytes:
    mfrs = "".join(f'<Manufacturer Id="{m}" Name="{m}" />' for m in manufacturers)
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        f'<KNX xmlns="{_NS}">'
        f'<MasterData Signature="{signature}">'
        f"<Manufacturers>{mfrs}</Manufacturers>"
        "</MasterData></KNX>"
    )
    return xml.encode("utf-8")


def test_single_master_returned_verbatim() -> None:
    blob = _master(["M-0001"], "SIG-KEEP")
    assert _merge_masters([blob]) is blob  # exact same bytes -> signature stays valid


def test_no_new_manufacturers_keeps_base_verbatim() -> None:
    base = _master(["M-0001", "M-0002"], "SIG-KEEP")
    subset = _master(["M-0001"], "SIG-OTHER")
    # subset adds nothing the base lacks -> base is returned untouched.
    assert _merge_masters([base, subset]) is base


def test_real_merge_blanks_signature() -> None:
    base = _master(["M-0001"], "SIG-BASE")
    other = _master(["M-0002"], "SIG-OTHER")
    merged = _merge_masters([base, other])
    assert merged is not None
    text = merged.decode("utf-8")
    assert "M-0001" in text and "M-0002" in text  # union of manufacturers
    assert 'Signature=""' in text  # stale signature blanked, not shipped mismatched
    assert "SIG-BASE" not in text and "SIG-OTHER" not in text


def test_empty_returns_none() -> None:
    assert _merge_masters([]) is None
