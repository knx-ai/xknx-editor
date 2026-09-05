"""Project log view: the ETS project traces carried over on import.

Shows ProjectInformation/ProjectTraces as a filterable, sortable table. Date and User are plaintext;
the Comment is stored verbatim from the source (ETS encrypts it), so it stays opaque until the
decryption phase is wired up.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING

from imgui_bundle import imgui

from editor_gui.plugins.project.strings import S
from editor_gui.widgets.filter_box import filter_box

if TYPE_CHECKING:
    from editor_gui.plugins.project.service import _ProjectTrace


class ProjectLogPanel:
    def __init__(self, get_traces: "Callable[[], list[_ProjectTrace]]") -> None:
        self._get_traces = get_traces
        self._filter = ""
        # 0 = Date, 1 = User, 2 = Comment; default: newest first (Date descending).
        self._sort_key = 0
        self._sort_desc = True

    def render(self) -> None:
        traces = self._get_traces()
        if not traces:
            imgui.text_disabled(S.PROJECT_LOG_EMPTY)
            return

        self._filter = filter_box(
            "##project_log_filter", S.PROJECT_LOG_FILTER_HINT, self._filter
        )

        needle = self._filter.strip().lower()
        rows = [t for t in traces if not needle or self._matches(t, needle)]
        rows.sort(key=self._sort_value, reverse=self._sort_desc)

        flags = (
            imgui.TableFlags_.borders_inner
            | imgui.TableFlags_.resizable
            | imgui.TableFlags_.row_bg
            | imgui.TableFlags_.scroll_y
        )
        if not imgui.begin_table("##project_log", 3, flags):
            return
        imgui.table_setup_column(
            S.PROJECT_LOG_COL_DATE, imgui.TableColumnFlags_.width_fixed, 150.0
        )
        imgui.table_setup_column(
            S.PROJECT_LOG_COL_USER, imgui.TableColumnFlags_.width_fixed, 120.0
        )
        imgui.table_setup_column(
            S.PROJECT_LOG_COL_COMMENT, imgui.TableColumnFlags_.width_stretch, 1.0
        )
        self._sortable_header()

        for t in rows:
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            imgui.text_unformatted(t.date or "-")
            imgui.table_set_column_index(1)
            imgui.text_unformatted(t.user_name or "-")
            imgui.table_set_column_index(2)
            imgui.text_unformatted(t.comment or "-")
            if t.comment and imgui.is_item_hovered():
                imgui.set_tooltip(t.comment)
        imgui.end_table()

    def _sortable_header(self) -> None:
        """Header row whose cells are clickable to sort by that column (no imgui sort-spec API)."""
        labels = (
            S.PROJECT_LOG_COL_DATE,
            S.PROJECT_LOG_COL_USER,
            S.PROJECT_LOG_COL_COMMENT,
        )
        imgui.table_next_row(imgui.TableRowFlags_.headers)
        for col, label in enumerate(labels):
            imgui.table_set_column_index(col)
            marker = ""
            if col == self._sort_key:
                marker = " v" if self._sort_desc else " ^"
            if imgui.selectable(f"{label}{marker}##hdr{col}", False):
                self._toggle_sort(col)

    def _toggle_sort(self, col: int) -> None:
        if self._sort_key == col:
            self._sort_desc = not self._sort_desc
        else:
            self._sort_key = col
            self._sort_desc = False

    def _sort_value(self, t: "_ProjectTrace") -> str:
        if self._sort_key == 1:
            return t.user_name.lower()
        if self._sort_key == 2:
            return t.comment.lower()
        return t.date

    @staticmethod
    def _matches(t: "_ProjectTrace", needle: str) -> bool:
        return (
            needle in t.date.lower()
            or needle in t.user_name.lower()
            or needle in t.comment.lower()
        )
