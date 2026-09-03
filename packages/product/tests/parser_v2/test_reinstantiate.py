"""com-object re-instantiation basis:

1. Integration: `DynamicUI.eval_unpruned_ui()` on a real application returns a stable, non-empty
   parameter-driven com-object set (used for the before/after diff on a parameter edit).
2. Unit: the `ChooseWhenNode` gating mechanism `eval_unpruned_ui` relies on routes com-objects by
   parameter value, so a function/mode change moves objects in and out of the set."""

from pathlib import Path

import pytest

from xknxmono.product import load
from xknxmono.product.parser_v2.context import EvalCapture
from xknxmono.product.parser_v2.dynamic import DynamicUI
from xknxmono.product.parser_v2.nodes.base import DynamicNode
from xknxmono.product.parser_v2.nodes.choose import ChooseWhenNode
from xknxmono.product.parser_v2.ui import UiComObject, UiNode, UiParameterBlock, UiTab

_FIXTURE = (
    Path(__file__).parent.parent / "fixtures" / "gira_2gang_button_interface.knxprod"
)
_APP_ID = "M-0008_A-7072-21-5CC3-O000A"


def _co_refs(nodes: list[UiNode]) -> set[str]:
    out: set[str] = set()
    for node in nodes:
        if isinstance(node, UiComObject):
            out.add(node.ref_id)
        elif isinstance(node, (UiTab, UiParameterBlock)):
            out |= _co_refs(list(node.children))
    return out


@pytest.fixture()
def dui() -> DynamicUI:
    app = load(_FIXTURE.read_bytes()).applications[_APP_ID]
    d = app.dynamic_ui()
    assert d is not None
    return d


def test_eval_unpruned_is_deterministic_and_nonempty(dui: DynamicUI) -> None:
    a = _co_refs(dui.eval_unpruned_ui())
    b = _co_refs(dui.eval_unpruned_ui())
    assert a and a == b  # returns the current param-driven set, stable across calls


class _CoLeaf(DynamicNode):
    """Minimal com-object leaf: records itself into the capture (like ComObjectRefRefNode) and emits a
    UiComObject."""

    def __init__(self, ref_id: str) -> None:
        self._ref_id = ref_id

    def eval(self, ctx: object) -> list[UiNode]:  # type: ignore[override]
        cap = getattr(ctx, "capture", None)
        if cap is not None:
            cap.record_object(self._ref_id)
        return [
            UiComObject(
                ref_id=self._ref_id,
                name=self._ref_id,
                function_text="",
                number=0,
                dpt_codes=(),
                object_size="",
                priority="",
                communication=True,
                read=False,
                write=False,
                transmit=False,
                update=False,
                read_on_init=False,
                read_locked=False,
                write_locked=False,
                transmit_locked=False,
                update_locked=False,
                read_on_init_locked=False,
            )
        ]


class _Ctx:
    """Stub EvalContext: Choose/Repeat/leaf eval need get(ref_id), capture and repeat_ctx."""

    def __init__(
        self, values: dict[str, str], capture: EvalCapture | None = None
    ) -> None:
        self._values = values
        self.capture = capture

    def get(self, ref_id: str) -> str:
        return self._values.get(ref_id, "")

    def repeat_ctx(self, _i: int) -> "_Ctx":
        return self  # same scope (carries the capture) for the synthetic test


def test_choose_routes_com_objects_by_parameter() -> None:
    node = ChooseWhenNode(
        param_ref_id="P",
        condition_to_nodes={"0": [_CoLeaf("co-a")], "1": [_CoLeaf("co-b")]},
        default_nodes=None,
    )
    before = _co_refs(node.eval(_Ctx({"P": "0"})))  # type: ignore[arg-type]
    after = _co_refs(node.eval(_Ctx({"P": "1"})))  # type: ignore[arg-type]
    assert before == {"co-a"}
    assert after == {"co-b"}
    assert (
        after != before
    )  # a function/mode change moves com-objects in and out of the set


