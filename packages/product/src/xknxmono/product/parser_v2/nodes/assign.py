from __future__ import annotations

from xknxmono.models.intermediate import Assign

from ..context import EvalContext
from ..ui import UiNode
from .base import DynamicNode


class AssignNode(DynamicNode):
    """Leaf: assigns a fixed value to a parameter — no visible UI element, affects state only."""

    def __init__(self, elem: Assign):
        self._elem = elem

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        if self._elem.value is not None:
            ctx.set(self._elem.target_param_ref_ref, self._elem.value)
        elif self._elem.source_param_ref_ref is not None:
            value = ctx.get(self._elem.source_param_ref_ref)
            if value is not None:
                ctx.set(self._elem.target_param_ref_ref, value)
        return []
