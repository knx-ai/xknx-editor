from __future__ import annotations

from xknxeditor.namespaces.intermediate import BinaryDataRef

from ..context import EvalContext
from ..ui import UiNode
from .base import DynamicNode


class BinaryDataRefNode(DynamicNode):
    """Points at a static binary blob from the application program."""

    def __init__(self, elem: BinaryDataRef):
        self._elem = elem

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        return []
