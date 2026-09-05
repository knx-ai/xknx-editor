"""Best-effort resolution of a KNX device's manual/documentation URL.

Shared by the MCP catalog tools (manufacturer-domain map) and the project "Download PDF manual"
button (full resolver). Everything is done with ``httpx`` — no browser engine — so it is cheap enough
to ship in the desktop app.

Resolution strategy (best effort, all steps optional, returns the first hit):
1. KNX device database: search ``www.knx.org/de/gerate?title=<order>``, open the first device page,
   and take its documentation PDF if the manufacturer uploaded one; otherwise note the manufacturer
   website the page links.
2. Otherwise a DuckDuckGo ``site:<manufacturer-domain>`` search for the order number, using the first
   result (the manufacturer's product/manual page).
3. Otherwise the manufacturer website / homepage, if known.

Returns a direct URL to open, or ``None`` if nothing could be resolved (the caller then falls back to
the KNX search page so the button always does something).
"""

from __future__ import annotations

import re
from urllib.parse import quote_plus, unquote, urlparse

import structlog

_log = structlog.get_logger("doc_links")

# Official domains for common KNX manufacturers, keyed by a lowercase substring of the catalog
# manufacturer name. Basis is the online catalog manufacturer list; domains verified 2026-09. This is
# the single source of truth — the MCP catalog tools import it from here.
#
# domain_for returns the FIRST matching key, so order matters: put the more specific key first where
# one name contains another (e.g. "ABB AG - BUSCH-JAEGER" must hit "busch" before "abb"). Short,
# ambiguous keys are qualified (e.g. "ise gmbh", "insta gmbh") so they do not match unrelated names.
MANUFACTURER_DOMAINS: dict[str, str] = {
    "siemens": "siemens.com",
    "busch": "busch-jaeger.de",
    "abb": "abb.com",
    "jung": "jung.de",
    "berker": "berker.com",
    "gira": "gira.com",
    "hager": "hager.com",
    "insta gmbh": "insta.de",
    "legrand": "legrand.com",
    "merten": "merten.de",
    "gewiss": "gewiss.com",
    "feller": "feller.ch",
    "vimar": "vimar.com",
    "theben": "theben.de",
    "somfy": "somfy.com",
    "zennio": "zennio.com",
    "mdt": "mdt.de",
    "weinzierl": "weinzierl.de",
    "elsner": "elsner-elektronik.de",
    "ekinex": "ekinex.com",
    "schneider": "se.com",
    "esylux": "esylux.com",
    "steinel": "steinel.de",
    "enertex": "enertex.de",
    "lingg": "lingg-janke.de",
    "ise gmbh": "ise.de",
    "basalte": "basalte.be",
    "iddero": "iddero.com",
    "arcus": "arcus-eds.de",
    "lunatone": "lunatone.com",
    "eelectron": "eelectron.com",
    "intesis": "intesis.com",
    "divus": "divus.eu",
    "warema": "warema.de",
    "b.e.g": "beg-luxomat.com",
    "peaknx": "peaknx.com",
    "1home": "1home.io",
    "casambi": "casambi.com",
    "dinuy": "dinuy.com",
    "blumotix": "blumotix.it",
    "tapko": "tapko.de",
    "ipas": "ipas-products.com",
    "interra": "interratechnology.com",
}

_UA = {"User-Agent": "Mozilla/5.0 (compatible; xknx-editor)"}
_TIMEOUT = 20.0


def domain_for(manufacturer: str | None) -> str | None:
    if not manufacturer:
        return None
    name = manufacturer.lower()
    return next((d for kw, d in MANUFACTURER_DOMAINS.items() if kw in name), None)


def knx_search_url(order_number: str | None, manufacturer: str | None = None) -> str:
    """Direct KNX device-database search URL (server-rendered, no search engine)."""
    term = (order_number or manufacturer or "").strip()
    return f"https://www.knx.org/de/gerate?title={quote_plus(term)}"


def _get_text(url: str, params: dict[str, str] | None = None) -> str | None:
    import httpx

    try:
        with httpx.Client(
            follow_redirects=True, timeout=_TIMEOUT, headers=_UA
        ) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            return resp.text
    except Exception as exc:
        _log.debug("doc fetch failed", url=url, error=str(exc))
        return None


