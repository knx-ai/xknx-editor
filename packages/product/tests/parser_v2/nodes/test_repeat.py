from xknxmono.models.intermediate import Repeat
from xknxmono.product.parser_v2.nodes import DynamicNode, EvalContext, GlobalState
from xknxmono.product.parser_v2.nodes.repeat import RepeatNode
from xknxmono.product.parser_v2.ui import UiNode
from xknxmono.product.parser_v2.ui.separator import UiSeparator

_BASE = "M-0008_A-7072-21-5CC3-O000A"
_PARAM_REF = f"{_BASE}_P-1_R-1"
_REPEAT_ID = f"{_BASE}_X-1"


def _repeat(
    count: int = 0,
    param_ref_id: str | None = None,
    children: list[DynamicNode | None] | None = None,
) -> RepeatNode:
    return RepeatNode(
        Repeat(id=_REPEAT_ID, name="", count=count, parameter_ref_id=param_ref_id),
        children or [],
    )


class UiLeaf(DynamicNode):
    """Stub leaf that returns one UiSeparator so we can count iterations."""

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        return [UiSeparator(id="item", text=None)]


class IndexCapture(DynamicNode):
    """Records the repeat_idx of each eval() call."""

    def __init__(self) -> None:
        self.seen: list[int] = []

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        self.seen.append(ctx._repeat_idx)
        return []


class TestCount:
    def test_static_count_returned_directly(self):
        node = _repeat(count=3)
        assert node._count(EvalContext(GlobalState())) == 3

    def test_zero_count_with_no_param_returns_zero(self):
        node = _repeat(count=0)
        assert node._count(EvalContext(GlobalState())) == 0

    def test_dynamic_count_read_from_state(self):
        node = _repeat(count=0, param_ref_id=_PARAM_REF)
        assert node._count(EvalContext(GlobalState({_PARAM_REF: "5"}))) == 5

    def test_dynamic_count_missing_param_returns_zero(self):
        node = _repeat(count=0, param_ref_id=_PARAM_REF)
        assert node._count(EvalContext(GlobalState())) == 0

    def test_dynamic_count_non_integer_value_returns_zero(self):
        node = _repeat(count=0, param_ref_id=_PARAM_REF)
        assert node._count(EvalContext(GlobalState({_PARAM_REF: "off"}))) == 0

    def test_static_count_takes_precedence_over_param(self):
        node = _repeat(count=2, param_ref_id=_PARAM_REF)
        assert node._count(EvalContext(GlobalState({_PARAM_REF: "99"}))) == 2


class TestEval:
    def test_zero_count_returns_empty(self):
        assert (
            _repeat(count=0, children=[UiLeaf()]).eval(EvalContext(GlobalState())) == []
        )

    def test_repeated_n_times(self):
        result = _repeat(count=3, children=[UiLeaf()]).eval(EvalContext(GlobalState()))
        assert len(result) == 3

    def test_none_children_filtered(self):
        result = _repeat(count=2, children=[None, UiLeaf(), None]).eval(
            EvalContext(GlobalState())
        )
        assert len(result) == 2

    def test_multiple_children_all_included_per_iteration(self):
        result = _repeat(count=2, children=[UiLeaf(), UiLeaf()]).eval(
            EvalContext(GlobalState())
        )
        assert len(result) == 4

    def test_dynamic_count_drives_iterations(self):
        state = GlobalState({_PARAM_REF: "4"})
        result = _repeat(count=0, param_ref_id=_PARAM_REF, children=[UiLeaf()]).eval(
            EvalContext(state)
        )
        assert len(result) == 4

    def test_indices_start_at_one(self):
        capture = IndexCapture()
        _repeat(count=3, children=[capture]).eval(EvalContext(GlobalState()))
        assert capture.seen == [1, 2, 3]

    def test_each_iteration_gets_own_repeat_ctx(self):
        capture = IndexCapture()
        _repeat(count=4, children=[capture]).eval(EvalContext(GlobalState()))
        assert capture.seen == [1, 2, 3, 4]
