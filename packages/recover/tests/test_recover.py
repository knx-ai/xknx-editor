"""Tests for recover orchestration (transport retry)."""

from __future__ import annotations

import pytest
from xknx.exceptions import ManagementConnectionError
from xknx.telegram import IndividualAddress

from xknxeditor.recover.recover import recover_device_at


class _FlakyManagement:
    """A management stub whose connect always fails with a transport error."""

    def __init__(self) -> None:
        self.connect_calls = 0

    async def connect(self, address: IndividualAddress) -> object:
        self.connect_calls += 1
        raise ManagementConnectionError("tunnel dropped")

    async def disconnect(self, address: IndividualAddress) -> None:
        pass


class _FlakyXknx:
    def __init__(self) -> None:
        self.management = _FlakyManagement()


async def test_recover_device_at_retries_then_raises() -> None:
    xknx = _FlakyXknx()
    with pytest.raises(ManagementConnectionError):
        await recover_device_at(
            xknx,  # type: ignore[arg-type]
            "1.1.9",
            object(),  # type: ignore[arg-type]  # never reached: connect fails first
            attempts=3,
            retry_delay=0.0,
        )
    # Reconnected on every attempt before giving up.
    assert xknx.management.connect_calls == 3
