"""Tests for the no-connection guard shared by all connection-requiring features."""

import time

import pytest

from editor_gui.plugins.connection.service import ConnectionService


class _FakeLogger:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def error(self, event: str, **kwargs: object) -> None:
        self.errors.append(event)

    def debug(self, event: str, **kwargs: object) -> None:
        pass

    def info(self, event: str, **kwargs: object) -> None:
        pass

    def warning(self, event: str, **kwargs: object) -> None:
        pass


@pytest.fixture
def service() -> ConnectionService:
    svc = ConnectionService()
    svc.set_logger(_FakeLogger())  # type: ignore[arg-type]
    return svc


class TestNotConnectedGuard:
    def test_refused_when_disconnected(self, service: ConnectionService) -> None:
        assert service.not_connected("program_device") is True
        assert service.not_connected_notice() is True
        assert (
            service.not_connected_notice(max_age=0.0) is False
        )  # not already aged out

    def test_allowed_when_connected(self, service: ConnectionService) -> None:
        service.set_connection(object(), None)  # any non-None xknx counts as connected
        assert service.not_connected("program_device") is False
        assert service.not_connected_notice() is False

    def test_notice_requires_a_live_rejection(self, service: ConnectionService) -> None:
        service.set_connection(object(), None)
        service.not_connected("program_device")  # logged but no notice: connected
        assert service.not_connected_notice() is False
        service.set_connection(None, None)  # dropped the link afterwards
        assert service.not_connected_notice() is False  # ...but nothing was refused

    def test_notice_covers_send_cemi(self, service: ConnectionService) -> None:
        assert service.send_cemi(b"\x01\x23") is None
        assert service.not_connected_notice() is True

    def test_notice_covers_eval_and_program(self, service: ConnectionService) -> None:
        assert service.evaluate_device(device=None) is None  # type: ignore[arg-type]
        assert service.program_device(device=None) is None  # type: ignore[arg-type]
        assert service.not_connected_notice() is True

    def test_notice_clears_after_max_age(
        self, service: ConnectionService, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        service.not_connected("send_cemi")
        now = time.monotonic()
        monkeypatch.setattr(time, "monotonic", lambda: now + 6.1)
        assert service.not_connected_notice(max_age=6.0) is False
