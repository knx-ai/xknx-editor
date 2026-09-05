"""Unit tests for the programming queue (no bus): sequencing, dedupe, cancel, advance, visibility."""

from __future__ import annotations

from concurrent.futures import Future
from typing import Any

from editor_gui.plugins.project.program_queue import ProgramQueue, QueueItem


class _Harness:
    """Drives a ProgramQueue with a controllable bus + futures, marshaling inline (UI-thread)."""

    def __init__(self, start_returns_none: bool = False) -> None:
        self.busy = False
        self.started: list[int] = []  # node_ids in start order
        self._futures: dict[int, Future[Any]] = {}
        self._start_none = start_returns_none
        self.queue = ProgramQueue(
            is_busy=lambda: self.busy,
            start=self._start,
            submit=None,  # run advance inline
        )

    def _start(self, item: QueueItem) -> Future[Any] | None:
        if self._start_none:
            return None
        self.started.append(item.node_id)
        self.busy = True
        fut: Future[Any] = Future()
        self._futures[item.node_id] = fut
        return fut

    def finish(self, node_id: int, *, error: bool = False) -> None:
        """Complete a running device's future (bus frees, queue advances)."""
        self.busy = False
        fut = self._futures.pop(node_id)
        if error:
            fut.set_exception(RuntimeError("boom"))
        else:
            fut.set_result(None)


def _item(node_id: int, scope: str = "FULL") -> QueueItem:
    return QueueItem(
        node_id=node_id, address=f"1.1.{node_id}", name=f"D{node_id}", scope=scope
    )  # type: ignore[arg-type]


def test_idle_enqueue_starts_immediately_no_panel() -> None:
    h = _Harness()
    h.queue.enqueue(_item(1))
    assert h.started == [1]
    assert h.queue.current is not None and h.queue.current.node_id == 1
    assert h.queue.queued == []
    assert h.queue.visible is False  # a lone programming shows no panel


def test_second_press_while_busy_queues_and_shows_panel() -> None:
    h = _Harness()
    h.queue.enqueue(_item(1))  # runs
    h.queue.enqueue(_item(2))  # busy -> queued
    assert h.started == [1]
    assert [q.node_id for q in h.queue.queued] == [2]
    assert h.queue.visible is True


def test_fifo_drains_on_completion() -> None:
    h = _Harness()
    for n in (1, 2, 3):
        h.queue.enqueue(_item(n))
    assert h.started == [1]
    h.finish(1)
    assert h.started == [1, 2]
    h.finish(2)
    assert h.started == [1, 2, 3]
    h.finish(3)
    assert h.queue.current is None and h.queue.queued == []
    assert h.queue.visible is False


def test_dedupe_updates_scope_no_duplicate() -> None:
    h = _Harness()
    h.queue.enqueue(_item(1))  # running
    h.queue.enqueue(_item(2, scope="FULL"))
    h.queue.enqueue(_item(2, scope="PARAMETERS"))  # same device -> update scope, no dup
    assert [q.node_id for q in h.queue.queued] == [2]
    assert h.queue.queued[0].scope == "PARAMETERS"


def test_continue_on_error_advances() -> None:
    h = _Harness()
    h.queue.enqueue(_item(1))
    h.queue.enqueue(_item(2))
    h.finish(1, error=True)  # device 1 failed
    assert h.started == [1, 2]  # queue still advances to 2


def test_cancel_and_clear_queued() -> None:
    h = _Harness()
    for n in (1, 2, 3):
        h.queue.enqueue(_item(n))
    h.queue.cancel(2)
    assert [q.node_id for q in h.queue.queued] == [3]
    h.queue.clear_queued()
    assert h.queue.queued == []
    # the running device is untouched by cancel/clear
    assert h.queue.current is not None and h.queue.current.node_id == 1


def test_start_none_drops_and_advances() -> None:
    h = _Harness(start_returns_none=True)
    h.queue.enqueue(_item(1))
    h.queue.enqueue(_item(2))
    # neither could start; both dropped, nothing left running or queued
    assert h.queue.current is None
    assert h.queue.queued == []


def test_tick_does_not_double_start_when_busy() -> None:
    h = _Harness()
    h.queue.enqueue(_item(1))  # running, busy=True
    h.queue.enqueue(_item(2))
    h.queue.tick()  # extra frame ticks must not start a second op
    h.queue.tick()
    assert h.started == [1]
