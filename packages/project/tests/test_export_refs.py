"""Tests for the export-time referential-integrity audit (installation -> manufacturer bundle).

Mirrors the two dictionaries ETS's import converter builds: a missing application program or
hardware-to-program reference is what makes ETS abort with "The given key was not present in the
dictionary", so the exporter flags it up front.
"""

from __future__ import annotations

from xknxmono.project.core.knxproj_export import _audit_installation_refs


def _installation(refs: str) -> bytes:
    return f"<KNX><Installations>{refs}</Installations></KNX>".encode()


def test_clean_bundle_has_no_missing_refs() -> None:
    members = {
        "P-1/0.xml": _installation(
            '<DeviceInstance Hardware2ProgramRefId="M-0001_H-x-1_HP-1"/>'
            '<ComObjectInstanceRef RefId="M-0001_A-1-1-1_O-0_R-1"/>'
        ),
        "M-0001/M-0001_A-1-1-1.xml": b"<KNX/>",
        "M-0001/Hardware.xml": b'<KNX><Hardware2Program Id="M-0001_H-x-1_HP-1"/></KNX>',
    }
    assert _audit_installation_refs(members) == []


def test_missing_application_program_is_flagged() -> None:
    members = {
        "P-1/0.xml": _installation(
            '<ComObjectInstanceRef RefId="M-0001_A-9-9-9_O-0_R-1"/>'
        ),
        "M-0001/Hardware.xml": b"<KNX/>",
    }
    assert _audit_installation_refs(members) == ["application program M-0001_A-9-9-9"]


def test_missing_hardware2program_is_flagged() -> None:
    members = {
        "P-1/0.xml": _installation(
            '<DeviceInstance Hardware2ProgramRefId="M-0001_H-x-1_HP-9"/>'
        ),
        "M-0001/Hardware.xml": b'<KNX><Hardware2Program Id="M-0001_H-x-1_HP-1"/></KNX>',
    }
    assert _audit_installation_refs(members) == ["hardware2program M-0001_H-x-1_HP-9"]


def test_no_installation_no_refs() -> None:
    assert _audit_installation_refs({"knx_master.xml": b"<KNX/>"}) == []
