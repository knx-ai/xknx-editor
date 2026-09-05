from datetime import UTC, datetime

import pytest
from xknx.dpt import DPTArray, DPTBinary
from xknx.telegram import Telegram
from xknx.telegram.apci import (
    ADCRead,
    ADCResponse,
    AuthorizeRequest,
    AuthorizeResponse,
    DeviceDescriptorRead,
    DeviceDescriptorResponse,
    FunctionPropertyCommand,
    FunctionPropertyStateRead,
    FunctionPropertyStateResponse,
    GroupValueRead,
    GroupValueResponse,
    GroupValueWrite,
    IndividualAddressRead,
    IndividualAddressResponse,
    IndividualAddressSerialRead,
    IndividualAddressSerialResponse,
    IndividualAddressSerialWrite,
    IndividualAddressWrite,
    MemoryExtendedRead,
    MemoryExtendedReadResponse,
    MemoryExtendedWrite,
    MemoryExtendedWriteResponse,
    MemoryRead,
    MemoryResponse,
    MemoryWrite,
    PropertyDescriptionRead,
    PropertyDescriptionResponse,
    PropertyValueRead,
    PropertyValueResponse,
    PropertyValueWrite,
    Restart,
    UserManufacturerInfoRead,
    UserManufacturerInfoResponse,
    UserMemoryRead,
    UserMemoryResponse,
    UserMemoryWrite,
)

from editor_gui.plugins.network.records import TelegramRecord


def make_telegram_record(source: str, dest: str, payload, sec: int) -> TelegramRecord:
    t = Telegram(destination_address=dest, source_address=source, payload=payload)
    ts = datetime(2026, 5, 12, 9, 15, sec, tzinfo=UTC)
    return TelegramRecord(telegram=t, timestamp=ts)


