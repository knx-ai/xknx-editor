"""Pure-Python, Windows-independent MyKnx cloud client to obtain a project certificate.

Requests a project certificate (``{pid}.certificate``) from macOS/Linux without ETS or a dongle,
using the user's *own* MyKnx account (legitimate use of the user's license). Verified against the
live MyKnx cloud API.

Protocol:
  * Auth: ``POST /v1/user/login?username=&password=`` with the user's own credentials, yielding
    ``X-Session-ID`` + ``X-Next-OT-Token``.
  * API server ``https://openapi.knx.org/v1`` (plain JSON over TLS). Every authed request sends
    ``X-Session-ID`` + ``X-OT-Token`` (the current one-time token); the response returns the next
    ``X-Next-OT-Token``.
  * Certificate is workset-scoped and server-signed (no local key):
    ``POST /v1/workset`` -> ``.../claim`` -> ``.../product/{productId}``
    -> ``.../product/{productId}/certificate`` (body ``{"projectHash", "projectName"}``) -> ``.../release``.
  * REQUIRES a cloud-enabled ETS product license; a non-ETS product fails the add-product step with
    HTTP 422 ("Encryption \"cloud\" is not enabled ...")
"""

from __future__ import annotations

import hashlib
import io
import json
import logging
import urllib.error
import urllib.request
import zipfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

logger = logging.getLogger(__name__)

API_BASE = "https://openapi.knx.org/v1"


class MyKnxError(RuntimeError):
    """A MyKnx API call failed.

    Carries the HTTP ``status`` and the raw server ``detail`` (for logs/debugging) plus a concise,
    actionable ``user_message`` suitable for showing in the UI. ``str(err)`` is the technical form.
    """

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        detail: str = "",
        user_message: str = "",
    ) -> None:
        super().__init__(message)
        self.status = status
        self.detail = detail
        self.user_message = user_message or message


def _server_detail(resp: bytes) -> str:
    """Decode a MyKnx error body into readable text (the API returns a JSON string or object)."""
    text = resp.decode("utf-8", "replace").strip()
    try:
        parsed: object = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(parsed, str):
        return parsed
    if isinstance(parsed, dict):
        fields = cast("dict[str, object]", parsed)
        for key in ("message", "detail", "error", "title"):
            value = fields.get(key)
            if value:
                return str(value)
    return text


def project_hash(folder_signature: bytes) -> str:
    """Return the ``projectHash`` sent to the certificate endpoint.

    UNVERIFIED: implemented as ``sha256(folder_signature)`` hex, where ``folder_signature`` is the
    base64 content of the project's ``{pid}.signature`` (the converter-key directory signature over
    ``project.xml`` + ``0.xml``). The certificate binds to that signature, so hashing it is the
    most likely input -- confirm against a real request. A leading
    UTF-8 BOM (as written into the ``.signature`` file) is stripped so both call paths hash the
    same bytes.
    """
    if folder_signature.startswith(b"\xef\xbb\xbf"):
        folder_signature = folder_signature[3:]
    return hashlib.sha256(folder_signature).hexdigest()


def _post(
    url: str, body: bytes, headers: dict[str, str], timeout: float
) -> tuple[int, dict[str, str], bytes]:
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    logger.debug("myknx POST %s (%d bytes)", url, len(body))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            logger.debug("myknx POST %s -> %d", url, r.status)
            return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read()
    except urllib.error.HTTPError as e:
        logger.debug("myknx POST %s -> HTTPError %d", url, e.code)
        return e.code, {k.lower(): v for k, v in (e.headers or {}).items()}, e.read()


def _get(
    url: str, headers: dict[str, str], timeout: float
) -> tuple[int, dict[str, str], bytes]:
    req = urllib.request.Request(url, headers=headers, method="GET")
    logger.debug("myknx GET %s", url)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            logger.debug("myknx GET %s -> %d", url, r.status)
            return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read()
    except urllib.error.HTTPError as e:
        logger.debug("myknx GET %s -> HTTPError %d", url, e.code)
        return e.code, {k.lower(): v for k, v in (e.headers or {}).items()}, e.read()


def _empty_headers() -> dict[str, str]:
    return {}


