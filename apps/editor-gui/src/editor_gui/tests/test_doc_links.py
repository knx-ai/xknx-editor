"""Documentation-link helpers: manufacturer-domain map + best-effort manual resolver (mocked HTTP)."""

from __future__ import annotations

from typing import Any

from editor_gui import doc_links


def test_domain_for_substring_and_ordering() -> None:
    # more specific key wins where one catalog name contains another (regression guard)
    assert doc_links.domain_for("ABB AG - BUSCH-JAEGER") == "busch-jaeger.de"
    assert doc_links.domain_for("ABB AG - STOTZ-KONTAKT") == "abb.com"
    # qualified keys do not leak into unrelated names
    assert doc_links.domain_for("Instell") is None
    assert doc_links.domain_for("MDT technologies") == "mdt.de"
    assert doc_links.domain_for(None) is None


def test_knx_search_url() -> None:
    assert (
        doc_links.knx_search_url("AKH-0400.02")
        == "https://www.knx.org/de/gerate?title=AKH-0400.02"
    )


def _patch_http(monkeypatch: Any, pages: dict[str, str]) -> None:
    """Fake _get_text: return the page whose key is a substring of the requested URL. Keys must be
    unambiguous discriminators (e.g. ``gerate?title=`` for the search vs. the device slug)."""

    from urllib.parse import urlencode

    def fake(url: str, params: dict[str, str] | None = None) -> str | None:
        full = url + ("?" + urlencode(params) if params else "")
        return next((html for needle, html in pages.items() if needle in full), None)

    monkeypatch.setattr(doc_links, "_get_text", fake)


def test_resolve_prefers_knx_pdf(monkeypatch: Any) -> None:
    _patch_http(
        monkeypatch,
        {
            "gerate?title=": '<a href="/de/gerate/akh-040002-heizungsaktor">x</a>',
            "/de/gerate/akh-040002-heizungsaktor": (
                '<a href="https://www.mdt.de/download/MDT_THB_Heizungsaktor_02.pdf">PDF</a>'
            ),
        },
    )
    url = doc_links.resolve_manual_url("MDT technologies", "AKH-0400.02")
    assert url == "https://www.mdt.de/download/MDT_THB_Heizungsaktor_02.pdf"


def test_resolve_uses_knx_uploaded_pdf_prefers_german(monkeypatch: Any) -> None:
    """When KNX hosts the manual (/devices/.../download), use it and prefer the German version."""
    base = "https://www.knx.org/devices/2/M-0002_H-x_HP-y_CI-z"
    _patch_http(
        monkeypatch,
        {
            "gerate?title=": '<a href="/de/gerate/abb-dev">d</a>',
            "/de/gerate/abb-dev": (
                f'<a href="{base}/en-US/download">EN</a>'
                f'<a href="{base}/de-DE/download">DE</a>'
            ),
        },
    )
    url = doc_links.resolve_manual_url(
        "ABB", "2CDG 110 126 R0011", "JRA/S8.230.5.1 Blind/RollerShutterAct"
    )
    assert url == f"{base}/de-DE/download"


def test_resolve_falls_back_to_duckduckgo_site_search(monkeypatch: Any) -> None:
    _patch_http(
        monkeypatch,
        {
            # KNX search finds the device but its page hosts no PDF -> fall through to the search
            "gerate?title=": '<a href="/de/gerate/some-dev">d</a>',
            "/de/gerate/some-dev": "<p>no documents here</p>",
            # DuckDuckGo returns a wrapped first result (//duckduckgo.com/l/?uddg=<encoded>)
            "duckduckgo": (
                '<a class="result__a" href="//duckduckgo.com/l/?uddg='
                'https%3A%2F%2Fwww.mdt.de%2Fmanual.pdf&rut=abc">r</a>'
            ),
        },
    )
    url = doc_links.resolve_manual_url("MDT technologies", "AKH-0400.02")
    assert url == "https://www.mdt.de/manual.pdf"


def test_rank_classifies_documents() -> None:
    # KNX config docs (application description OR technical manual) rank best (0)
    assert doc_links._rank("https://steinel.de/knxappl/KNX_Applikationsbeschreibung.pdf") == 0
    assert doc_links._rank("https://www.mdt.de/download/MDT_THB_AKD.pdf") == 0
    # a general operation manual / other PDF ranks 1, a datasheet ranks 2 (worst)
    assert doc_links._rank("https://www.steinel.de/out/media/operationmanual/BDAL.pdf") == 1
    assert doc_links._rank("https://cdn.mdt-group.com/x/AKD-0424R-02_MDT_DS_DE.PDF") == 2
    # not a PDF
    assert doc_links._rank("https://www.mdt.de/produktdetail/led-controller-akd.html") is None


def test_is_foreign_manufacturer() -> None:
    # a different known manufacturer's domain is foreign; own domain and resellers/knx are not
    assert doc_links._is_foreign_manufacturer("https://www.beg-luxomat.com/x.pdf", "basalte.be")
    assert not doc_links._is_foreign_manufacturer("https://www.basalte.be/x.pdf", "basalte.be")
    assert not doc_links._is_foreign_manufacturer("https://cdn.siblik.com/x.pdf", "mdt.de")
    assert not doc_links._is_foreign_manufacturer("https://www.knx.org/x.pdf", "mdt.de")


def test_resolve_rejects_foreign_manufacturer_pdf(monkeypatch: Any) -> None:
    """A search that only returns another maker's PDF must fall back to the homepage, not that PDF."""
    _patch_http(
        monkeypatch,
        {
            "duckduckgo": (
                '<a href="//duckduckgo.com/l/?uddg='
                'https%3A%2F%2Fwww.beg-luxomat.com%2Fappl.pdf">r</a>'
            )
        },
    )
    assert (
        doc_links.resolve_manual_url("Basalte", "180-20", "Basalte Auro 180-20")
        == "https://basalte.be"
    )


def test_on_domain() -> None:
    assert doc_links._on_domain("https://www.mdt.de/x.pdf", "mdt.de") is True
    assert doc_links._on_domain("https://cdn.reseller.com/x.pdf", "mdt.de") is False
    assert doc_links._on_domain("https://x/y.pdf", None) is False


def test_resolve_returns_none_when_nothing_found(monkeypatch: Any) -> None:
    _patch_http(monkeypatch, {})  # every fetch returns None
    assert doc_links.resolve_manual_url("Totally Unknown Maker", "X-1") is None
