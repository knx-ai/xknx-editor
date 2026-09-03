"""Tests for cross-device group-communication validation."""

from __future__ import annotations

from xknxmono.recover import RecoveredParameters, validate_group_communication
from xknxmono.recover.recover import RecoveredDevice
from xknxmono.recover.tables_decode import DecodedLink


def _device(address: str, links: list[DecodedLink]) -> RecoveredDevice:
    return RecoveredDevice(
        address=address,
        application_id="M-0001_A-0001-00-0001",
        device_address=None,
        group_addresses=sorted({link.group_address for link in links}),
        links=links,
        group_objects={},
        parameters=RecoveredParameters(values={}, unknown=[]),
    )


def test_no_sender_and_multiple_senders_flagged() -> None:
    devices = [
        # GA 0x0B00: one sender + one receiver -> healthy, not reported.
        _device("1.1.1", [DecodedLink(0x0B00, 1, sending=True)]),
        _device("1.1.2", [DecodedLink(0x0B00, 1, sending=False)]),
        # GA 0x0B01: only receivers -> no_sender.
        _device("1.1.3", [DecodedLink(0x0B01, 2, sending=False)]),
        # GA 0x0B02: two senders -> multiple_senders.
        _device(
            "1.1.4",
            [
                DecodedLink(0x0B02, 3, sending=True),
                DecodedLink(0x0B02, 4, sending=True),
            ],
        ),
    ]
    warnings = {w.group_address: w for w in validate_group_communication(devices)}
    assert set(warnings) == {0x0B01, 0x0B02}
    assert warnings[0x0B01].kind == "no_sender"
    assert warnings[0x0B02].kind == "multiple_senders"
    assert warnings[0x0B02].senders == 2


def test_healthy_links_have_no_warnings() -> None:
    devices = [
        _device("1.1.1", [DecodedLink(0x0B00, 1, sending=True)]),
        _device("1.1.2", [DecodedLink(0x0B00, 1, sending=False)]),
    ]
    assert validate_group_communication(devices) == []
