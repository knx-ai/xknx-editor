"""build_module_tables: pivot repeating module instances (e.g. a DALI gateway's ECGs) into a table
by grouping instance-qualified ParameterRef ids (``…_MD-x_M-y_MI-n_P-p_R-r``). Manufacturer-agnostic."""

from __future__ import annotations

from editor_gui.widgets.module_table import _column_header, build_module_tables
from xknxeditor.prod.parser_v2.ui import UiParameterBlock, UiTab
from xknxeditor.prod.parser_v2.ui.parameter import TextWidget, UiParameter


def _p(ref_id: str, label: str, value: str = "") -> UiParameter:
    return UiParameter(ref_id=ref_id, label=label, value=value, widget=TextWidget())


_APP = "M-0083_A-0155-11-FA68-O00EF"


def _ecg(n: int, desc: str = "", group: str = "0") -> UiParameterBlock:
    base = f"{_APP}_MD-4_M-3_MI-{n}"
    return UiParameterBlock(
        id=f"ecg-{n}",
        text=f"ECG {n}",
        children=(
            _p(f"{base}_P-1_R-1", f"ECG {n}, Description", desc),
            _p(f"{base}_P-2_R-1", f"ECG {n}, Group", group),
        ),
    )


def _tree() -> list:
    # Mirror the real shape: a generic top tab ("General"), a section block ("Single ECG"), then one
    # templated block per instance ("ECG {{ECG_NO}}") holding the parameters.
    return [
        UiTab(
            id="t",
            text="General",
            children=(
                _p(f"{_APP}_P-9_R-1", "Name"),  # a non-module param -> ignored
                UiParameterBlock(
                    id="sec",
                    text="Single ECG",
                    children=(
                        _ecg(1, desc="Kitchen", group="1"),
                        _ecg(2, desc="Hall", group="2"),
                        _ecg(3),
                    ),
                ),
            ),
        )
    ]


def test_pivots_instances_into_one_table() -> None:
    tables = build_module_tables(_tree())
    assert len(tables) == 1
    table = tables[0]
    assert table.key == f"{_APP}_MD-4_M-3"
    assert (
        table.title == "Single ECG"
    )  # section below the generic top tab, not a per-instance block
    assert [row.index for row in table.rows] == [1, 2, 3]  # sorted instance indices
    # Two module parameters -> two columns; the per-instance entity prefix ("ECG N,") is dropped so
    # only the field name remains (the instance number lives in the "#" row column).
    assert [c.label for c in table.columns] == ["Description", "Group"]
    # Cells bind to the instance-qualified ref id and carry the stored value.
    row1 = table.rows[0]
    assert row1.params["P-1_R-1"].value == "Kitchen"
    assert row1.params["P-1_R-1"].ref_id == f"{_APP}_MD-4_M-3_MI-1_P-1_R-1"


def test_single_instance_is_not_a_table() -> None:
    # Only one instance -> the parameter tree shows it fine; no pivot table.
    assert build_module_tables([_ecg(1)]) == []


def test_non_module_params_ignored() -> None:
    assert build_module_tables([_p(f"{_APP}_P-9_R-1", "Name")]) == []


def test_column_header_strips_instance_prefix_and_templates() -> None:
    # Substituted index varying across instances -> entity prefix dropped, field name kept.
    assert _column_header(["ECG 1, Level", "ECG 2, Level", "ECG 10, Level"]) == "Level"
    # Unsubstituted template, identical across instances -> template removed, prefix dropped.
    assert (
        _column_header(["MD {{MD_NO}}, Description", "MD {{MD_NO}}, Description"])
        == "Description"
    )
    # A field with no entity prefix is kept verbatim.
    assert _column_header(["Operating Mode", "Operating Mode"]) == "Operating Mode"
    assert _column_header([]) == ""
