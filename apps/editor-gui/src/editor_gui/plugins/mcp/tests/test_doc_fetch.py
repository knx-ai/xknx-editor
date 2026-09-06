"""The documentation fetcher must stay a documentation fetcher, not an SSRF proxy.

``catalog_docs_fetch`` downloads from an allowlist of manufacturer/KNX/GitHub hosts. If redirects
were followed automatically, that allowlist would only constrain the URL we *ask* for, not the host
we end up reading from — an allowlisted (or taken-over, or simply open-redirecting) site could bounce
the fetch to an intranet address, and the body would reach the model as a manufacturer's manual.
"""

from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest
from fastmcp.exceptions import ToolError

from editor_gui.plugins.mcp.tools import catalog

_ALLOWED = "https://knx.org/manual.pdf"
_ALLOWED_ELSEWHERE = "https://raw.githubusercontent.com/o/r/main/manual.md"
_INTERNAL = "http://169.254.169.254/latest/meta-data/"

_PDF = b"%PDF-1.7 body"


def _install(
    monkeypatch: pytest.MonkeyPatch, handler: Callable[[httpx.Request], httpx.Response]
) -> list[str]:
    """Route ``_http_get`` through a mock transport; returns the list of URLs actually requested."""
    seen: list[str] = []

    def _recording(request: httpx.Request) -> httpx.Response:
        seen.append(str(request.url))
        return handler(request)

    real_client = httpx.Client

    def _factory(**kwargs: object) -> httpx.Client:
        kwargs.pop("follow_redirects", None)
        return real_client(
            transport=httpx.MockTransport(_recording),
            follow_redirects=False,
            **kwargs,  # type: ignore[arg-type]
        )

    # ``_http_get`` imports httpx lazily and calls ``httpx.Client(...)``, so patching the module
    # attribute is what reaches it.
    monkeypatch.setattr(httpx, "Client", _factory)
    return seen


def test_plain_download_still_works(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = _install(monkeypatch, lambda req: httpx.Response(200, content=_PDF))
    assert catalog._http_get(_ALLOWED) == _PDF
    assert seen == [_ALLOWED]


def test_redirect_within_the_allowlist_is_followed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == _ALLOWED:
            return httpx.Response(302, headers={"Location": _ALLOWED_ELSEWHERE})
        return httpx.Response(200, content=_PDF)

    seen = _install(monkeypatch, handler)
    assert catalog._http_get(_ALLOWED) == _PDF
    assert seen == [_ALLOWED, _ALLOWED_ELSEWHERE]


def test_redirect_off_the_allowlist_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The redirect target must never be requested — checking it after the fact is not enough."""

    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == _ALLOWED:
            return httpx.Response(302, headers={"Location": _INTERNAL})
        raise AssertionError(f"must not have fetched {request.url}")

    seen = _install(monkeypatch, handler)
    with pytest.raises(ToolError, match="not allowlisted"):
        catalog._http_get(_ALLOWED)
    assert seen == [_ALLOWED]


def test_redirect_loop_terminates(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = _install(
        monkeypatch,
        lambda req: httpx.Response(302, headers={"Location": _ALLOWED}),
    )
    with pytest.raises(ToolError, match="too many redirects"):
        catalog._http_get(_ALLOWED)
    assert len(seen) == catalog._MAX_REDIRECTS
