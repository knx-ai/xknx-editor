"""Small text helpers shared across panels."""

from __future__ import annotations

from imgui_bundle import imgui


def text_clipped_tooltip(text: str, *, disabled: bool = False) -> None:
    """Render ``text`` and, when it is clipped by the current column/region, show the full value
    as a tooltip on hover. Use in table cells whose content can overflow (decoded values, names)."""
    avail = imgui.get_content_region_avail().x
    if disabled:
        imgui.text_disabled(text)
    else:
        imgui.text(text)
    if text and imgui.is_item_hovered() and imgui.calc_text_size(text).x > avail:
        imgui.set_tooltip(text)
