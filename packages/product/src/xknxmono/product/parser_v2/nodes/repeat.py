from __future__ import annotations

from xknxmono.models.intermediate import Repeat

from ..context import EvalContext
from ..ui import UiNode
from .base import DynamicNode


class RepeatNode(DynamicNode):
    """Container: repeats its children N times, each under its own repeat context.

    N comes from count, or from a parameter value when count=0 and parameter_ref_id is set.
    Index substitution for non-Module direct children is not yet implemented.
    """

    def __init__(
        self,
        elem: Repeat,
        children: list[DynamicNode | None],
        widget_param_refs: set[str] | None = None,
    ):
        self._elem = elem
        self._children = children
        # See ChooseWhenNode: only a count parameter that is also rendered as a widget can be "active",
        # so only such a gate is pushed onto the capture chain (chain-AND activeness).
        self._widget_param_refs = widget_param_refs

    def _count(self, ctx: EvalContext) -> int:
        if self._elem.count != 0:
            return self._elem.count
        if self._elem.parameter_ref_id:
            try:
                return int(ctx.get(self._elem.parameter_ref_id) or "0")
            except ValueError:
                return 0
        return 0

    def _active(self) -> list[DynamicNode]:
        return [c for c in self._children if c is not None]

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        result: list[UiNode] = []
        capture = ctx.capture
        # A parameter-driven instance count gates the objects this Repeat produces; put that parameter
        # on the capture's gate chain while evaluating the iterations (see EvalCapture / chain-AND).
        count_param = self._elem.parameter_ref_id if capture is not None else None
        gating = bool(count_param) and (
            self._widget_param_refs is None or count_param in self._widget_param_refs
        )
        if gating and count_param:
            capture.push(count_param)  # type: ignore[union-attr]
        try:
            for i in range(1, self._count(ctx) + 1):
                rctx = ctx.repeat_ctx(i)
                for c in self._active():
                    result.extend(c.eval(rctx))
        finally:
            if gating and count_param:
                capture.pop()  # type: ignore[union-attr]
        return result
