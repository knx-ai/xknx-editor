"""Tests for the packaged-app CA bundle fallback."""

from __future__ import annotations

import os
import ssl
import sys
from pathlib import Path
from typing import NamedTuple

import pytest

from editor_gui import certs


class _FakeCertifi:
    def __init__(self, path: str) -> None:
        self._path = path

    def where(self) -> str:
        return self._path


class _Paths(NamedTuple):
    """Stand-in for a ``get_default_verify_paths()`` result.

    Only ``cafile``/``capath`` matter here. At runtime both are ``None`` when the location does not
    exist on disk — the packaged-app situation — even though typeshed declares them as ``str``.
    """

    cafile: str | None
    capath: str | None


def _paths(cafile: str | None, capath: str | None) -> _Paths:
    return _Paths(cafile=cafile, capath=capath)


def test_installs_certifi_when_openssl_has_no_trust_store(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The packaged-app case: OpenSSL's compiled-in paths do not exist on the user's machine."""
    bundle = tmp_path / "cacert.pem"
    bundle.write_text("-----BEGIN CERTIFICATE-----\n", encoding="utf-8")
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)
    monkeypatch.setattr(ssl, "get_default_verify_paths", lambda: _paths(None, None))
    monkeypatch.setitem(sys.modules, "certifi", _FakeCertifi(str(bundle)))

    assert certs.ensure_ca_bundle() == str(bundle)
    assert os.environ["SSL_CERT_FILE"] == str(bundle)


def test_leaves_a_working_system_store_alone(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        ssl, "get_default_verify_paths", lambda: _paths("/etc/ssl/cert.pem", None)
    )
    assert certs.ensure_ca_bundle() is None


def test_respects_an_existing_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """An SSL_CERT_FILE the user or packager set is reflected in ``cafile`` — never overwrite it."""
    monkeypatch.setattr(
        ssl, "get_default_verify_paths", lambda: _paths("/custom/ca.pem", None)
    )
    assert certs.ensure_ca_bundle() is None


def test_capath_alone_is_enough(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        ssl, "get_default_verify_paths", lambda: _paths(None, "/etc/ssl/certs")
    )
    assert certs.ensure_ca_bundle() is None


def test_missing_certifi_is_not_fatal(monkeypatch: pytest.MonkeyPatch) -> None:
    """A source checkout without certifi must not crash at startup."""
    monkeypatch.setattr(ssl, "get_default_verify_paths", lambda: _paths(None, None))
    monkeypatch.setitem(sys.modules, "certifi", None)  # makes `import certifi` raise
    assert certs.ensure_ca_bundle() is None