@pytest.fixture
def mock_telegrams() -> list[TelegramRecord]:
    return [
        make_telegram_record("1.1.10", "0/0/1", GroupValueWrite(DPTBinary(1)), 0),
        make_telegram_record("1.1.15", "0/0/2", GroupValueRead(), 1),
        make_telegram_record(
            "1.1.20", "0/0/2", GroupValueResponse(DPTArray([0x4B])), 1
        ),
        make_telegram_record("0.0.0", "1.1.50", DeviceDescriptorRead(descriptor=0), 2),
        make_telegram_record(
            "1.1.50", "0.0.0", DeviceDescriptorResponse(descriptor=0, value=0x07B0), 2
        ),
        make_telegram_record("0.0.0", "0.0.0", IndividualAddressRead(), 3),
        make_telegram_record("1.1.99", "0.0.0", IndividualAddressResponse(), 3),
        make_telegram_record(
            "0.0.0", "1.1.50", IndividualAddressWrite(address="1.1.60"), 4
        ),
        make_telegram_record(
            "0.0.0",
            "0.0.0",
            IndividualAddressSerialRead(
                serial=bytes([0x00, 0xFA, 0x12, 0x34, 0x56, 0x78])
            ),
            5,
        ),
        make_telegram_record(
            "1.1.50",
            "0.0.0",
            IndividualAddressSerialResponse(
                serial=bytes([0x00, 0xFA, 0x12, 0x34, 0x56, 0x78]), address="1.1.50"
            ),
            5,
        ),
        make_telegram_record(
            "0.0.0",
            "1.1.50",
            IndividualAddressSerialWrite(
                serial=bytes([0x00, 0xFA, 0x12, 0x34, 0x56, 0x78]), address="1.1.60"
            ),
            6,
        ),
        make_telegram_record("0.0.0", "1.1.50", MemoryRead(address=0x0060, count=2), 7),
        make_telegram_record(
            "1.1.50",
            "0.0.0",
            MemoryResponse(address=0x0060, data=bytes([0x01, 0x02])),
            7,
        ),
        make_telegram_record(
            "0.0.0", "1.1.50", MemoryWrite(address=0x0060, data=bytes([0xAB, 0xCD])), 8
        ),
        make_telegram_record(
            "0.0.0", "1.1.50", MemoryExtendedRead(address=0x010000, count=4), 9
        ),
        make_telegram_record(
            "1.1.50",
            "0.0.0",
            MemoryExtendedReadResponse(
                return_code=0, address=0x010000, data=bytes([0x11, 0x22, 0x33, 0x44])
            ),
            9,
        ),
        make_telegram_record(
            "0.0.0",
            "1.1.50",
            MemoryExtendedWrite(address=0x010000, data=bytes([0xDE, 0xAD])),
            10,
        ),
        make_telegram_record(
            "1.1.50",
            "0.0.0",
            MemoryExtendedWriteResponse(
                return_code=0, address=0x010000, confirmation_data=bytes([0xDE, 0xAD])
            ),
            10,
        ),
        make_telegram_record(
            "0.0.0", "1.1.50", UserMemoryRead(address=0x100, count=1), 11
        ),
        make_telegram_record(
            "1.1.50", "0.0.0", UserMemoryResponse(address=0x100, data=bytes([0x55])), 11
        ),
        make_telegram_record(
            "0.0.0", "1.1.50", UserMemoryWrite(address=0x100, data=bytes([0xAA])), 12
        ),
        make_telegram_record(
            "0.0.0",
            "1.1.50",
            PropertyValueRead(object_index=0, property_id=78, count=1, start_index=1),
            13,
        ),
        make_telegram_record(
            "1.1.50",
            "0.0.0",
            PropertyValueResponse(
                object_index=0,
                property_id=78,
                count=1,
                start_index=1,
                data=bytes([0x00, 0x12]),
            ),
            13,
        ),
        make_telegram_record(
            "0.0.0",
            "1.1.50",
            PropertyValueWrite(
                object_index=0,
                property_id=78,
                count=1,
                start_index=1,
                data=bytes([0x00, 0x15]),
            ),
            14,
        ),
        make_telegram_record(
            "0.0.0",
            "1.1.50",
            PropertyDescriptionRead(object_index=0, property_id=78, property_index=0),
            15,
        ),
        make_telegram_record(
            "1.1.50",
            "0.0.0",
            PropertyDescriptionResponse(
                object_index=0,
                property_id=78,
                property_index=0,
                type_=0x11,
                max_count=1,
                access=0x3F,
            ),
            15,
        ),
        make_telegram_record(
            "0.0.0",
            "1.1.50",
            FunctionPropertyCommand(object_index=0, property_id=1, data=bytes([0x01])),
            16,
        ),
        make_telegram_record(
            "0.0.0",
            "1.1.50",
            FunctionPropertyStateRead(object_index=0, property_id=1, data=b""),
            17,
        ),
        make_telegram_record(
            "1.1.50",
            "0.0.0",
            FunctionPropertyStateResponse(
                object_index=0, property_id=1, return_code=0, data=bytes([0x02])
            ),
            17,
        ),
        make_telegram_record("0.0.0", "1.1.50", ADCRead(channel=1, count=1), 18),
        make_telegram_record(
            "1.1.50", "0.0.0", ADCResponse(channel=1, count=1, value=512), 18
        ),
        make_telegram_record("0.0.0", "1.1.50", AuthorizeRequest(key=0x12345678), 19),
        make_telegram_record("1.1.50", "0.0.0", AuthorizeResponse(level=0), 19),
        make_telegram_record("0.0.0", "1.1.50", UserManufacturerInfoRead(), 20),
        make_telegram_record(
            "1.1.50",
            "0.0.0",
            UserManufacturerInfoResponse(
                manufacturer_id=0x00FA, data=bytes([0x01, 0x02, 0x03])
            ),
            20,
        ),
        make_telegram_record("0.0.0", "1.1.50", Restart(), 21),
        make_telegram_record("1.1.10", "0/0/1", GroupValueWrite(DPTBinary(0)), 22),
    ]