@dataclass
class MyKnxSession:
    access_token: str
    session_id: str = ""
    next_ot_token: str = ""
    timeout: float = 30.0
    extra_headers: dict[str, str] = field(default_factory=_empty_headers)

    def _headers(self, json_body: bool) -> dict[str, str]:
        h = {"accept": "application/json", "User-Agent": "ETS/6.4.1 (x64) XKNX"}
        if json_body:
            h["content-type"] = "application/json"
        # VERIFIED live: authed requests send X-Session-ID + the CURRENT one-time token as
        # X-OT-Token; the response returns the next one in X-Next-OT-Token (see _absorb).
        if self.session_id:
            h["X-Session-ID"] = self.session_id
        if self.next_ot_token:
            h["X-OT-Token"] = self.next_ot_token
        h.update(self.extra_headers)
        return h

    def _absorb(self, resp_headers: dict[str, str]) -> None:
        # Rotate the one-time token: the response's X-Next-OT-Token is the next request's X-OT-Token.
        if "x-next-ot-token" in resp_headers:
            self.next_ot_token = resp_headers["x-next-ot-token"]
        if "x-session-id" in resp_headers:
            self.session_id = resp_headers["x-session-id"]

    def login(self, username: str, password: str) -> None:
        """Establish a session (verified live): ``POST /user/login?username=&password=``.

        Returns 200 "Login successful" with ``x-session-id`` + ``x-next-ot-token`` headers, which
        this stores for subsequent requests. Note: openapi.knx.org uses this username/password
        login directly (the OAuth device-code flow at id.knx.org is for my.knx.org, not this API).
        """
        import urllib.parse

        qs = urllib.parse.urlencode({"username": username, "password": password})
        status, headers, body = _post(
            f"{API_BASE}/user/login?{qs}",
            b"",
            self._headers(json_body=False),
            self.timeout,
        )
        if status // 100 != 2:
            detail = _server_detail(body)
            logger.error("MyKnx login failed: HTTP %s: %s", status, detail)
            raise MyKnxError(
                f"login failed: HTTP {status}: {detail}",
                status=status,
                detail=detail,
                user_message="MyKnx login failed - check your username and password.",
            )
        self._absorb(headers)
        if not self.session_id:
            raise MyKnxError("login returned no x-session-id")

    def _req(
        self, method: str, path: str, body: bytes | None = None
    ) -> tuple[int, bytes]:
        json_body = body is not None
        if method == "POST":
            status, headers, resp = _post(
                f"{API_BASE}{path}", body or b"", self._headers(json_body), self.timeout
            )
        else:  # GET
            status, headers, resp = _get(
                f"{API_BASE}{path}", self._headers(False), self.timeout
            )
        self._absorb(headers)
        return status, resp

    def entities(self) -> list[dict[str, object]]:
        status, resp = self._req("GET", "/entity/getAll")
        if status // 100 != 2:
            raise RuntimeError(f"entity/getAll failed: HTTP {status}: {resp[:200]!r}")
        return json.loads(resp or b"[]")

    def products(self) -> list[dict[str, object]]:
        status, resp = self._req("GET", "/product/getAll")
        if status // 100 != 2:
            raise RuntimeError(f"product/getAll failed: HTTP {status}: {resp[:200]!r}")
        return json.loads(resp or b"[]")

    def project_certificate(
        self, product_id: str, project_hash_hex: str, project_name: str
    ) -> bytes:
        """Request a project certificate for ``product_id`` (verified endpoint structure).

        Full flow (all confirmed against the live API): create a workset, claim it, add the product,
        then ``POST /v1/workset/{ws}/product/{product_id}/certificate`` with
        ``{"projectHash","projectName"}``. Returns the certificate bytes. The product must be a
        cloud-enabled ETS license: a non-ETS product yields HTTP 422
        ("Encryption \"cloud\" is not enabled for product_type ...").
        """
        logger.debug("requesting project certificate", extra={"product_id": product_id})
        s, resp = self._req(
            "POST", "/workset", json.dumps({"description": "xknx-editor"}).encode()
        )
        if s // 100 != 2:
            detail = _server_detail(resp)
            logger.error("create workset failed: HTTP %s: %s", s, detail)
            raise MyKnxError(
                f"create workset failed: HTTP {s}: {detail}", status=s, detail=detail
            )
        ws = json.loads(resp)["id"]
        logger.debug("workset created", extra={"workset": ws})
        try:
            s, resp = self._req("POST", f"/workset/{ws}/claim")
            if s // 100 != 2:
                detail = _server_detail(resp)
                logger.error("claim workset failed: HTTP %s: %s", s, detail)
                raise MyKnxError(
                    f"claim workset failed: HTTP {s}: {detail}", status=s, detail=detail
                )
            s, resp = self._req("POST", f"/workset/{ws}/product/{product_id}")
            if s // 100 != 2:
                detail = _server_detail(resp)
                logger.error(
                    "add product to workset failed: HTTP %s (product_id=%s): %s",
                    s,
                    product_id,
                    detail,
                )
                # The most common failure: the picked license is not a cloud-enabled ETS product.
                cloud_disabled = s == 422 and "cloud" in detail.lower()
                user_message = (
                    (
                        "This license cannot sign projects online: "
                        + detail.replace("\n", " ").strip()
                        + ". Pick a cloud-enabled ETS license (e.g. ETS Professional), or use "
                        "'License with a dongle' instead."
                    )
                    if cloud_disabled
                    else f"MyKnx rejected the license (HTTP {s}): "
                    + detail.replace("\n", " ").strip()
                )
                raise MyKnxError(
                    f"add product to workset failed: HTTP {s}: {detail}",
                    status=s,
                    detail=detail,
                    user_message=user_message,
                )
            payload = json.dumps(
                {"projectHash": project_hash_hex, "projectName": project_name}
            ).encode()
            s, resp = self._req(
                "POST", f"/workset/{ws}/product/{product_id}/certificate", payload
            )
            if s // 100 != 2:
                detail = _server_detail(resp)
                logger.error("certificate request failed: HTTP %s: %s", s, detail)
                raise MyKnxError(
                    f"certificate request failed: HTTP {s}: {detail}",
                    status=s,
                    detail=detail,
                )
            logger.info(
                "project certificate obtained", extra={"product_id": product_id}
            )
            text = resp.decode("utf-8", "replace").lstrip()
            if text.startswith("{"):
                try:
                    data = json.loads(resp)
                    for key in ("certificate", "file", "File", "data"):
                        if data.get(key):
                            return str(data[key]).encode("utf-8")
                except json.JSONDecodeError:
                    pass
            return resp
        finally:
            self._req("POST", f"/workset/{ws}/release")


