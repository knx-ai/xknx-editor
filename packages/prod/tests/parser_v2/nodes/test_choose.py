from xknxeditor.prod.parser_v2.nodes import (
    ChooseWhenNode,
    DynamicNode,
    EvalContext,
    GlobalState,
)
from xknxeditor.prod.parser_v2.nodes.choose import (
    _token_matches,
    _value_matches,
    satisfies,
)
from xknxeditor.prod.parser_v2.ui import UiNode
from xknxeditor.prod.parser_v2.ui.separator import UiSeparator

_BASE = "M-0008_A-7072-21-5CC3-O000A"
_REF_MODE = f"{_BASE}_P-1_R-1"

_UI_A = UiSeparator(id="a", text=None)
_UI_B = UiSeparator(id="b", text=None)


class UiLeaf(DynamicNode):
    """Stub leaf that returns a fixed UiSeparator so we can assert which branch was taken."""

    def __init__(self, marker: UiSeparator) -> None:
        self._marker = marker

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        return [self._marker]


class TestTokenMatches:
    def test_exact_match(self):
        assert _token_matches("1", "1") is True
        assert _token_matches("1", "2") is False

    def test_greater_than(self):
        assert _token_matches("5", ">4") is True
        assert _token_matches("4", ">4") is False

    def test_greater_than_or_equal(self):
        assert _token_matches("4", ">=4") is True
        assert _token_matches("3", ">=4") is False

    def test_less_than(self):
        assert _token_matches("3", "<4") is True
        assert _token_matches("4", "<4") is False

    def test_less_than_or_equal(self):
        assert _token_matches("4", "<=4") is True
        assert _token_matches("5", "<=4") is False

    def test_non_integer_value_with_operator_returns_false(self):
        assert _token_matches("x", ">1") is False


class TestValueMatches:
    def test_matches_any_token(self):
        assert _value_matches("2", ["1", "2", "3"]) is True
        assert _value_matches("5", ["1", "2", "3"]) is False

    def test_matches_operator_token(self):
        assert _value_matches("10", [">5", "<20"]) is True


class TestSatisfies:
    def test_none_condition_returns_false(self):
        assert satisfies(None, "1") is False

    def test_space_separated_values(self):
        assert satisfies("1 2 3", "2") is True
        assert satisfies("1 2 3", "5") is False

    def test_operator_in_condition(self):
        assert satisfies(">5", "6") is True
        assert satisfies(">5", "5") is False


class TestChooseWhenNode:
    def test_eval_returns_empty_with_no_conditions_and_no_default(self):
        node = ChooseWhenNode(_REF_MODE, {}, None)
        assert node.eval(EvalContext(GlobalState({_REF_MODE: "1"}))) == []

    def test_eval_returns_matching_branch(self):
        node = ChooseWhenNode(_REF_MODE, {"1": [UiLeaf(_UI_A)]}, None)
        assert node.eval(EvalContext(GlobalState({_REF_MODE: "1"}))) == [_UI_A]

    def test_eval_falls_through_to_default(self):
        node = ChooseWhenNode(_REF_MODE, {"1": [UiLeaf(_UI_A)]}, [UiLeaf(_UI_B)])
        assert node.eval(EvalContext(GlobalState({_REF_MODE: "99"}))) == [_UI_B]

    def test_eval_default_branch_without_test_condition(self):
        node = ChooseWhenNode(_REF_MODE, {}, [UiLeaf(_UI_B)])
        assert node.eval(EvalContext(GlobalState({_REF_MODE: "anything"}))) == [_UI_B]

    def test_eval_returns_empty_when_no_match_and_no_default(self):
        node = ChooseWhenNode(_REF_MODE, {"1": [UiLeaf(_UI_A)]}, None)
        assert node.eval(EvalContext(GlobalState({_REF_MODE: "99"}))) == []

    def test_eval_uses_empty_string_for_missing_param(self):
        node = ChooseWhenNode(_REF_MODE, {"1": [UiLeaf(_UI_A)]}, None)
        assert node.eval(EvalContext(GlobalState())) == []

    def test_eval_matches_value_in_space_separated_condition(self):
        node = ChooseWhenNode(
            _REF_MODE, {"1 2 130 4 6 134 36 132": [UiLeaf(_UI_A)]}, None
        )
        assert node.eval(EvalContext(GlobalState({_REF_MODE: "130"}))) == [_UI_A]
        assert node.eval(EvalContext(GlobalState({_REF_MODE: "36"}))) == [_UI_A]
        assert node.eval(EvalContext(GlobalState({_REF_MODE: "99"}))) == []


