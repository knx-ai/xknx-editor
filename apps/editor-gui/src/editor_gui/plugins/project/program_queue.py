"""A tiny FIFO that serialises repeated "Program" presses onto the single KNX bus slot.

The bus has one exclusive operation slot (``ConnectionService.begin_operation``), so a second
programming started while one runs would be rejected. This queue instead appends it and drains the
queue one device at a time, reusing the normal single-device path (``connection.program_device``)
verbatim — so slot handling, progress, the completion notice and commissioning recording are
unchanged.

Threading: ``enqueue``/``tick``/``cancel``/``clear_queued`` run on the UI thread. The only callback
from the async loop thread is the future's completion, which is marshalled back onto the UI thread
via ``submit`` before advancing — so all state lives on and is mutated from the UI thread only.
"""

from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import Future
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from xknxeditor.download.scope import DownloadScope


@dataclass
class QueueItem:
    node_id: int
    address: str
    name: str
    scope: DownloadScope


class ProgramQueue:
    """Serialises programmings. ``is_busy() -> bool`` reports whether any bus op is running;
    ``start(item) -> Future | None`` starts one programming (``None`` = could not start); ``submit``
    marshals a callable onto the UI thread (``None`` runs it inline, for tests)."""

    def __init__(
        self,
        *,
        is_busy: Callable[[], bool],
        start: Callable[[QueueItem], Future[Any] | None],
        submit: Callable[[Callable[[], None]], Any] | None = None,
    ) -> None:
        self._is_busy = is_busy
        self._start = start
        self._submit = submit
        self._current: QueueItem | None = None
        self._queued: list[QueueItem] = []

    @property
    def current(self) -> QueueItem | None:
        return self._current

    @property
    def queued(self) -> list[QueueItem]:
        return list(self._queued)

    @property
    def visible(self) -> bool:
        """The queue UI is shown only once something waits behind the running device."""
        return len(self._queued) >= 1

    def enqueue(self, item: QueueItem) -> None:
        """Add a device to program. Dedupe per device: re-pressing a queued device only updates its
        scope (no duplicate); re-pressing the running device queues exactly one reprogram."""
        for queued in self._queued:
            if queued.node_id == item.node_id:
                queued.scope = item.scope
                self.tick()
                return
        self._queued.append(item)
        self.tick()

    def cancel(self, node_id: int) -> None:
        """Remove a *queued* device (the running one cannot be interrupted)."""
        self._queued = [q for q in self._queued if q.node_id != node_id]

    def clear_queued(self) -> None:
        self._queued.clear()

    def tick(self) -> None:
        """Start the next queued device if the bus is free. Idempotent; safe to call every frame."""
        if self._current is not None or self._is_busy() or not self._queued:
            return
        item = self._queued.pop(0)
        self._current = item
        future = self._start(item)
        if future is None:
            # Could not start (e.g. not connected / device gone): drop it and try the next.
            self._current = None
            self.tick()
            return
        future.add_done_callback(lambda _f: self._on_done())

    def _on_done(self) -> None:
        # Fires on the async loop thread -> marshal the advance onto the UI thread.
        if self._submit is not None:
            self._submit(self._advance)
        else:
            self._advance()

    def _advance(self) -> None:
        self._current = None
        self.tick()