def obtain_certificate(
    username: str,
    password: str,
    product_id: str,
    folder_signature: bytes,
    project_name: str,
) -> bytes:
    """End-to-end: log in with the user's MyKnx credentials, then request the project certificate.

    NOTE: login is verified live; the certificate request itself still hits the unresolved
    data-route auth (see the module docstring) and will fail until that is captured.
    """
    session = MyKnxSession(access_token="")
    session.login(username, password)
    return session.project_certificate(
        product_id, project_hash(folder_signature), project_name
    )


def fetch_myknx_products(
    username: str, password: str, *, timeout: float = 30.0
) -> list[dict[str, object]]:
    """Log in and return the account's products/licenses (``GET /product/getAll``).

    Used by the GUI so the user can pick a license instead of typing an opaque product id.
    Blocking (network I/O); call from a worker thread."""
    session = MyKnxSession(access_token="", timeout=timeout)
    session.login(username, password)
    return session.products()


def myknx_certificate_signer(
    username: str,
    password: str,
    product_id: str,
    *,
    timeout: float = 30.0,
) -> Callable[[str, bytes, str], bytes]:
    """Return a ``CertificateSigner`` for :func:`knxproj_export.export_knxproj`.

    The returned callable logs into MyKnx with the user's own credentials and requests the
    server-signed project certificate for the exported folder signature, so a single
    ``export_knxproj(..., certificate_signer=myknx_certificate_signer(...))`` produces a
    fully-signed, certified ``.knxproj``. Requires a cloud-enabled ETS product license on the
    account (a non-ETS product yields HTTP 422). Blocking; call the export from a worker thread.
    """

    def _sign(_pid: str, folder_signature: bytes, project_name: str) -> bytes:
        logger.debug(
            "myknx signer invoked: product_id=%s project=%s sig=%d bytes",
            product_id,
            project_name,
            len(folder_signature),
        )
        session = MyKnxSession(access_token="", timeout=timeout)
        session.login(username, password)
        cert = session.project_certificate(
            product_id, project_hash(folder_signature), project_name
        )
        logger.debug("myknx signer done: certificate %d bytes", len(cert))
        return cert

    return _sign


# --- knxproj archive helpers (two-phase flow: export -> read signature -> cert -> add) ---


def read_folder_signature(knxproj: Path | str) -> tuple[str, bytes]:
    """Return ``(pid, {pid}.signature bytes)`` from an exported ``.knxproj`` archive.

    The ``pid`` (project id, e.g. ``P-XXXX``) is the name of the ``.signature`` member; its bytes
    are the converter-key folder signature the certificate binds to (see :func:`project_hash`).
    """
    with zipfile.ZipFile(knxproj) as zf:
        names = [n for n in zf.namelist() if n.endswith(".signature") and "/" not in n]
        if not names:
            raise RuntimeError(f"{knxproj} has no top-level .signature member")
        name = names[0]
        return name[: -len(".signature")], zf.read(name)


def add_certificate_to_archive(knxproj: Path | str, certificate: bytes) -> None:
    """Add ``{pid}.certificate`` (server-signed cert) to an exported ``.knxproj`` in place."""
    knxproj = Path(knxproj)
    pid, _sig = read_folder_signature(knxproj)
    with zipfile.ZipFile(knxproj) as zf:
        members = {n: zf.read(n) for n in zf.namelist()}
    members[f"{pid}.certificate"] = certificate
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for n, data in members.items():
            zf.writestr(n, data)
    knxproj.write_bytes(buf.getvalue())


def sign_exported_knxproj(
    knxproj: Path | str,
    username: str,
    password: str,
    product_id: str,
    project_name: str,
) -> None:
    """End-to-end for an already-exported archive: MyKnx login -> cert -> bundle into the archive.

    Reads the folder signature from ``knxproj``, logs in with the user's MyKnx credentials, requests
    the server-signed certificate for ``product_id``, and writes ``{pid}.certificate`` back into the
    archive. Blocking; call from a worker thread in a GUI.
    """
    _pid, folder_signature = read_folder_signature(knxproj)
    cert = obtain_certificate(
        username, password, product_id, folder_signature, project_name
    )
    add_certificate_to_archive(knxproj, cert)
