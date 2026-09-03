from editor_gui.plugins.network.records import TelegramRecord


def test_telegram_record_properties(mock_telegrams: list[TelegramRecord]) -> None:
    assert len(mock_telegrams) == 37

    group_write = mock_telegrams[0]
    assert group_write.source == "1.1.10"
    assert group_write.destination == "0/0/1"
    assert group_write.service == "GroupValueWrite"
    assert group_write.value == "1"

    group_read = mock_telegrams[1]
    assert group_read.service == "GroupValueRead"
    assert group_read.value == ""

    group_response = mock_telegrams[2]
    assert group_response.service == "GroupValueResponse"
    # Undecoded group values are shown as hex bytes (ETS convention), so 75 == 0x4B.
    assert "4b" in group_response.value.lower()

    device_desc_read = mock_telegrams[3]
    assert device_desc_read.service == "DeviceDescriptorRead"
    assert "0" in device_desc_read.value

    device_desc_response = mock_telegrams[4]
    assert device_desc_response.service == "DeviceDescriptorResponse"
    assert "07b0" in device_desc_response.value.lower()


def test_telegram_record_timestamp(mock_telegrams: list[TelegramRecord]) -> None:
    record = mock_telegrams[0]
    assert record.timestamp_str == "09:15:00"
