from __future__ import annotations

from xknxeditor.namespaces.intermediate import Button

from ..context import EvalContext
from ..ui import UiNode
from ..ui.button import UiButton
from .base import DynamicNode


class ButtonNode(DynamicNode):
    """A clickable button rendered inside a parameter block."""

    def __init__(self, elem: Button):
        self._elem = elem

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        return [UiButton(id=self._elem.id, text=self._elem.text)]