def _knx_device_page(order_number: str) -> str | None:
    html = _get_text("https://www.knx.org/de/gerate", {"title": order_number})
    if not html:
        return None
    slugs = re.findall(r"/de/gerate/([a-z0-9][a-z0-9-]+)", html)
    slug = next(iter(dict.fromkeys(slugs)), None)
    return f"https://www.knx.org/de/gerate/{slug}" if slug else None


def _knx_pdf(term: str) -> str | None:
    """The official documentation PDF hosted on the KNX device page found by searching ``term``.

    KNX serves uploaded manuals as ``/devices/<n>/<refs>/<lang>/download`` (no .pdf suffix), listed
    under "Technische Dokumentation" — we prefer the German one. Not every manufacturer uploads there
    (e.g. MDT does not); then this returns None and resolve_manual_url falls back to a web search. We
    deliberately do NOT use the page's "manufacturer website" link (often the useless corporate
    homepage)."""
    page = _knx_device_page(term)
    if not page:
        return None
    html = _get_text(page)
    if not html:
        return None
    downloads = re.findall(r"https?://[^\"'> ]*?/devices/[^\"'> ]*?/download", html)
    if downloads:
        german = next((u for u in downloads if "/de-DE/" in u or "/de/" in u), None)
        return german or downloads[0]
    return next(iter(re.findall(r"https?://[^\"'> ]+\.pdf\b", html, re.I)), None)


# The KNX-specific configuration document — the KNX application description (STEINEL hosts it under
# /knxappl/) or the technical manual (MDT names it "..._THB_...") — is what explains the ETS
# parameters/objects, so it beats a general operation manual and the short product datasheet.
_KNXDOC_HINTS = (
    "knxappl",
    "applikationsbeschreibung",
    "application-description",
    "thb",
    "technisches-handbuch",
    "technisches_handbuch",
    "technical-manual",
)
_DATASHEET_HINTS = ("_ds_", "-ds-", "datenblatt", "datasheet", "_db_")


def _duckduckgo_urls(query: str) -> list[str]:
    """Organic result URLs from DuckDuckGo's HTML endpoint, in order (best effort)."""
    html = _get_text("https://html.duckduckgo.com/html/", {"q": query})
    if not html:
        return []
    # Results are wrapped as //duckduckgo.com/l/?uddg=<url-encoded target>.
    urls = [unquote(u) for u in re.findall(r"uddg=([^\"&]+)", html)]
    if not urls:
        urls = re.findall(r'class="result__a"[^>]+href="([^"]+)"', html)
    return urls


def _rank(url: str) -> int | None:
    """Relevance rank of a PDF URL (lower = better), or None if it is not a PDF.

    0 = KNX config doc (application description / technical manual), 1 = other PDF (e.g. a general
    operation manual), 2 = product datasheet."""
    low = url.lower()
    if not low.endswith(".pdf"):
        return None
    if any(h in low for h in _KNXDOC_HINTS):
        return 0
    if any(h in low for h in _DATASHEET_HINTS):
        return 2
    return 1


def _on_domain(url: str, domain: str | None) -> bool:
    if not domain:
        return False
    host = (urlparse(url).hostname or "").lower()
    return host == domain or host.endswith("." + domain)


_ALL_MFR_DOMAINS = frozenset(MANUFACTURER_DOMAINS.values())


def _is_foreign_manufacturer(url: str, own_domain: str | None) -> bool:
    """True if the URL is hosted on a DIFFERENT known manufacturer's domain than own_domain.

    Guards against a search returning another maker's document (e.g. a B.E.G. application description
    for a Basalte query). Reseller/aggregator hosts are not in the map, so they are not rejected."""
    host = (urlparse(url).hostname or "").lower()
    return any(
        (host == dom or host.endswith("." + dom)) and dom != own_domain
        for dom in _ALL_MFR_DOMAINS
    )


