"""A tiny guard for service reads during a background import.

A long ``.knxproj`` import runs on a worker thread that mutates the catalog and project databases.
The GUI panels read those same services every frame on the UI thread. To keep the UI responsive
without racing the writer, the importer holds a shared *re-entrant* lock for the whole import, and
every per-frame service read is wrapped with :func:`io_guarded`: it acquires the lock without
blocking and, if the importer holds it, returns an empty placeholder instead of touching the
database. Because the lock is re-entrant, the importing thread itself (which already holds it) still
reads real data while building the project view.
"""

from __future__ import annotations

import queue
from collections.abc import Callable
from concurrent.futures import Future
from functools import wraps
from typing import Any, cast


class MainThreadExecutor:
    """Run callables on the imgui main thread and hand their result back to any thread.

    The GUI's ``project``/``catalog`` services wrap non-thread-safe SQLAlchemy sessions and per-frame
    caches, so a background caller (the embedded MCP server on its own thread) must not touch them
    directly. Instead it submits a callable here and blocks on the returned :class:`Future`; the main
    thread drains the queue once per frame via :meth:`drain` and fulfils each future. This serialises
    background access with the GUI's own per-frame reads and writes on a single thread.

    ``drain`` must be called from the main thread each frame; ``submit`` is safe from any thread.
    """

    def __init__(self) -> None:
        self._queue: queue.Queue[tuple[Callable[[], Any], Future[Any]]] = queue.Queue()

    def submit[T](self, fn: Callable[[], T]) -> Future[T]:
        """Queue ``fn`` for execution on the main thread; return a future for its result."""
        future: Future[T] = Future()
        self._queue.put((fn, future))
        return future

    def run[T](self, fn: Callable[[], T], *, timeout: float = 30.0) -> T:
        """Submit ``fn`` and block until the main thread has produced its result (or it raises).

        On timeout the task is cancelled so it cannot still run on a later frame after the caller has
        given up — otherwise a "failed" mutation could silently take effect afterwards. Cancellation
        is best-effort: if the main thread has already started the task, it runs to completion."""
        future = self.submit(fn)
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            future.cancel()
            raise

    def drain(self) -> None:
        """Execute all queued callables on the calling (main) thread. Call once per frame."""
        while True:
            try:
                fn, future = self._queue.get_nowait()
            except queue.Empty:
                return
            if future.set_running_or_notify_cancel():
                try:
                    future.set_result(fn())
                except BaseException as exc:
                    future.set_exception(exc)


def io_guarded[T](
    default_factory: Callable[[], object],
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Return the wrapped read's result, or ``default_factory()`` if a background import is running.

    The instance must expose a re-entrant ``self._io_lock`` (``threading.RLock``). ``default_factory``
    is typed loosely (``Callable[[], object]``) so the wrapped function's own return type is
    preserved rather than being erased to the factory's type (e.g. ``io_guarded(list)`` on a method
    returning ``list[Foo]`` keeps ``list[Foo]``). The empty placeholder must still be a valid stand-in
    at runtime."""

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> T:
            if not self._io_lock.acquire(blocking=False):
                return cast(T, default_factory())
            try:
                return fn(self, *args, **kwargs)
            finally:
                self._io_lock.release()

        return wrapper

    return decorator
