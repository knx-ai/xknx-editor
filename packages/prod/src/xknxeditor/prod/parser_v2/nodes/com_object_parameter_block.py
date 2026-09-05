from __future__ import annotations

from xknxeditor.namespaces.intermediate.application_program_channel_t import (
    ComObjectParameterBlock,
)

from .._name import apply_text_args, fill_name
from ..context import EvalContext
from ..ui import UiNode
from ..ui.parameter_block import UiParameterBlock
from .base import DynamicNode


class ComObjectParameterBlockNode(DynamicNode):
    """A grouped box of parameters (dynamic-XML ParameterBlock)."""

    __slots__ = ("_children", "_elem", "_heading_text")

    def __init__(
        self,
        elem: ComObjectParameterBlock,
        children: list[DynamicNode | None],
        heading_text: str | None = None,
    ) -> None:
        self._elem = elem
        self._children = children
        # The resolved Text of the block's heading parameter (its ``ParamRefId``), if that parameter
        # carries one. The importer labels the block with this Text (e.g. a channel-prefixed "A: Drive") in
        # preference to the block's own Name (which may be a generic template like "Jalousie X: …").
        self._heading_text = heading_text

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        items = [u for c in self._children if c for u in c.eval(ctx)]
        arg_defaults = ctx.get_arg_defaults()
        text_ref = self._elem.text_parameter_ref_id
        name_value = ctx.get(text_ref) if text_ref else None
        template = (
            ctx.get_text(self._elem.id)
            or self._heading_text
            or self._elem.text
            or self._elem.name
        )
        text = (
            fill_name(apply_text_args(template or "", arg_defaults), name_value or "")
            or None
        )
        rows = self._elem.rows
        cols = self._elem.columns
        row_labels = (
            tuple(
                apply_text_args(r.text or r.name or "", arg_defaults) for r in rows.row
            )
            if rows
            else ()
        )
        column_headers = (
            tuple(
                apply_text_args(c.text or c.name or "", arg_defaults)
                for c in cols.column
            )
            if cols
            else ()
        )
        return [
            UiParameterBlock(
                id=self._elem.id,
                name=self._elem.name,
                text=text,
                inline=self._elem.inline,
                layout=self._elem.layout,
                children=tuple(items),
                row_labels=row_labels,
                column_headers=column_headers,
            )
        ]
