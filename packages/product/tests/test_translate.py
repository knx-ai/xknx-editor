"""Tests for the KNX language-translation overlay (:mod:`xknxmono.product.translate`)."""

from pathlib import Path

from xknxmono.models import detect_version
from xknxmono.models.intermediate.language_data_t import LanguageData
from xknxmono.product.archive import Archive
from xknxmono.product.data import to_ir
from xknxmono.product.translate import (
    _index_by_id,
    _pick_language,
    apply_translations,
)

_FIXTURE = Path(__file__).parent / "fixtures" / "gira_2gang_button_interface.knxprod"


def _lang(identifier: str) -> LanguageData:
    return LanguageData(identifier=identifier, translation_unit=[])


def test_pick_language_exact_and_prefix() -> None:
    langs = [_lang("en-US"), _lang("de-DE"), _lang("fr-FR")]
    # Exact identifier wins.
    assert _pick_language(langs, "de-DE") is langs[1]
    # A bare language code matches its region variant.
    assert _pick_language(langs, "de") is langs[1]
    assert _pick_language(langs, "en") is langs[0]
    # No match -> None (caller leaves the inline default text).
    assert _pick_language(langs, "it") is None


def test_apply_translations_overlays_texts() -> None:
    with Archive(str(_FIXTURE)) as archive:
        mid = sorted(archive.manufacturer_ids)[0]
        _app_id, xml = next(iter(archive.get_application_xmls(mid).items()))

    version = detect_version(xml)
    knx = to_ir(xml, version)
    manufacturer = knx.manufacturer_data.manufacturer[0]  # type: ignore[union-attr]

    # The fixture ships en-US; overlaying it must run cleanly and keep element texts populated.
    before = _index_by_id(manufacturer)
    apply_translations(knx, "en")
    after = _index_by_id(manufacturer)

    assert before.keys() == after.keys()
    assert any(getattr(obj, "text", None) for obj in after.values())


def test_apply_translations_unknown_language_is_noop() -> None:
    with Archive(str(_FIXTURE)) as archive:
        mid = sorted(archive.manufacturer_ids)[0]
        _app_id, xml = next(iter(archive.get_application_xmls(mid).items()))

    version = detect_version(xml)
    knx = to_ir(xml, version)
    texts_before = {
        k: getattr(v, "text", None)
        for k, v in _index_by_id(knx.manufacturer_data.manufacturer[0]).items()  # type: ignore[union-attr]
    }
    apply_translations(knx, "zz")  # no such language
    texts_after = {
        k: getattr(v, "text", None)
        for k, v in _index_by_id(knx.manufacturer_data.manufacturer[0]).items()  # type: ignore[union-attr]
    }
    assert texts_before == texts_after
