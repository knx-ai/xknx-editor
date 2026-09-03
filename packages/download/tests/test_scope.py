"""Tests for download scope filtering (by target loadable part)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from xknxmono.download.scope import DownloadScope, control_in_scope


def _ctrl(**attrs: int) -> object:
    return SimpleNamespace(**attrs)


@pytest.mark.parametrize(
    ("control", "scope", "expected"),
    [
        # framing controls (no target object) always run
        (_ctrl(), DownloadScope.PARAMETERS, True),
        (_ctrl(), DownloadScope.GROUP_COMMUNICATION, True),
        # device object (0) is framing (fingerprint compare) -> always
        (_ctrl(obj_idx=0), DownloadScope.PARAMETERS, True),
        (_ctrl(obj_idx=0), DownloadScope.GROUP_COMMUNICATION, True),
        # group communication objects: address(1), association(2), group object(9)
        (_ctrl(obj_type=1), DownloadScope.GROUP_COMMUNICATION, True),
        (_ctrl(obj_type=2), DownloadScope.GROUP_COMMUNICATION, True),
        (_ctrl(lsm_idx=9), DownloadScope.GROUP_COMMUNICATION, True),
        (_ctrl(obj_type=1), DownloadScope.PARAMETERS, False),
        # application program object (3) holds parameters
        (_ctrl(obj_type=3), DownloadScope.PARAMETERS, True),
        (_ctrl(lsm_idx=3), DownloadScope.PARAMETERS, True),
        (_ctrl(obj_type=3), DownloadScope.GROUP_COMMUNICATION, False),
        # full download runs everything
        (_ctrl(obj_type=1), DownloadScope.FULL, True),
        (_ctrl(obj_type=3), DownloadScope.FULL, True),
        # application program: params (3) and group object table (9) run, but the
        # address (1) and association (2) tables do not.
        (_ctrl(obj_type=3), DownloadScope.APPLICATION, True),
        (_ctrl(lsm_idx=3), DownloadScope.APPLICATION, True),
        (_ctrl(obj_type=9), DownloadScope.APPLICATION, True),
        (_ctrl(obj_type=1), DownloadScope.APPLICATION, False),
        (_ctrl(obj_type=2), DownloadScope.APPLICATION, False),
        (_ctrl(obj_idx=0), DownloadScope.APPLICATION, True),
        (_ctrl(), DownloadScope.APPLICATION, True),
    ],
)
def test_control_in_scope(
    control: object, scope: DownloadScope, expected: bool
) -> None:
    assert control_in_scope(control, scope) is expected


def test_coupler_filter_table_scopes_together() -> None:
    # The coupler filter table (Router object type 6) and its clear must scope IDENTICALLY, so a
    # partial download never clears without rewriting or rewrites without clearing.
    from xknxmono.models.intermediate.ld_ctrl_clear_lcfilter_table_t import (
        LdCtrlClearLcfilterTable,
    )

    clear = LdCtrlClearLcfilterTable(use_function_prop=True)
    write = _ctrl(obj_type=6)
    for scope, expected in [
        (DownloadScope.FULL, True),
        (DownloadScope.GROUP_COMMUNICATION, True),
        (DownloadScope.PARAMETERS, False),
        (DownloadScope.APPLICATION, False),
    ]:
        assert control_in_scope(clear, scope) is expected
        assert control_in_scope(write, scope) is expected
