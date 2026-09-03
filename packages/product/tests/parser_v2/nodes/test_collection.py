from xknxmono.product.parser_v2.nodes import (
    DynamicNode,
    EvalContext,
    GenericCollectionNode,
    GlobalState,
)
from xknxmono.product.parser_v2.ui import UiNode
from xknxmono.product.parser_v2.ui.separator import UiSeparator


class UiLeaf(DynamicNode):
    """Stub leaf that produces one UiSeparator so we can verify it was included."""

    def __init__(self, id: str) -> None:
        self._id = id

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        return [UiSeparator(id=self._id, text=None)]


class TestGenericCollectionNode:
    def test_eval_empty_children_returns_empty_list(self):
        node = GenericCollectionNode([])
        assert node.eval(EvalContext(GlobalState())) == []

    def test_eval_flatmaps_children(self):
        a = UiLeaf("a")
        b = UiLeaf("b")
        result = GenericCollectionNode([a, b]).eval(EvalContext(GlobalState()))
        assert result == [
            UiSeparator(id="a", text=None),
            UiSeparator(id="b", text=None),
        ]

    def test_eval_filters_none_children(self):
        a = UiLeaf("a")
        result = GenericCollectionNode([a, None]).eval(EvalContext(GlobalState()))
        assert result == [UiSeparator(id="a", text=None)]

    def test_eval_recurses_into_nested_collection(self):
        leaf = UiLeaf("x")
        inner = GenericCollectionNode([leaf])
        outer = GenericCollectionNode([inner])
        result = outer.eval(EvalContext(GlobalState()))
        assert result == [UiSeparator(id="x", text=None)]
