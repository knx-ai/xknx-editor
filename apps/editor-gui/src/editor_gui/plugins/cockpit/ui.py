"""Commissioning cockpit: a site-wide device table with catalog/health status and jump-to-device."""

from __future__ import annotations

from collections.abc import Callable

from imgui_bundle import imgui

from editor_gui.plugins.cockpit.service import CockpitRow, CockpitService
from editor_gui.plugins.cockpit.strings import S
from editor_gui.widgets.filter_box import filter_box
from editor_gui.widgets.text_util import text_clipped_tooltip

_ATTENTION_COLOR = imgui.ImVec4(1.0, 0.75, 0.3, 1.0)
_OK_COLOR = imgui.ImVec4(0.45, 0.8, 0.5, 1.0)


class CockpitPanel:
    def __init__(
        self,
        service: CockpitService,
        on_select: Callable[[int], None],
        is_open: Callable[[], bool],
    ) -> None:
        self._service = service
        self._on_select = on_select
        self._is_open = is_open
        self._filter = ""
        self._attention_only = False

    def render(self) -> None:
        if not self._is_open():
            imgui.text_disabled(S.COCKPIT_EMPTY)
            return
        skipped = self._service.skipped_count()
        if skipped:
            imgui.text_colored(
                _ATTENTION_COLOR, S.COCKPIT_SKIPPED.format(count=skipped)
            )
        _, self._attention_only = imgui.checkbox(
            S.COCKPIT_ATTENTION_ONLY, self._attention_only
        )
        self._filter = filter_box("##cockpit_filter", S.COCKPIT_SEARCH, self._filter)

        needle = self._filter.lower().strip()
        rows = [r for r in self._service.rows() if self._matches(r, needle)]
        self._render_table(rows)

    def _matches(self, r: CockpitRow, needle: str) -> bool:
        if self._attention_only and not r.needs_attention:
            return False
        if not needle:
            return True
        return (
            needle in r.name.lower()
            or needle in r.individual_address.lower()
            or needle in r.product_name.lower()
            or needle in r.order_number.lower()
            or needle in r.commissioning.lower()
        )

    def _render_table(self, rows: list[CockpitRow]) -> None:
        flags = (
            imgui.TableFlags_.row_bg
            | imgui.TableFlags_.borders_inner_h
            | imgui.TableFlags_.scroll_y
            | imgui.TableFlags_.resizable
        )
        avail = imgui.get_content_region_avail()
        if not imgui.begin_table("##cockpit", 5, flags, imgui.ImVec2(avail.x, avail.y)):
            return
        imgui.table_setup_scroll_freeze(0, 1)
        imgui.table_setup_column(
            S.COCKPIT_COL_ADDRESS, imgui.TableColumnFlags_.width_fixed, 70.0
        )
        imgui.table_setup_column(
            S.COCKPIT_COL_NAME, imgui.TableColumnFlags_.width_stretch, 0.4
        )
        imgui.table_setup_column(
            S.COCKPIT_COL_PRODUCT, imgui.TableColumnFlags_.width_stretch, 0.4
        )
        imgui.table_setup_column(
            S.COCKPIT_COL_LOADED, imgui.TableColumnFlags_.width_fixed, 90.0
        )
        imgui.table_setup_column(
            S.COCKPIT_COL_STATUS, imgui.TableColumnFlags_.width_stretch, 0.2
        )
        imgui.table_headers_row()
        for i, r in enumerate(rows):
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            if imgui.selectable(
                f"{r.individual_address or '-'}##cockpit{i}",
                False,
                imgui.SelectableFlags_.span_all_columns,
            )[0]:
                self._on_select(r.node_id)
            imgui.table_set_column_index(1)
            text_clipped_tooltip(r.name)
            imgui.table_set_column_index(2)
            text_clipped_tooltip(r.product_name or r.order_number or "-", disabled=True)
            imgui.table_set_column_index(3)
            text_clipped_tooltip(r.commissioning or "-", disabled=True)
            if r.commissioning_tooltip and imgui.is_item_hovered():
                imgui.set_tooltip(r.commissioning_tooltip)
            imgui.table_set_column_index(4)
            if r.needs_attention:
                imgui.text_colored(_ATTENTION_COLOR, f"! {len(r.issues)}")
                if imgui.is_item_hovered():
                    imgui.set_tooltip("\n".join(r.issues))
            else:
                imgui.text_colored(_OK_COLOR, S.COCKPIT_OK)
        imgui.end_table()