_REF_A = f"{_BASE}_UP-1_R-1"  # a Union member's parameter-ref
_REF_B = f"{_BASE}_UP-2_R-2"  # its union sibling (same memory overlay)


class TestChooseWhenNodeUnionGating:
    """A Choose on a Union member must render only when it is the ACTIVE overlay. Union members share
    memory, so both would otherwise match the same shared value and render duplicate content. The
    active overlay is the member REACHED in the discovery pass (frozen via snapshot_discovered_active);
    the render pass suppresses a member that was not reached while a sibling was."""

    def test_inactive_union_member_renders_nothing_when_sibling_reached(self):
        node = ChooseWhenNode(_REF_A, {"0": [UiLeaf(_UI_A)]}, None, None, {_REF_B})
        state = GlobalState({_REF_A: "0", _REF_B: "0"})
        state.mark_active_param(_REF_B)  # the sibling was reached in discovery...
        state.snapshot_discovered_active()  # ...frozen as the discovery result
        assert node.eval(EvalContext(state)) == []

    def test_active_union_member_renders_normally(self):
        node = ChooseWhenNode(_REF_A, {"0": [UiLeaf(_UI_A)]}, None, None, {_REF_B})
        state = GlobalState({_REF_A: "0", _REF_B: "0"})
        state.mark_active_param(_REF_A)  # this member was reached in discovery
        state.snapshot_discovered_active()
        assert node.eval(EvalContext(state)) == [_UI_A]

    def test_no_sibling_reached_renders_normally(self):
        # Neither member reached in discovery -> do not suppress.
        node = ChooseWhenNode(_REF_A, {"0": [UiLeaf(_UI_A)]}, None, None, {_REF_B})
        assert node.eval(EvalContext(GlobalState({_REF_A: "0"}))) == [_UI_A]

    def test_discovery_pass_never_suppresses(self):
        # During discovery (union_suppress=False) both members render even when a sibling is already
        # marked active, so the reached member is recorded regardless of eval order.
        node = ChooseWhenNode(_REF_A, {"0": [UiLeaf(_UI_A)]}, None, None, {_REF_B})
        state = GlobalState({_REF_A: "0", _REF_B: "0"})
        state.mark_active_param(_REF_B)
        state.snapshot_discovered_active()
        assert node.eval(EvalContext(state, union_suppress=False)) == [_UI_A]

    def test_stale_explicit_sibling_does_not_suppress_reached_member(self):
        # Fresh-activation regression: the sibling carries a stale explicit value (imported for an
        # inactive branch), but THIS member is the one reached under the current values. The active
        # overlay is decided by the discovery result, not by which member has an explicit value, so
        # this member must render (a freshly-activated function's secondary object is not dropped).
        node = ChooseWhenNode(_REF_A, {"0": [UiLeaf(_UI_A)]}, None, None, {_REF_B})
        state = GlobalState({_REF_A: "0"})
        state.set(_REF_B, "0")  # sibling has an explicit value but is NOT reached
        state.mark_active_param(_REF_A)  # only this member reached in discovery
        state.snapshot_discovered_active()
        assert node.eval(EvalContext(state)) == [_UI_A]

    def test_non_union_choose_unaffected(self):
        # No union siblings -> a plain Choose ignores discovery state entirely.
        node = ChooseWhenNode(_REF_MODE, {"1": [UiLeaf(_UI_A)]}, None)
        state = GlobalState({_REF_MODE: "1"})
        state.mark_active_param(_REF_A)
        state.snapshot_discovered_active()
        assert node.eval(EvalContext(state)) == [_UI_A]
