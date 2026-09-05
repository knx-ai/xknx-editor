"""Logic tests for the DALI commissioning tab (gating + async op-runner state machine).

The imgui rendering isn't unit-tested; this covers the parts that decide behaviour: which devices
show the tab, and that a started operation toggles busy / stashes a scan result / surfaces errors.
"""

from __future__ import annotations

import asyncio
import contextlib
from types import SimpleNamespace
from typing import Any

from editor_gui.plugins.project.ui.dali_commissioning import DaliCommissioningPanel
from editor_gui.programming_dali import is_mdt_dali_app
from xknxeditor.dali.model import DaliBusState, EcgState


def test_gating_matches_only_mdt_dali_apps() -> None:
    assert is_mdt_dali_app("M-0083_A-0154-40-0F69-O00EF")
    assert is_mdt_dali_app("M-0083_A-0153-10-297A-O00EF")
    assert not is_mdt_dali_app("M-0083_A-9999-40")  # other MDT app
    assert not is_mdt_dali_app("M-0001_A-0154")  # other manufacturer
    assert not is_mdt_dali_app(None)


def _device() -> Any:
    return SimpleNamespace(individual_address="1.1.1", name="Gateway")


def _runner(commissioner: Any, *, started: bool = True):
    """A fake ConnectionService.run_dali: executes the wrapped coroutine (like the async loop would),
    swallowing exceptions (the real future captures them), and reports whether it was accepted."""

    def run(device: Any, wrapped: Any) -> bool:
        if started:
            with contextlib.suppress(Exception):  # the real future captures the error
                asyncio.run(wrapped(commissioner))
        return started

    return run


def test_scan_stashes_result_and_clears_busy() -> None:
    bus = DaliBusState(channel=0, ecgs=[EcgState(slot=0, present=True, group_index=5)])
    commissioner = SimpleNamespace(scan=lambda: _coro(bus))
    panel = DaliCommissioningPanel(_runner(commissioner))

    panel._start(_device(), "scan", lambda c: c.scan(), store_scan=True)

    state = panel._state("1.1.1")
    assert state.busy == ""  # released
    assert state.error == ""
    assert state.scan is bus


def test_error_is_surfaced_and_busy_released() -> None:
    async def boom(_c: Any) -> object:
        raise RuntimeError("no ack")

    commissioner = SimpleNamespace()
    panel = DaliCommissioningPanel(_runner(commissioner))
    panel._start(_device(), "commission", boom)

    state = panel._state("1.1.1")
    assert state.busy == ""
    assert "no ack" in state.error


def test_not_started_when_runner_rejects() -> None:
    panel = DaliCommissioningPanel(_runner(SimpleNamespace(), started=False))
    panel._start(_device(), "scan", lambda c: c.scan(), store_scan=True)
    assert panel._state("1.1.1").busy == ""  # rolled back when the bus was busy


async def _coro(value: Any) -> Any:
    return value
