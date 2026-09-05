"""End-to-end keyring crypto tests against real KNX keyring (.knxkeys) files.

Fixtures and expected plaintext values are taken from the xknx project's
(MIT-licensed) secure test suite, vendored under ``tests/resources/``, which asserts
them against real keyring files.
"""

from __future__ import annotations

import base64
from pathlib import Path

import pytest

from xknxeditor.datasecure import (
    DecryptedKeyring,
    KeyringSignatureError,
    decrypt_keyring,
    encrypt_key,
    encrypt_password,
    load_and_decrypt,
    load_keyring,
    reencrypt_keyring,
    serialize_keyring,
    sign_keyring,
    verify_signature,
    verify_signature_bytes,
)
from xknxeditor.datasecure.crypto import (
    DEFAULT_PASSWORD_PAYLOAD_LENGTH,
    compute_signature,
    derive_iv,
    encrypt_aes128cbc,
    hash_keyring_password,
)

RESOURCES = Path(__file__).parent / "resources"

KEYRING = RESOURCES / "keyring.knxkeys"
TESTCASE = RESOURCES / "testcase.knxkeys"
SPECIAL_CHARS = RESOURCES / "special_chars_secure_tunnel.knxkeys"
DATA_SECURE_IP = RESOURCES / "DataSecure_only_one_interface.knxkeys"


def _iface_password(dec: DecryptedKeyring, ia: str) -> str | None:
    return next(i.password for i in dec.interfaces if i.individual_address == ia)


def test_verify_signature_bytes_valid() -> None:
    assert verify_signature_bytes(KEYRING.read_bytes(), "pwd")
    assert verify_signature_bytes(TESTCASE.read_bytes(), "password")
    assert verify_signature_bytes(SPECIAL_CHARS.read_bytes(), "test")
    assert verify_signature_bytes(DATA_SECURE_IP.read_bytes(), "test")


def test_verify_signature_bytes_wrong_password() -> None:
    assert not verify_signature_bytes(TESTCASE.read_bytes(), "wrong")


def test_decrypt_backbone_and_interfaces() -> None:
    dec = load_and_decrypt(KEYRING, "pwd")
    assert dec.backbone_key == bytes.fromhex("96f034fccf510760cbd63da0f70d4a9d")
    assert _iface_password(dec, "1.1.4") == "user4"
    assert _iface_password(dec, "1.1.6") == "@zvI1G&_"
    assert _iface_password(dec, "1.1.7") == "ZvDY-:g#"
    assert _iface_password(dec, "1.1.2") == "user2"


def test_decrypt_devices() -> None:
    dec = load_and_decrypt(TESTCASE, "password")
    assert dec.backbone_key == bytes.fromhex("cf89fd0f18f4889783c7ef44ee1f5e14")
    assert dec.devices[0].management_password == "commissioning"
    assert dec.devices[0].authentication == "authenticationcode"


def test_load_and_decrypt_wrong_password_raises() -> None:
    with pytest.raises(KeyringSignatureError):
        load_and_decrypt(TESTCASE, "wrong_password")


def test_one_block_key_encryption_matches_ets() -> None:
    """Encrypting a decrypted key with the same key+IV must reproduce the exact
    ciphertext in the real keyring (deterministic, no random salt)."""
    raw = TESTCASE.read_bytes()
    keyring = load_keyring(raw)
    key = hash_keyring_password(b"password")
    iv = derive_iv(str(keyring.created))

    assert keyring.backbone is not None
    dec = decrypt_keyring(keyring, "password")
    assert dec.backbone_key is not None
    assert encrypt_key(dec.backbone_key, key, iv) == keyring.backbone.key

    if keyring.group_addresses is not None:
        for group in keyring.group_addresses.group:
            plain = dec.group_keys[group.address]
            assert encrypt_key(plain, key, iv) == group.key


def test_password_wrap_roundtrip() -> None:
    key = hash_keyring_password(b"password")
    iv = derive_iv("2022-03-27T18:47:05")
    for secret in ("user1", "@zvI1G&_", "commissioning"):
        ciphertext = encrypt_password(secret, key, iv)
        # 24 payload + 8 salt = 32 bytes -> 44-char base64
        assert len(ciphertext) == 44
        from xknxeditor.datasecure.crypto import decrypt_aes128cbc, extract_password

        assert (
            extract_password(decrypt_aes128cbc(base64.b64decode(ciphertext), key, iv))
            == secret
        )


def test_sign_roundtrip_self_consistent() -> None:
    """A keyring we (re-)sign must verify against our own re-serialization."""
    keyring = load_keyring(TESTCASE.read_bytes())
    sign_keyring(keyring, "password")
    assert verify_signature(keyring, "password")
    assert not verify_signature(keyring, "wrong")


