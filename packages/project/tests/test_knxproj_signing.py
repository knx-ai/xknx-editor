"""Tests for the folder-signature audit (knxproj_signing).

Flat folders are signed byte-exact (verified elsewhere against genuine ETS archives). Here we
cover the audit that ensures every folder in an archive carries a signature and reports the ones
we cannot verify offline (nested/baggage folders, whose ETS digest order needs Windows-NLS
collation).
"""

from __future__ import annotations

from xknxmono.project.core.knxproj_signing import (
    audit_and_sign_folders,
    directory_signature,
    nls_directory_signature,
    verify_directory_signature,
)


def test_verify_roundtrip_flat() -> None:
    files = {"project.xml": b"<a/>", "0.xml": b"<b/>"}
    sig = directory_signature(files)
    assert verify_directory_signature(files, sig)
    # tampered content no longer verifies
    assert not verify_directory_signature({**files, "0.xml": b"<c/>"}, sig)
    # garbage signature is rejected, not crashing
    assert not verify_directory_signature(files, b"not-base64!!")


def test_audit_signs_flat_folder_without_signature() -> None:
    members = {"P-1/project.xml": b"<a/>", "P-1/0.xml": b"<b/>"}
    audit = audit_and_sign_folders(members)
    assert audit.signed == ["P-1"]
    assert audit.unverifiable == []
    assert "P-1.signature" in members
    assert verify_directory_signature(
        {"project.xml": b"<a/>", "0.xml": b"<b/>"}, members["P-1.signature"]
    )


def test_audit_keeps_valid_flat_signature() -> None:
    files = {"project.xml": b"<a/>"}
    members = {"P-1/project.xml": b"<a/>", "P-1.signature": directory_signature(files)}
    audit = audit_and_sign_folders(members)
    assert audit.signed == []
    assert audit.unverifiable == []


def test_audit_resigns_invalid_flat_signature() -> None:
    members = {"P-1/project.xml": b"<a/>", "P-1.signature": b"stale-wrong"}
    audit = audit_and_sign_folders(members)
    assert audit.signed == ["P-1"]
    assert verify_directory_signature(
        {"project.xml": b"<a/>"}, members["P-1.signature"]
    )


def test_audit_keeps_valid_nested_signature() -> None:
    # A nested folder whose signature already verifies (NLS order, covered charset) is untouched.
    files = {"Catalog.xml": b"<c/>", "Baggages/icon.png": b"\x89PNG"}
    valid = nls_directory_signature(files)
    assert valid is not None
    members = {
        "M-0083/Catalog.xml": b"<c/>",
        "M-0083/Baggages/icon.png": b"\x89PNG",
        "M-0083.signature": valid,
    }
    audit = audit_and_sign_folders(members)
    assert audit.signed == []
    assert audit.unverifiable == []
    assert members["M-0083.signature"] == valid


def test_audit_resigns_invalid_nested_signature() -> None:
    # Covered charset: an invalid nested signature is replaced with a reproducible, valid one.
    members = {
        "M-0083/Catalog.xml": b"<c/>",
        "M-0083/Baggages/icon.png": b"\x89PNG",
        "M-0083.signature": b"stale-wrong",
    }
    audit = audit_and_sign_folders(members)
    assert audit.signed == ["M-0083"]
    assert audit.unverifiable == []
    assert verify_directory_signature(
        {"Catalog.xml": b"<c/>", "Baggages/icon.png": b"\x89PNG"},
        members["M-0083.signature"],
    )


def test_audit_reports_nested_folder_with_uncovered_characters() -> None:
    # A file name with a character outside the embedded NLS table cannot be ordered offline.
    members = {
        "M-0083/Catalog.xml": b"<c/>",
        "M-0083/Baggages/あ.png": b"\x89PNG",  # U+3042 hiragana, not in the table
    }
    audit = audit_and_sign_folders(members)
    assert audit.signed == []
    assert audit.unverifiable == ["M-0083"]
    assert "M-0083.signature" in members  # best-effort still written
