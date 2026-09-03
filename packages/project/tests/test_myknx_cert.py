"""Error surfacing for the MyKnx certificate flow.

The workset flow fails with HTTP 422 when the picked license is not a cloud-enabled ETS product.
That must raise a typed :class:`MyKnxError` carrying the raw server ``detail`` (for logs) and a
concise, actionable ``user_message`` (for the UI), not an opaque ``bytes`` repr.
"""

from __future__ import annotations

import pytest

from xknxmono.project.core import myknx_cert
from xknxmono.project.core.myknx_cert import MyKnxError, MyKnxSession, _server_detail

_CLOUD_422 = (
    b'"Cannot add product to workset:\\nEncryption \\"cloud\\" is not enabled for '
    b'product_type KNX Specifications"'
)


def test_server_detail_unwraps_json_string() -> None:
    assert _server_detail(b'"boom"') == "boom"
    assert _server_detail(b'{"message": "nope"}') == "nope"
    assert _server_detail(b"not json") == "not json"


def _fake_post(url: str, body: bytes, headers: dict[str, str], timeout: float):
    if url.endswith("/workset"):
        return 200, {}, b'{"id": "WS1"}'
    if url.endswith("/claim"):
        return 200, {}, b""
    if url.endswith("/product/PROD"):
        return 422, {}, _CLOUD_422
    if url.endswith("/release"):
        return 200, {}, b""
    raise AssertionError(f"unexpected POST {url}")


def test_cloud_disabled_license_raises_actionable_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(myknx_cert, "_post", _fake_post)
    session = MyKnxSession(access_token="", session_id="S1", next_ot_token="T1")
    with pytest.raises(MyKnxError) as excinfo:
        session.project_certificate("PROD", "deadbeef", "Demo")
    err = excinfo.value
    assert err.status == 422
    assert "KNX Specifications" in err.detail  # raw server text kept for logs
    assert "dongle" in err.user_message.lower()  # points the user at the workaround
    assert "\\n" not in err.user_message  # newlines flattened for a one-line toast
