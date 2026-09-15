"""Tests for the dev-only per-frame DB read watchdog (:class:`_FrameDbProfiler`)."""

from xknxeditor.proj.db import _FrameDbProfiler


def test_flags_uncached_per_frame_reads() -> None:
    """Queries firing every frame while the revision is unchanged must warn once past the streak."""
    p = _FrameDbProfiler()
    # The first end_frame binds the render thread; note() only counts on that thread afterwards.
    assert p.end_frame(revision=5) is None
    msg = None
    for _ in range(5):
        p.note("SELECT * FROM spaces\nWHERE project_id = ?")
        msg = p.end_frame(revision=5)  # revision never changes
        if msg is not None:
            break
    assert msg is not None
    assert "spaces" in msg


def test_silent_when_revision_changes_each_frame() -> None:
    """A revision bump every frame is a legitimate edit stream, not an uncached read; never warns."""
    p = _FrameDbProfiler()
    p.end_frame(revision=1)
    for rev in range(2, 10):
        p.note("SELECT 1")
        assert p.end_frame(revision=rev) is None


def test_silent_without_queries() -> None:
    """No queries in a frame means an idle panel; never warns even across many unchanged frames."""
    p = _FrameDbProfiler()
    p.end_frame(revision=1)
    for _ in range(10):
        assert p.end_frame(revision=1) is None


def test_ignores_queries_off_the_render_thread() -> None:
    """A background thread (import/IO) must not be counted: only render-thread reads stall the UI."""
    import threading

    p = _FrameDbProfiler()
    p.end_frame(revision=1)  # binds the current (test) thread as the render thread

    def hammer() -> None:
        for _ in range(100):
            p.note("SELECT * FROM devices")

    t = threading.Thread(target=hammer)
    t.start()
    t.join()
    # None of the background queries were counted, so an unchanged frame stays silent.
    assert p.end_frame(revision=1) is None
