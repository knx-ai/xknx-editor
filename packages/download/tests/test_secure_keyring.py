"""Tests for building DeviceSecurity from a KNX keyring."""

from __future__ import annotations

from pathlib import Path

import pytest
from xknx.secure.keyring import Keyring, XMLDevice
from xknx.telegram.address import IndividualAddress

from xknxmono.download.data_secure import SecureProgrammingError
from xknxmono.download.secure_keyring import (
    device_security_from_keyring,
    load_device_security,
)

# xknx's own keyring fixture (kept out of the repo, present locally). The device
# 1.0.0 in it decrypts to this Tool Key with the password "password".
_FIXTURE = (
    Path(__file__).resolve().parents[3]
    / ".references/xknx/test/secure_tests/resources/testcase.knxkeys"
)
_FIXTURE_TOOL_KEY = bytes.fromhex("9bc4fc74043a332b80baa2c8fef72d9d")


def _keyring_with(address: str, tool_key: bytes | None) -> Keyring:
    device = XMLDevice()
    device.individual_address = IndividualAddress(address)
    device.decrypted_tool_key = tool_key
    keyring = Keyring()
    keyring.devices = [device]
    return keyring


def test_device_security_from_keyring_returns_tool_key() -> None:
    keyring = _keyring_with("1.1.5", bytes(range(16)))
    security = device_security_from_keyring(keyring, "1.1.5")
    assert security.address == IndividualAddress("1.1.5")
    assert security.tool_key == bytes(range(16))


def test_device_security_from_keyring_missing_device() -> None:
    keyring = _keyring_with("1.1.5", bytes(16))
    with pytest.raises(SecureProgrammingError, match="not found"):
        device_security_from_keyring(keyring, "1.1.6")


def test_device_security_from_keyring_without_tool_key() -> None:
    keyring = _keyring_with("1.1.5", None)
    with pytest.raises(SecureProgrammingError, match="no Tool Key"):
        device_security_from_keyring(keyring, "1.1.5")


@pytest.mark.skipif(not _FIXTURE.exists(), reason="keyring fixture not available")
def test_load_device_security_decrypts_real_keyring() -> None:
    security = load_device_security(_FIXTURE, "password", "1.0.0")
    assert security.tool_key == _FIXTURE_TOOL_KEY
