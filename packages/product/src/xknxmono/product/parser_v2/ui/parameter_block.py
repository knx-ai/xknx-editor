from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from xknxmono.models.intermediate.parameter_block_layout_t import ParameterBlockLayout

if TYPE_CHECKING:
    from xknxmono.product.parser_v2.ui import UiNode


@dataclass(frozen=True, slots=True)
class UiParameterBlock:
    id: str
    children: tuple[UiNode, ...]
    name: str | None = None
    text: str | None = None
    inline: bool = False
    layout: ParameterBlockLayout = ParameterBlockLayout.LIST
    row_labels: tuple[str, ...] = ()
    column_headers: tuple[str, ...] = ()