def resolve_manual_url(
    manufacturer: str | None,
    order_number: str | None,
    product_name: str | None = None,
) -> str | None:
    """Best-effort direct URL to the device's manual/documentation, or None.

    Different manufacturers are found by different identifiers: MDT by its order number, ABB and
    STEINEL only by product name (their order numbers do not match / are placeholders). So we try
    several terms and rank documents (see _pick_pdf): KNX application description > technical manual >
    datasheet. Order:
    1. the official PDF hosted on the KNX device page (found via order number OR product name OR the
       leading model token) — best source when the manufacturer uploaded one,
    2. a web search per term for "Applikationsbeschreibung", then "Technisches Handbuch", then
       "manual", taking the best PDF (an HTML page is only a last-resort fallback),
    3. the manufacturer homepage as a last resort."""
    order = (order_number or "").strip()
    name = (product_name or "").strip()
    token = name.split()[0] if name else ""  # e.g. "JRA/S8.230.5.1" from the ABB product name
    # A bare brand word (e.g. "GIRA") is too generic for a KNX title search — it matches a random
    # device of that brand. Only keep a leading token that looks like a model code (contains a digit).
    if token and not any(ch.isdigit() for ch in token):
        token = ""
    terms = [t for t in dict.fromkeys([order, name, token]) if t]
    _log.debug(
        "resolve manual", manufacturer=manufacturer, order=order, product=name, terms=terms
    )
    if not terms:
        domain = domain_for(manufacturer)
        return f"https://{domain}" if domain else None

    for term in terms:
        pdf = _knx_pdf(term)
        if pdf:
            _log.info("manual resolved", source="knx.org", term=term, url=pdf)
            return pdf

    mfr = (manufacturer or "").strip()
    mfr_word = mfr.split()[0].lower() if mfr else ""
    domain = domain_for(manufacturer)

    def _q(key: str, suffix: str) -> str:
        # Skip the manufacturer prefix when the key already carries the brand (a product name like
        # "STEINEL sensIQ S KNX"), else prepend it (a bare order number like "AKD-0424R.02").
        prefix = "" if mfr_word and mfr_word in key.lower() else f"{mfr} "
        return f"{prefix}{key} {suffix}".strip()

    # Try both the order number AND the product name: some devices are found by order (MDT), others
    # only by name (STEINEL's order numbers are placeholders like "40078410040xx"). The KNX
    # application description is the most relevant doc, then the technical manual, then any manual.
    keys = [k for k in dict.fromkeys([order, name]) if k]
    # Search per document type. Across ALL queries keep the best candidate, ordered by (doc rank,
    # off-manufacturer-domain): a KNX config doc beats other PDFs beats a datasheet, and among equally
    # relevant docs the manufacturer's own site wins over a reseller's copy (so MDT's mdt.de technical
    # manual beats a reseller "Applikationsbeschreibung", while STEINEL's application description still
    # beats its general operation manual). A datasheet from an early query never short-circuits a later
    # manual; an HTML result page is only a last-resort fallback.
    best: tuple[int, int, str] | None = None
    fallback: str | None = None
    for suffix in ("Applikationsbeschreibung", "Technisches Handbuch", "manual"):
        for key in keys:
            urls = _duckduckgo_urls(_q(key, suffix))
            if fallback is None:
                fallback = next(
                    (u for u in urls if not _is_foreign_manufacturer(u, domain)), None
                )
            for url in urls:
                rank = _rank(url)
                if rank is None or _is_foreign_manufacturer(url, domain):
                    continue
                cand = (rank, 0 if _on_domain(url, domain) else 1, url)
                if best is None or cand[:2] < best[:2]:
                    best = cand
        if best is not None and best[0] == 0 and best[1] == 0:
            break  # a KNX config doc on the manufacturer's own site — cannot do better
    if best is not None:
        _log.info("manual resolved", source="web", rank=best[0], url=best[2])
        return best[2]
    if fallback:
        _log.info("manual: no PDF found, opening first result", url=fallback)
        return fallback
    if domain:
        _log.info("manual not found, opening manufacturer site", url=f"https://{domain}")
        return f"https://{domain}"
    _log.warning("manual not resolved", manufacturer=manufacturer, order=order)
    return None
