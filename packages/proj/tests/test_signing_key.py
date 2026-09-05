"""Tests for the injectable signing key and the ETS-DLL key extractor.

The signer ships a placeholder key; a genuine key can be injected at runtime. The DLL extraction is
exercised against the real ``Knx.Ets.XmlSigning.dll`` when Mono is available (skipped otherwise).
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from xknxeditor.proj import (
    KeyExtractionError,
    current_signing_key,
    extract_converter_key,
    extraction_backend,
    reset_signing_key,
    set_signing_key,
    signing_key_is_placeholder,
)
from xknxeditor.proj.core import key_extract
from xknxeditor.proj.core.knxproj_signing import (
    directory_signature,
    verify_directory_signature,
)

# Path to a real Knx.Ets.XmlSigning.dll, supplied out-of-band via env var for the extraction test.
_REAL_DLL_ENV = os.environ.get("XKNX_TEST_SIGNING_DLL", "")
_REAL_DLL = Path(_REAL_DLL_ENV) if _REAL_DLL_ENV else None


@pytest.fixture(autouse=True)
def _restore_key():
    yield
    reset_signing_key()


def test_default_is_placeholder() -> None:
    reset_signing_key()
    assert signing_key_is_placeholder()


def test_set_and_reset_signing_key() -> None:
    reset_signing_key()
    files = {"project.xml": b"<a/>"}
    placeholder_sig = directory_signature(files)

    # A different (valid) key changes the signature and clears the placeholder flag.
    set_signing_key(_TEST_N, _TEST_D, 65537)
    assert not signing_key_is_placeholder()
    assert current_signing_key() == (_TEST_N, _TEST_D, 65537)
    sig = directory_signature(files)
    assert sig != placeholder_sig
    assert verify_directory_signature(files, sig)

    reset_signing_key()
    assert signing_key_is_placeholder()
    assert directory_signature(files) == placeholder_sig


def test_extract_missing_file_raises() -> None:
    with pytest.raises(KeyExtractionError):
        extract_converter_key("/no/such/Knx.Ets.XmlSigning.dll")


@pytest.mark.skipif(
    key_extract.extraction_backend() is None
    or _REAL_DLL is None
    or not _REAL_DLL.is_file(),
    reason="set XKNX_TEST_SIGNING_DLL and have Mono/pythonnet to run this",
)
def test_extract_real_dll_roundtrip() -> None:
    assert _REAL_DLL is not None
    assert extraction_backend() in ("dotnet", "mono", "pythonnet")
    n, d, e = extract_converter_key(_REAL_DLL)
    assert e == 65537
    assert n.bit_length() == 1024
    # Feeding the extracted key makes the signer produce a self-consistent signature.
    set_signing_key(n, d, e)
    files = {"project.xml": b"<a/>", "0.xml": b"<b/>"}
    assert verify_directory_signature(files, directory_signature(files))


# A distinct, valid throwaway 1024-bit RSA keypair (e=65537) for the set/reset test.
_TEST_N = 0x985AFB0417C4FAEFB5ECA91953E5D3249B78AD96C754CA4ECCA573B1E914EBF92030DF6C25831A46396BA1B7671DEF4768DDD6891F07D53B12A99087C0BAADB7602A8E832563C515820AAF74FCB9E70C0BD95B240BC64A456AA18AACE679B793E33BCAD6E493C634CA6033356496356E95892E0313D3229F7E7D495D288C0FA3
_TEST_D = 0x2B8B7BC971482383C3036C57BC0E28BC8293234A269843CD8B735E75E306CFCB0C6D1EBB389D7E66909F9DDA924CC3FBC691FAA41FF25861151C6B5114BFDFE316F1467ABA609A043608DC21B419D6C8BF68CBF951E98F0704E3A916E514A0256E2A2F006B5AE0CAD2EDE6B989D1ABCC46440529D1C3C420435638FBB9B925D
