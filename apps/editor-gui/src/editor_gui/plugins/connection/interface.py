from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from xknx.io.knxip_interface import KNXIPInterface, KNXIPInterfaceThreaded

if TYPE_CHECKING:
    from xknx import XKNX
    from xknx.io.connection import ConnectionConfig


class ObservableKNXIPInterface(KNXIPInterface):
    __slots__ = ("_raw_cemi_callback",)

    def __init__(
        self,
        xknx: XKNX,
        connection_config: ConnectionConfig | None = None,
        raw_cemi_callback: Callable[[bytes], None] | None = None,
    ) -> None:
        super().__init__(xknx, connection_config)
        self._raw_cemi_callback = raw_cemi_callback

    def cemi_received(self, raw_cemi: bytes) -> None:
        if self._raw_cemi_callback:
            self._raw_cemi_callback(raw_cemi)
        super().cemi_received(raw_cemi)


class ObservableKNXIPInterfaceThreaded(KNXIPInterfaceThreaded):
    __slots__ = ("_raw_cemi_callback",)

    def __init__(
        self,
        xknx: XKNX,
        connection_config: ConnectionConfig | None = None,
        raw_cemi_callback: Callable[[bytes], None] | None = None,
    ) -> None:
        super().__init__(xknx, connection_config)
        self._raw_cemi_callback = raw_cemi_callback

    def cemi_received(self, raw_cemi: bytes) -> None:
        if self._raw_cemi_callback:
            self._raw_cemi_callback(raw_cemi)
        super().cemi_received(raw_cemi)
