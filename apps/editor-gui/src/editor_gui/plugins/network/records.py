from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast

from xknx.telegram import Telegram as XknxTelegram

from editor_gui.dpt import transcoder_for
from editor_gui.net import TelegramSource


def _format_raw_dpt(payload_value: Any) -> str:
    """Human-readable raw KNX payload: DPTArray -> hex bytes, DPTBinary -> its bit value.

    Avoids Python's tuple repr ("(0, 0, 0, 246)") for undecoded group values. The narrowed value is
    rebound to an ``Any`` local so iterating the dynamic xknx payload stays typed as ``Any``."""
    if payload_value is None:
        return ""
    raw: Any = getattr(payload_value, "value", payload_value)
    if isinstance(raw, (tuple, list, bytes, bytearray)):
        return " ".join(f"{int(b) & 0xFF:02X}" for b in cast("tuple[Any, ...]", raw))
    return str(raw)


def _format_value(value: Any, unit: Any) -> str:
    """Compact readable form of a decoded value: dict/namedtuple as ``k=v`` pairs, plus the unit."""
    if isinstance(value, dict):
        text = ", ".join(f"{k}={v}" for k, v in cast("dict[Any, Any]", value).items())
    elif isinstance(value, tuple) and hasattr(cast(Any, value), "_fields"):
        nt = cast(Any, value)
        text = ", ".join(f"{f}={getattr(nt, f)}" for f in nt._fields)
    elif isinstance(value, (bytes, bytearray)):
        text = " ".join(f"{b & 0xFF:02X}" for b in cast("tuple[Any, ...]", value))
    elif isinstance(value, float):
        text = f"{value:g}"
    else:
        text = str(cast(object, value))
    return f"{text} {unit}" if unit else text


def _format_decoded_value(decoded: Any) -> str:
    """Format the telegram's own DPT-decoded value (used when the frame carried its transcoder)."""
    unit = getattr(getattr(decoded, "transcoder", None), "unit", None)
    return _format_value(decoded.value, unit)


@dataclass
class CemiRecord:
    """Captured CEMI frame, including ones not decodable as telegrams."""

    raw: bytes
    timestamp: datetime
    source_type: TelegramSource
    msg_code: str
    src_addr: str
    dst_addr: str
    flags: int | None
    hops: int | None

    @property
    def timestamp_str(self) -> str:
        return self.timestamp.strftime("%H:%M:%S")

    @property
    def raw_hex(self) -> str:
        return self.raw.hex(" ")


