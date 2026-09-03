"""Floating "Programming queue" window, shown while devices wait behind the running one.

Rendered each frame from ``main.py`` (like the bus-operation overlay) only when the queue has
waiting items, so a lone programming shows nothing new. It carries the running device's progress, so
the standalone overlay is suppressed while this is visible (no double progress bar).
"""

from __future__ import annotations

from collections.abc import Callable

from imgui_bundle import imgui

from editor_gui.plugins.project.program_queue import QueueItem
from editor_gui.plugins.project.strings import S


class ProgramQueuePanel:
    def __init__(
        self,
        *,
        get_current: Callable[[], QueueItem | None],
        get_queued: Callable[[], list[QueueItem]],
        get_progress: Callable[[], tuple[int, int] | None],
        on_cancel: Callable[[int], None],
        on_clear: Callable[[], None],
    ) -> None:
        self._get_current = get_current
        self._get_queued = get_queued
        self._get_progress = get_progress
        self._on_cancel = on_cancel
        self._on_clear = on_clear

    def render(self) -> None:
        vp = imgui.get_main_viewport()
        pos = imgui.ImVec2(
            vp.work_pos.x + vp.work_size.x - 12.0,
            vp.work_pos.y + vp.work_size.y - 12.0,
        )
        imgui.set_next_window_pos(pos, imgui.Cond_.always, imgui.ImVec2(1.0, 1.0))
        imgui.set_next_window_bg_alpha(0.92)
        imgui.set_next_window_size_constraints(
            imgui.ImVec2(320.0, 0.0), imgui.ImVec2(560.0, 400.0)
        )
        flags = (
            imgui.WindowFlags_.no_saved_settings
            | imgui.WindowFlags_.always_auto_resize
            | imgui.WindowFlags_.no_focus_on_appearing
            | imgui.WindowFlags_.no_nav
            | imgui.WindowFlags_.no_docking
            | imgui.WindowFlags_.no_collapse
        )
        if not imgui.begin(f"{S.PROGRAM_QUEUE_TITLE}###program_queue", None, flags)[0]:
            imgui.end()
            return

        current = self._get_current()
        if current is not None:
            progress = self._get_progress()
            frac = (
                progress[0] / progress[1]
                if progress is not None and progress[1] > 0
                else None
            )
            imgui.text_colored(
                imgui.ImVec4(0.3, 0.8, 0.4, 1.0),
                f"> {current.address}  {current.name}  [{current.scope.name}]",
            )
            if frac is not None:
                imgui.same_line()
                imgui.progress_bar(frac, imgui.ImVec2(120.0, 0.0))

        queued = self._get_queued()
        for pos, item in enumerate(queued, start=1):
            imgui.push_id(item.node_id)
            imgui.text_disabled(
                f"{pos}.  {item.address}  {item.name}  [{item.scope.name}]  "
                f"{S.PROGRAM_QUEUE_QUEUED}"
            )
            imgui.same_line()
            if imgui.small_button(f"{S.PROGRAM_QUEUE_REMOVE}##cancel"):
                self._on_cancel(item.node_id)
            imgui.pop_id()

        if queued:
            imgui.separator()
            if imgui.button(S.PROGRAM_QUEUE_CLEAR):
                self._on_clear()
        imgui.end()
