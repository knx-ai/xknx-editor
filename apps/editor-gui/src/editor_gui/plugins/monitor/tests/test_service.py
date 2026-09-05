"""Tests for the monitor service: the live telegram log and latest-value tracking."""

from __future__ import annotations

from typing import Any

from xknx.cemi import CEMIFrame, CEMILData, CEMIMessageCode
from xknx.dpt import DPTBinary
from xknx.telegram import GroupAddress, IndividualAddress, Telegram
from xknx.telegram.apci import GroupValueRead, GroupValueWrite

from editor_gui.plugins.monitor.service import MonitorService


def _raw(dst: str, payload: Any, src: str = "1.1.1") -> bytes:
    telegram = Telegram(destination_address=GroupAddress(dst), payload=payload)
    data = CEMILData.init_from_telegram(telegram, src_addr=IndividualAddress(src))
    return CEMIFrame(code=CEMIMessageCode.L_DATA_IND, data=data).to_knx()


def _service() -> MonitorService:
    svc = MonitorService(connection=object())  # type: ignore[arg-type]  # on_raw_cemi ignores it
    return svc


def test_write_recorded_in_log_and_latest() -> None:
    svc = _service()
    svc.on_raw_cemi(_raw("1/2/3", GroupValueWrite(DPTBinary(1))), None)  # type: ignore[arg-type]
    log = svc.telegrams()
    assert len(log) == 1
    assert log[0].destination == "1/2/3"
    assert log[0].service == "Write"
    assert log[0].source == "1.1.1"
    assert svc.latest("1/2/3") is not None


def test_read_logged_but_not_a_latest_value() -> None:
    svc = _service()
    svc.on_raw_cemi(_raw("0/0/1", GroupValueRead()), None)  # type: ignore[arg-type]
    assert len(svc.telegrams()) == 1
    assert svc.telegrams()[0].service == "Read"
    assert svc.latest("0/0/1") is None  # a read carries no value


def test_clear_empties_log_and_values() -> None:
    svc = _service()
    svc.on_raw_cemi(_raw("1/2/3", GroupValueWrite(DPTBinary(1))), None)  # type: ignore[arg-type]
    svc.clear()
    assert svc.telegrams() == []
    assert svc.latest("1/2/3") is None