def test_choose_records_gate_chain_for_tracked_param() -> None:
    node = ChooseWhenNode(
        param_ref_id="P",
        condition_to_nodes={"0": [_CoLeaf("co-a")], "1": [_CoLeaf("co-b")]},
        default_nodes=None,
    )
    cap = EvalCapture("P")  # only record emissions gated by P
    node.eval(_Ctx({"P": "1"}, cap))  # type: ignore[arg-type]
    assert cap.controlled_ref_ids() == {"co-b"}
    assert cap.chains["co-b"] == [frozenset({"P"})]

    other = EvalCapture("Q")  # tracking a different param records nothing
    node.eval(_Ctx({"P": "1"}, other))  # type: ignore[arg-type]
    assert other.controlled_ref_ids() == set()


def test_chain_and_activeness_excludes_inactive_outer_gate() -> None:
    # Object under an inactive OUTER choose but active INNER choose must be EXCLUDED; a fully-active
    # chain and an ungated object must be INCLUDED (mirrors RGB grouping: A/B/C dropped, D kept).
    inner = ChooseWhenNode("INNER", {"0": [_CoLeaf("co-gated")]}, None)
    tree = ChooseWhenNode(
        "OUTER",
        {"1": [inner, _CoLeaf("co-ungated-under-active")]},
        None,
    )
    cap = EvalCapture(None)
    tree.eval(_Ctx({"OUTER": "1", "INNER": "0"}, cap))  # type: ignore[arg-type]
    # co-gated chain = {OUTER, INNER}; co-ungated-under-active chain = {OUTER}
    assert cap.chains["co-gated"] == [frozenset({"OUTER", "INNER"})]
    # OUTER inactive: nothing qualifies.
    assert cap.active_ref_ids(frozenset({"INNER"})) == set()
    # OUTER active but INNER inactive: only the object whose whole chain is active.
    assert cap.active_ref_ids(frozenset({"OUTER"})) == {"co-ungated-under-active"}
    # Both active: everything.
    assert cap.active_ref_ids(frozenset({"OUTER", "INNER"})) == {
        "co-gated",
        "co-ungated-under-active",
    }


def test_non_widget_gate_does_not_disqualify_object() -> None:
    # A Choose gated by a param that is NEVER rendered as a widget (not in widget_param_refs) must not
    # push its gate — else it would disqualify every object under it, since it can never be "active"
    # (the ABB dummy-selector case). A widget-eligible gate IS pushed and gates activeness normally.
    struct = ChooseWhenNode("STRUCT", {"1": [_CoLeaf("co-a")]}, None, widget_param_refs=set())
    cap = EvalCapture(None)
    struct.eval(_Ctx({"STRUCT": "1"}, cap))  # type: ignore[arg-type]
    assert cap.chains["co-a"] == [frozenset()]  # gate not pushed -> empty chain
    assert cap.active_ref_ids(frozenset()) == {"co-a"}  # active despite no active params

    widget = ChooseWhenNode(
        "WIDGET", {"1": [_CoLeaf("co-b")]}, None, widget_param_refs={"WIDGET"}
    )
    cap2 = EvalCapture(None)
    widget.eval(_Ctx({"WIDGET": "1"}, cap2))  # type: ignore[arg-type]
    assert cap2.chains["co-b"] == [frozenset({"WIDGET"})]
    assert cap2.active_ref_ids(frozenset()) == set()  # needs WIDGET active
    assert cap2.active_ref_ids(frozenset({"WIDGET"})) == {"co-b"}


def test_ungated_object_always_active() -> None:
    cap = EvalCapture(None)
    _CoLeaf("co-global").eval(_Ctx({}, cap))  # type: ignore[arg-type]
    assert cap.chains["co-global"] == [frozenset()]
    assert cap.active_ref_ids(frozenset()) == {"co-global"}  # empty chain ⊆ anything


def test_repeat_records_gate_chain_for_count_param() -> None:
    from xknxmono.models.intermediate import Repeat
    from xknxmono.product.parser_v2.nodes.repeat import RepeatNode

    # count=0 -> the instance count comes from parameter "N"
    node = RepeatNode(
        Repeat(id="R", name="rep", count=0, parameter_ref_id="N"), [_CoLeaf("co-r")]
    )
    cap = EvalCapture("N")
    node.eval(_Ctx({"N": "2"}, cap))  # type: ignore[arg-type]
    assert cap.controlled_ref_ids() == {"co-r"}
    assert cap.chains["co-r"] == [frozenset({"N"}), frozenset({"N"})]  # two iterations