@dataclass
class TelegramRecord:
    telegram: XknxTelegram
    timestamp: datetime
    source_type: TelegramSource = TelegramSource.CONNECTION

    @property
    def source(self) -> str:
        return str(self.telegram.source_address)

    @property
    def destination(self) -> str:
        return str(self.telegram.destination_address)

    @property
    def destination_raw(self) -> int:
        """Raw 16-bit destination address (style-independent key for project GA lookups)."""
        return int(self.telegram.destination_address.raw)

    @property
    def service(self) -> str:
        if self.telegram.payload is None:
            return ""
        return type(self.telegram.payload).__name__

    @property
    def tpci(self) -> str:
        tpci = self.telegram.tpci
        if not tpci:
            return ""
        return type(tpci).__name__

    @property
    def dpt(self) -> str:
        if self.telegram.decoded_data is not None:
            return self.telegram.decoded_data.transcoder.__name__
        return ""

    @property
    def value(self) -> str:
        if self.telegram.decoded_data is not None:
            return _format_decoded_value(self.telegram.decoded_data)
        payload = self.telegram.payload
        if payload is None:
            return ""
        return self._format_payload_value(payload)

    def value_with_dpt(self, dpt: str | None) -> str:
        """Value decoded with the project group address' DPT when the frame itself carried none.

        Falls back to :attr:`value` (raw hex) when there is no DPT or decoding fails."""
        if self.telegram.decoded_data is not None or not dpt:
            return self.value
        name = type(self.telegram.payload).__name__
        if name not in ("GroupValueWrite", "GroupValueResponse"):
            return self.value
        transcoder = transcoder_for(dpt)
        raw = getattr(self.telegram.payload, "value", None)
        if transcoder is None or raw is None:
            return self.value
        try:
            return _format_value(
                transcoder.from_knx(raw), getattr(transcoder, "unit", None)
            )
        except Exception:
            return self.value

    def _format_payload_value(self, payload: Any) -> str:
        name = type(payload).__name__

        if name == "DeviceDescriptorRead":
            return f"Desc{payload.descriptor}"
        if name == "DeviceDescriptorResponse":
            return f"Desc{payload.descriptor}: {payload.value:#06x}"
        if name == "IndividualAddressWrite":
            return str(payload.address)
        if name == "IndividualAddressSerialRead":
            return payload.serial.hex()
        if name == "IndividualAddressSerialResponse":
            return f"{payload.serial.hex()} -> {payload.address}"
        if name == "IndividualAddressSerialWrite":
            return f"{payload.serial.hex()} -> {payload.address}"
        if name == "MemoryRead":
            return f"@{payload.address:#06x} x{payload.count}"
        if name == "MemoryResponse":
            return f"@{payload.address:#06x}: {payload.data.hex()}"
        if name == "MemoryWrite":
            return f"@{payload.address:#06x}: {payload.data.hex()}"
        if name == "MemoryExtendedRead":
            return f"@{payload.address:#08x} x{payload.count}"
        if name == "MemoryExtendedReadResponse":
            return f"@{payload.address:#08x}: {payload.data.hex()} (rc={payload.return_code})"
        if name == "MemoryExtendedWrite":
            return f"@{payload.address:#08x}: {payload.data.hex()}"
        if name == "MemoryExtendedWriteResponse":
            return f"@{payload.address:#08x} (rc={payload.return_code})"
        if name == "UserMemoryRead":
            return f"@{payload.address:#06x} x{payload.count}"
        if name == "UserMemoryResponse":
            return f"@{payload.address:#06x}: {payload.data.hex()}"
        if name == "UserMemoryWrite":
            return f"@{payload.address:#06x}: {payload.data.hex()}"
        if name == "PropertyValueRead":
            return f"Obj{payload.object_index}/P{payload.property_id}[{payload.start_index}]"
        if name == "PropertyValueResponse":
            return f"Obj{payload.object_index}/P{payload.property_id}: {payload.data.hex()}"
        if name == "PropertyValueWrite":
            return f"Obj{payload.object_index}/P{payload.property_id}: {payload.data.hex()}"
        if name == "PropertyDescriptionRead":
            return f"Obj{payload.object_index}/P{payload.property_id}"
        if name == "PropertyDescriptionResponse":
            return f"Obj{payload.object_index}/P{payload.property_id} type={payload.type_:#x} max={payload.max_count}"
        if name == "FunctionPropertyCommand":
            return f"Obj{payload.object_index}/P{payload.property_id}: {payload.data.hex()}"
        if name == "FunctionPropertyStateRead":
            return f"Obj{payload.object_index}/P{payload.property_id}"
        if name == "FunctionPropertyStateResponse":
            return f"Obj{payload.object_index}/P{payload.property_id}: {payload.data.hex()} (rc={payload.return_code})"
        if name == "ADCRead":
            return f"Ch{payload.channel} x{payload.count}"
        if name == "ADCResponse":
            return f"Ch{payload.channel}: {payload.value}"
        if name == "AuthorizeRequest":
            return f"key={payload.key:#010x}"
        if name == "AuthorizeResponse":
            return f"level={payload.level}"
        if name == "UserManufacturerInfoRead":
            return ""
        if name == "UserManufacturerInfoResponse":
            return f"MfId={payload.manufacturer_id:#06x} {payload.data.hex()}"
        if name in ("IndividualAddressRead", "IndividualAddressResponse", "Restart"):
            return ""

        if name in ("GroupValueWrite", "GroupValueResponse", "GroupValueRead"):
            # No project DPT to decode with: show the raw payload as hex bytes (arrays) or the
            # bit value (DPTBinary), never a bare Python tuple like "(0, 0, 0, 246)".
            return _format_raw_dpt(getattr(payload, "value", None))

        if hasattr(payload, "value"):
            payload_value = payload.value
            if payload_value is not None and hasattr(payload_value, "value"):
                return _format_raw_dpt(payload_value)
            return str(payload_value) if payload_value is not None else ""
        return ""

    @property
    def timestamp_str(self) -> str:
        return self.timestamp.strftime("%H:%M:%S")
