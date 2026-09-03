from __future__ import annotations

from abc import ABC, abstractmethod

from ..context import EvalContext
from ..ui import UiNode


class DynamicNode(ABC):
    """Base class for all nodes in the dynamic evaluation tree.

    eval(ctx) is the single method: it fires side effects (mark_active_param,
    mark_active_com_object, set_text, set) and returns the UI nodes produced by
    this node and its active children. Containers flatmap their children's results;
    leaves return [] (side-effect only) or [UiNode] (visible element).
    """

    @abstractmethod
    def eval(self, ctx: EvalContext) -> list[UiNode]: ...
