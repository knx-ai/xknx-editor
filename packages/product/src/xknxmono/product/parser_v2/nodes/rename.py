from __future__ import annotations

from xknxmono.models.intermediate import Rename

from .._name import apply_text_args
from ..context import EvalContext
from ..ui import UiNode
from .base import DynamicNode


class RenameNode(DynamicNode):
    """Leaf: overrides the display text of a ComObjectParameterBlock within a choose branch."""

    __slots__ = ("_elem",)

    def __init__(self, elem: Rename):
        self._elem = elem

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        text = apply_text_args(self._elem.text, ctx.get_arg_defaults())
        ctx.set_text(self._elem.ref_id, text)
        return []
