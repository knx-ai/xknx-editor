from __future__ import annotations

from xknxeditor.namespaces.intermediate import ParameterSeparator

from .._name import apply_text_args, fill_name
from ..context import EvalContext
from ..ui import UiNode
from ..ui.separator import UiSeparator
from .base import DynamicNode


class ParameterSeparatorNode(DynamicNode):
    """Leaf: label or divider sitting between block parameters."""

    def __init__(self, elem: ParameterSeparator):
        self._elem = elem

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        raw = self._elem.text
        if raw:
            template = apply_text_args(raw, ctx.get_arg_defaults())
            name_value = (
                ctx.get(self._elem.text_parameter_ref_id)
                if self._elem.text_parameter_ref_id
                else None
            )
            text: str | None = fill_name(template, name_value or "") or None
        else:
            text = None
        return [UiSeparator(id=self._elem.id, text=text, cell=self._elem.cell)]
