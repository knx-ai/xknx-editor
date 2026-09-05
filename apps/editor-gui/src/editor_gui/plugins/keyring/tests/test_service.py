"""Integration tests for the GUI keyring service: import, device-security lookup, export."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from xsdata.models.datatype import XmlDateTime

from editor_gui.plugins.base import Logger
from editor_gui.plugins.keyring.service import KeyringService
from xknxeditor.datasecure import load_and_decrypt, serialize_keyring, sign_keyring
from xknxeditor.datasecure.crypto import derive_iv, hash_keyring_password
from xknxeditor.datasecure.files.knx_keyring import (
    Backbone,
    Devices,
    Interface,
    InterfaceType,
    Keyring,
)
from xknxeditor.datasecure.secure import encrypt_key, encrypt_password

_PASSWORD = "test"
_CREATED = "2026-09-04T12:00:00"
_TOOL_KEY = bytes.fromhex("a0a1a2a3a4a5a6a7a8a9aaabacadaeaf")
_BACKBONE = bytes.fromhex("00112233445566778899aabbccddeeff")


class _StubLog:
    def info(self, event: str, **kwargs: Any) -> None: ...
    def warning(self, event: str, **kwargs: Any) -> None: ...
    def debug(self, event: str, **kwargs: Any) -> None: ...
    def error(self, event: str, **kwargs: Any) -> None: ...


def _write_keyring(path: Path) -> None:
    key = hash_keyring_password(_PASSWORD.encode("utf-8"))
    iv = derive_iv(_CREATED)
    keyring = Keyring(
        project="svc-test",
        created=XmlDateTime.from_string(_CREATED),
        created_by="test",
        signature="A" * 21 + "Q==",
        backbone=Backbone(
            multicast_address="224.0.23.12",
            latency=1000,
            key=encrypt_key(_BACKBONE, key, iv),
        ),
        interface=[
            Interface(
                type_value=InterfaceType.TUNNELING,
                host="1.0.0",
                individual_address="1.0.1",
                user_id=2,
                password=encrypt_password("tunnel_pw", key, iv),
            )
        ],
        devices=Devices(
            device=[
                Devices.Device(
                    individual_address="1.0.5",
                    serial_number="00FA00000001",
                    tool_key=encrypt_key(_TOOL_KEY, key, iv),
                )
            ]
        ),
    )
    sign_keyring(keyring, _PASSWORD)
    path.write_bytes(serialize_keyring(keyring))


def _service() -> KeyringService:
    svc = KeyringService()
    svc.set_logger(cast(Logger, _StubLog()))
    return svc


def test_load_and_device_security(tmp_path: Path) -> None:
    path = tmp_path / "kr.knxkeys"
    _write_keyring(path)
    svc = _service()
    svc.load(path, _PASSWORD)

    assert svc.is_loaded()
    assert svc.project_name == "svc-test"
    # device with a tool key -> DeviceSecurity; unknown / non-secure -> None
    sec = svc.device_security("1.0.5")
    assert sec is not None
    assert bytes(sec.tool_key) == _TOOL_KEY
    assert svc.device_security("1.0.99") is None


def test_export_converts_password(tmp_path: Path) -> None:
    src = tmp_path / "kr.knxkeys"
    _write_keyring(src)
    svc = _service()
    svc.load(src, _PASSWORD)

    out = tmp_path / "converted.knxkeys"
    svc.export(out, "new-password")

    # exported file opens under the new password with identical key material
    dec = load_and_decrypt(out, "new-password")
    assert dec.backbone_key == _BACKBONE
    assert dec.devices[0].tool_key == _TOOL_KEY
    assert dec.interfaces[0].password == "tunnel_pw"


def test_clear_resets_state(tmp_path: Path) -> None:
    path = tmp_path / "kr.knxkeys"
    _write_keyring(path)
    svc = _service()
    svc.load(path, _PASSWORD)
    svc.clear()
    assert not svc.is_loaded()
    assert svc.keyring is None
    assert svc.device_security("1.0.5") is None
