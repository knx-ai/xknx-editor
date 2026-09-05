from __future__ import annotations

from abc import ABC, abstractmethod

from ..context import EvalContext
from ..ui import UiNode


class DynamicNode(ABC):
    """Root type for the dynamic tree; one eval(ctx) per node.

    eval applies its side effects and yields the UiNodes from this node plus its
    active children. Containers concatenate child output; leaves give [] or one node.
    """

    @abstractmethod
    def eval(self, ctx: EvalContext) -> list[UiNode]: ...
