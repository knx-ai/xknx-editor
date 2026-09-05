from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from editor_gui.plugins.logger.service import LogService


class Logger:
    def __init__(self, service: LogService, plugin: str) -> None:
        self._service = service
        self._plugin = plugin

    def debug(self, event: str, **kwargs: Any) -> None:
        self._service.debug(event, self._plugin, **kwargs)

    def info(self, event: str, **kwargs: Any) -> None:
        self._service.info(event, self._plugin, **kwargs)

    def warning(self, event: str, **kwargs: Any) -> None:
        self._service.warning(event, self._plugin, **kwargs)

    def error(self, event: str, **kwargs: Any) -> None:
        self._service.error(event, self._plugin, **kwargs)
