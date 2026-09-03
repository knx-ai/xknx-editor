from collections.abc import Callable
from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

from xknx.cemi import CEMIFrame, CEMILData, CEMIMessageCode
from xknx.telegram import Telegram

from editor_gui.net import TelegramSource
from editor_gui.plugins.network.records import CemiRecord, TelegramRecord

if TYPE_CHECKING:
    from editor_gui.plugins.base import Logger


class CaptureState(Enum):
    STOPPED = "stopped"
    CAPTURING = "capturing"


class NetworkService:
    def __init__(self) -> None:
        self._telegrams: list[TelegramRecord] = []
        self._cemi_records: list[CemiRecord] = []
        self._state = CaptureState.STOPPED
        self._listeners: dict[str, list[Callable[..., Any]]] = {}
        self._log: Logger

    def set_logger(self, log: "Logger") -> None:
        self._log = log

    @property
    def state(self) -> CaptureState:
        return self._state

    @property
    def telegrams(self) -> list[TelegramRecord]:
        return self._telegrams

    @property
    def cemi_records(self) -> list[CemiRecord]:
        return self._cemi_records

    def start(self) -> None:
        if self._state == CaptureState.CAPTURING:
            return
        self._telegrams.clear()
        self._cemi_records.clear()
        self._state = CaptureState.CAPTURING
        self._emit("capture_state_changed", self._state)

    def stop(self) -> None:
        if self._state == CaptureState.STOPPED:
            return
        self._state = CaptureState.STOPPED
        self._emit("capture_state_changed", self._state)

    def add_raw(
        self, cemi_bytes: bytes, source: TelegramSource
    ) -> TelegramRecord | None:
        return self.add_raw_with_timestamp(cemi_bytes, source, datetime.now(UTC))

    def add_raw_with_timestamp(
        self, cemi_bytes: bytes, source: TelegramSource, timestamp: datetime
    ) -> TelegramRecord | None:
        if self._state != CaptureState.CAPTURING:
            return None
        cemi_rec = self._parse_cemi_record(cemi_bytes, source, timestamp)
        if cemi_rec is not None:
            self._cemi_records.append(cemi_rec)
            self._emit("cemi_added", cemi_rec)
        telegram = self._parse_telegram(cemi_bytes, source, timestamp)
        if telegram is not None:
            self._telegrams.append(telegram)
            self._emit("telegram_added", telegram)
        return telegram

    def clear(self) -> None:
        self._telegrams.clear()
        self._cemi_records.clear()
        self._emit("cleared")

    def subscribe(self, event: str, handler: Callable[..., Any]) -> Callable[[], None]:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(handler)
        return lambda: self._listeners[event].remove(handler)

    def _emit(self, event: str, *args: Any) -> None:
        for handler in self._listeners.get(event, []):
            handler(*args)

    def _parse_cemi_record(
        self, cemi_bytes: bytes, source: TelegramSource, timestamp: datetime
    ) -> CemiRecord | None:
        if not cemi_bytes:
            return None
        try:
            code_byte = cemi_bytes[0]
            try:
                code = CEMIMessageCode(code_byte)
                msg_code = code.name
            except ValueError:
                msg_code = f"0x{code_byte:02x}"

            src_addr = ""
            dst_addr = ""
            flags: int | None = None
            hops: int | None = None

            frame = CEMIFrame.from_knx(cemi_bytes)
            if isinstance(frame.data, CEMILData):
                data = frame.data
                src_addr = str(data.src_addr)
                dst_addr = str(data.dst_addr)
                flags = data.flags
                hops = (data.flags & 0x0070) >> 4

            reencoded = frame.to_knx()
            if reencoded != cemi_bytes:
                self._log.error(
                    "cemi round-trip mismatch",
                    original=cemi_bytes.hex(" "),
                    reencoded=reencoded.hex(" "),
                )

            return CemiRecord(
                raw=cemi_bytes,
                timestamp=timestamp,
                source_type=source,
                msg_code=msg_code,
                src_addr=src_addr,
                dst_addr=dst_addr,
                flags=flags,
                hops=hops,
            )
        except Exception as e:
            self._log.error("failed to parse CEMI record", error=str(e))
            # Still store a minimal record with the raw bytes
            code_byte = cemi_bytes[0] if cemi_bytes else 0
            return CemiRecord(
                raw=cemi_bytes,
                timestamp=timestamp,
                source_type=source,
                msg_code=f"0x{code_byte:02x}",
                src_addr="",
                dst_addr="",
                flags=None,
                hops=None,
            )

    def _parse_telegram(
        self, cemi_bytes: bytes, source: TelegramSource, timestamp: datetime
    ) -> TelegramRecord | None:
        try:
            frame = CEMIFrame.from_knx(cemi_bytes)
            data = frame.data
            if not isinstance(data, CEMILData):
                return None
            telegram = Telegram(
                source_address=data.src_addr,
                destination_address=data.dst_addr,
                payload=data.payload,
                tpci=data.tpci,
            )
            return TelegramRecord(
                telegram=telegram, timestamp=timestamp, source_type=source
            )
        except Exception as e:
            self._log.error("failed to parse CEMI frame", error=str(e))
            return None
