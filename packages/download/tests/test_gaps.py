"""Tests for the implementation-gap registry and its diagnostic messages."""

from __future__ import annotations

from types import SimpleNamespace
from typing import cast

import pytest

from xknxeditor.download import gaps
from xknxeditor.download.errors import UnsupportedProcedureError
from xknxeditor.download.image import DownloadImage
from xknxeditor.download.procedure import LoadProcedureRunner
from xknxeditor.download.programmer import DeviceProgrammer

from .conftest import FakeDevice

if True:  # keep import used for typing without a runtime dependency cycle
    from xknxeditor.prod import Application


def test_known_gap_message_names_standard_service() -> None:
    message = gaps.describe_missing("LdCtrlOnError")
    assert "LdCtrlOnError" in message
    assert "load procedure error-branch" in message
    assert "KNX Standard v3.0.0" in message


def test_unknown_control_message_flags_registry() -> None:
    message = gaps.describe_missing("LdCtrlSomethingBrandNew")
    assert "not recognised" in message
    assert "gaps.py" in message


def test_supported_task_controls_listed_in_preflight_no_write() -> None:
    # These controls are executed but emit load-state/segment events with nothing for a read-only
    # preflight to diff. They must appear in PREFLIGHT_NO_WRITE under their real xsdata class name,
    # or the preflight logs a spurious "cannot preview / not recognised" warning (the old stale
    # "LdCtrlTaskCtrl" without the 1/2 suffix never matched).
    for name in (
        "LdCtrlTaskCtrl1",
        "LdCtrlTaskCtrl2",
        "LdCtrlTaskSegment",
        "LdCtrlTaskPtr",
        "LdCtrlRelSegment",
    ):
        assert name in gaps.PREFLIGHT_NO_WRITE


def test_known_gaps_are_never_silently_skipped_in_preflight() -> None:
    # A control that is a known implementation gap must not also be in the
    # no-write set, otherwise preflight would hide it instead of logging it.
    assert gaps.KNOWN_GAPS.keys().isdisjoint(gaps.PREFLIGHT_NO_WRITE)


def test_registry_excludes_implemented_controls() -> None:
    # Controls the runner executes must not be listed as gaps.
    for implemented in ("LdCtrlWriteMem", "LdCtrlWriteProp", "LdCtrlLoad"):
        assert implemented not in gaps.KNOWN_GAPS


def _application(*controls: object) -> Application:
    fake = SimpleNamespace(
        load_procedures=None,
        manufacturer_id="M-0072",
        program=SimpleNamespace(
            pei_type=1, application_number=1, application_version=1
        ),
    )
    return cast("Application", fake)


async def test_unsupported_control_error_is_diagnostic() -> None:
    class LdCtrlBrandNew:  # a control the runner does not handle
        pass

    application = _application()
    runner = LoadProcedureRunner(
        application,
        DownloadImage(segments=(), properties=()),
        DeviceProgrammer(FakeDevice()),
        controls=[LdCtrlBrandNew()],
    )

    with pytest.raises(UnsupportedProcedureError) as excinfo:
        await runner.run()

    message = str(excinfo.value)
    assert "LdCtrlBrandNew" in message
    assert "in-scope load control 1/1" in message
    assert "bug report" in message
    assert "app=" in message
