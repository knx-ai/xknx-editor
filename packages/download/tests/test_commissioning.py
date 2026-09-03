"""Tests for individual address programming."""

from __future__ import annotations

from typing import cast

import pytest
from xknx import XKNX
from xknx.telegram.address import IndividualAddressableType

import xknxmono.download.commissioning as commissioning


async def test_program_via_programming_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[str, object]] = []

    async def fake_write(
        xknx: XKNX, individual_address: IndividualAddressableType
    ) -> None:
        calls.append(("prog", individual_address))

    monkeypatch.setattr(commissioning, "nm_individual_address_write", fake_write)

    await commissioning.program_individual_address(cast("XKNX", object()), "1.1.5")

    assert calls == [("prog", "1.1.5")]


async def test_program_via_serial_number(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[str, bytes, object]] = []

    async def fake_serial(
        xknx: XKNX, serial: bytes, individual_address: IndividualAddressableType
    ) -> None:
        calls.append(("serial", serial, individual_address))

    monkeypatch.setattr(
        commissioning, "nm_individual_address_serial_number_write", fake_serial
    )

    serial = bytes.fromhex("00010203 0405".replace(" ", ""))
    await commissioning.program_individual_address(
        cast("XKNX", object()), "1.1.5", serial_number=serial
    )

    assert calls == [("serial", serial, "1.1.5")]
