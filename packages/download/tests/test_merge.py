"""Tests for Load Procedure resolution (default / product / merged styles)."""

from __future__ import annotations

from types import SimpleNamespace
from typing import cast

from xknxeditor.download.merge import resolve_download_controls
from xknxeditor.namespaces.intermediate.ld_ctrl_connect_t import LdCtrlConnect
from xknxeditor.namespaces.intermediate.ld_ctrl_merge_t import LdCtrlMerge
from xknxeditor.namespaces.intermediate.ld_ctrl_restart_t import LdCtrlRestart
from xknxeditor.namespaces.intermediate.ld_ctrl_write_mem_t import LdCtrlWriteMem
from xknxeditor.namespaces.intermediate.load_procedure_style_t import LoadProcedureStyle
from xknxeditor.namespaces.intermediate.load_procedures_t import LoadProcedures
from xknxeditor.namespaces.intermediate.load_procedures_t_load_procedure import (
    LoadProceduresLoadProcedure,
)
from xknxeditor.namespaces.intermediate.master_data_t import MasterData
from xknxeditor.namespaces.intermediate.procedure_type_t import ProcedureType

_MASK = "MV-0705"


def _application(style: LoadProcedureStyle, *fragments: object) -> object:
    return SimpleNamespace(
        load_procedure_style=style,
        load_procedures=LoadProcedures(load_procedure=list(fragments)),  # type: ignore[arg-type]
        program=SimpleNamespace(mask_version=_MASK),
    )


def _master_with_default(*controls: object) -> MasterData:
    default = SimpleNamespace(procedure_type=ProcedureType.LOAD, choice=list(controls))
    mask = SimpleNamespace(
        id=_MASK,
        hawk_configuration_data=[
            SimpleNamespace(procedures=SimpleNamespace(procedure=[default]))
        ],
    )
    return cast(
        "MasterData",
        SimpleNamespace(mask_versions=SimpleNamespace(mask_version=[mask])),
    )


def _fragment(merge_id: int, *controls: object) -> LoadProceduresLoadProcedure:
    return LoadProceduresLoadProcedure(merge_id=merge_id, choice=list(controls))  # type: ignore[arg-type]


def test_product_procedure_uses_application_controls() -> None:
    application = _application(
        LoadProcedureStyle.PRODUCT_PROCEDURE,
        _fragment(0, LdCtrlConnect(), LdCtrlRestart()),
    )
    controls = resolve_download_controls(cast("object", application))  # type: ignore[arg-type]
    assert [type(c).__name__ for c in controls] == ["LdCtrlConnect", "LdCtrlRestart"]


def test_merged_procedure_splices_fragments_into_default() -> None:
    master = _master_with_default(
        LdCtrlConnect(),
        LdCtrlMerge(merge_id=2),
        LdCtrlMerge(merge_id=4),
        LdCtrlRestart(),
    )
    write = LdCtrlWriteMem(address=0x10, size=1, verify=False, inline_data=b"\x01")
    application = _application(
        LoadProcedureStyle.MERGED_PROCEDURE,
        _fragment(2, LdCtrlConnect()),
        _fragment(4, write),
    )

    controls = resolve_download_controls(cast("object", application), master)  # type: ignore[arg-type]

    # Connect, <frag 2: Connect>, <frag 4: WriteMem>, Restart
    assert [type(c).__name__ for c in controls] == [
        "LdCtrlConnect",
        "LdCtrlConnect",
        "LdCtrlWriteMem",
        "LdCtrlRestart",
    ]


def test_default_procedure_drops_unmatched_merge_placeholders() -> None:
    master = _master_with_default(
        LdCtrlConnect(), LdCtrlMerge(merge_id=9), LdCtrlRestart()
    )
    application = _application(LoadProcedureStyle.DEFAULT_PROCEDURE)

    controls = resolve_download_controls(cast("object", application), master)  # type: ignore[arg-type]

    # no fragment for merge id 9 -> placeholder dropped
    assert [type(c).__name__ for c in controls] == ["LdCtrlConnect", "LdCtrlRestart"]


def test_merged_without_master_falls_back_to_application() -> None:
    application = _application(
        LoadProcedureStyle.MERGED_PROCEDURE,
        _fragment(0, LdCtrlConnect()),
    )
    controls = resolve_download_controls(cast("object", application))  # type: ignore[arg-type]
    assert [type(c).__name__ for c in controls] == ["LdCtrlConnect"]


def _master_with_unload(*controls: object) -> MasterData:
    unload = SimpleNamespace(procedure_type=ProcedureType.UNLOAD, choice=list(controls))
    mask = SimpleNamespace(
        id=_MASK,
        hawk_configuration_data=[
            SimpleNamespace(procedures=SimpleNamespace(procedure=[unload]))
        ],
    )
    return cast(
        "MasterData",
        SimpleNamespace(mask_versions=SimpleNamespace(mask_version=[mask])),
    )


def test_unload_uses_master_default_not_application_load_procedure() -> None:
    # A ProductProcedure app ships only its Load procedure; UNLOAD must come from
    # the master default, never the application's (Load) controls.
    application = _application(
        LoadProcedureStyle.PRODUCT_PROCEDURE,
        _fragment(
            0, LdCtrlWriteMem(address=0x10, size=1, verify=False, inline_data=b"\x01")
        ),
    )
    master = _master_with_unload(LdCtrlConnect(), LdCtrlRestart())
    controls = resolve_download_controls(
        cast("object", application), master, procedure_type=ProcedureType.UNLOAD
    )  # type: ignore[arg-type]
    assert [type(c).__name__ for c in controls] == ["LdCtrlConnect", "LdCtrlRestart"]


def test_unload_without_master_raises() -> None:
    import pytest

    from xknxeditor.download.errors import UnsupportedProcedureError

    application = _application(
        LoadProcedureStyle.PRODUCT_PROCEDURE,
        _fragment(0, LdCtrlConnect()),
    )
    with pytest.raises(UnsupportedProcedureError, match=r"[Uu]nload procedure"):
        resolve_download_controls(
            cast("object", application), None, procedure_type=ProcedureType.UNLOAD
        )  # type: ignore[arg-type]