def test_iv_uses_raw_created_not_normalized() -> None:
    """The keyring format derives the IV from the original Created string. xsdata
    normalizes "+00:00" to "Z", which would yield a different IV; load_and_decrypt
    must use the raw attribute so a secret encrypted under the raw form decrypts."""
    created_raw = "2022-03-27T18:47:05+00:00"  # xsdata str() would render "...Z"
    key = hash_keyring_password(b"pwd")
    iv = derive_iv(created_raw)
    raw_key = bytes(range(16))
    enc_key = base64.b64encode(encrypt_aes128cbc(raw_key, key, iv)).decode("ascii")

    placeholder = "A" * 21 + "Q=="
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        f'<Keyring Project="P" CreatedBy="t" Created="{created_raw}" '
        f'Signature="{placeholder}" xmlns="http://knx.org/xml/keyring/1">'
        f'<Backbone MulticastAddress="224.0.23.12" Key="{enc_key}" /></Keyring>'
    )
    sig = base64.b64encode(compute_signature(xml.encode("utf-8"), "pwd")).decode(
        "ascii"
    )
    signed = xml.replace(placeholder, sig).encode("utf-8")

    dec = load_and_decrypt(signed, "pwd")
    assert dec.backbone_key == raw_key


def test_signature_long_attribute_value() -> None:
    """Attribute values >= 128 bytes need a multi-byte (LEB128) length prefix to
    match the keyring signing format. A single-byte length would corrupt them."""
    from xsdata.models.datatype import XmlDateTime

    from xknxeditor.datasecure.files.knx_keyring import (
        Interface,
        InterfaceType,
        Keyring,
    )

    # ~40 addresses -> Senders value well over 255 bytes.
    senders = [f"1.1.{n}" for n in range(1, 41)]
    keyring = Keyring(
        project="Long",
        created=XmlDateTime.from_string("2024-01-01T00:00:00"),
        created_by="test",
        signature="A" * 21 + "Q==",
        interface=[
            Interface(
                type_value=InterfaceType.TUNNELING,
                individual_address="1.0.1",
                group=[Interface.Group(address=1, senders=senders)],
            )
        ],
    )
    sign_keyring(keyring, "pwd")
    assert verify_signature(keyring, "pwd")
    written = serialize_keyring(keyring)
    assert verify_signature_bytes(written, "pwd")


def test_full_write_roundtrip() -> None:
    """Re-encrypt every secret with fresh randomness, re-sign, then load back and
    confirm the plaintext survives a full write/read cycle."""
    keyring = load_keyring(TESTCASE.read_bytes())
    original = decrypt_keyring(keyring, "password")

    key = hash_keyring_password(b"password")
    iv = derive_iv(str(keyring.created))

    # Re-encrypt interface passwords (uses fresh random salt each time).
    for iface_model, iface_plain in zip(
        keyring.interface, original.interfaces, strict=True
    ):
        if iface_plain.password is not None:
            iface_model.password = encrypt_password(
                iface_plain.password,
                key,
                iv,
                payload_length=DEFAULT_PASSWORD_PAYLOAD_LENGTH,
            )

    sign_keyring(keyring, "password")

    written = serialize_keyring(keyring)
    assert verify_signature_bytes(written, "password")
    reloaded = load_and_decrypt(written, "password")
    assert [i.password for i in reloaded.interfaces] == [
        i.password for i in original.interfaces
    ]


def _plaintext(dec: DecryptedKeyring) -> tuple[object, ...]:
    """Order-independent snapshot of all plaintext key material for comparison."""
    return (
        dec.backbone_key,
        sorted(
            (i.individual_address, i.password, i.authentication) for i in dec.interfaces
        ),
        sorted(
            (
                d.individual_address,
                d.tool_key,
                d.fdsk,
                d.management_password,
                d.authentication,
                d.password,
            )
            for d in dec.devices
        ),
        sorted(dec.group_keys.items()),
    )


def test_reencrypt_same_password_preserves_plaintext() -> None:
    original = load_and_decrypt(TESTCASE, "password")
    model = load_keyring(TESTCASE.read_bytes())
    converted = reencrypt_keyring(model, "password", "password")
    written = serialize_keyring(converted)
    assert verify_signature_bytes(written, "password")
    assert _plaintext(load_and_decrypt(written, "password")) == _plaintext(original)


def test_reencrypt_changes_password() -> None:
    original = load_and_decrypt(TESTCASE, "password")
    model = load_keyring(TESTCASE.read_bytes())
    converted = reencrypt_keyring(model, "password", "new-secret")
    written = serialize_keyring(converted)
    # old password no longer verifies; new one does, and plaintext is preserved.
    assert not verify_signature_bytes(written, "password")
    assert verify_signature_bytes(written, "new-secret")
    assert _plaintext(load_and_decrypt(written, "new-secret")) == _plaintext(original)


def test_reencrypt_new_created_changes_iv_but_preserves_plaintext() -> None:
    original = load_and_decrypt(TESTCASE, "password")
    model = load_keyring(TESTCASE.read_bytes())
    converted = reencrypt_keyring(
        model, "password", "password", new_created="2030-01-02T03:04:05"
    )
    written = serialize_keyring(converted)
    assert b'Created="2030-01-02T03:04:05"' in written
    assert verify_signature_bytes(written, "password")
    assert _plaintext(load_and_decrypt(written, "password")) == _plaintext(original)


def test_reencrypt_does_not_mutate_source_model() -> None:
    model = load_keyring(TESTCASE.read_bytes())
    before = serialize_keyring(model)
    reencrypt_keyring(model, "password", "other")
    assert serialize_keyring(model) == before
