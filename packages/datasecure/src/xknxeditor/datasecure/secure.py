"""Decrypt, verify, encrypt and sign KNX keyrings on the xsdata model.

High-level layer over :mod:`xknxeditor.datasecure.crypto` that works with the parsed
:class:`~xknxeditor.datasecure.files.knx_keyring.Keyring` model. Reading recovers the
plaintext key material into :class:`DecryptedKeyring`; writing re-encrypts secrets
and produces a valid keyring ``Signature``.
"""

from __future__ import annotations

import base64
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from xknxeditor.datasecure.crypto import (
    DEFAULT_PASSWORD_PAYLOAD_LENGTH,
    DEVICE_PASSWORD_PAYLOAD_LENGTH,
    compute_signature,
    decrypt_aes128cbc,
    derive_iv,
    encrypt_aes128cbc,
    extract_password,
    hash_keyring_password,
    wrap_password,
)
from xknxeditor.datasecure.files.knx_keyring import InterfaceType, Keyring
from xknxeditor.datasecure.schema import load_keyring, serialize_keyring

# Valid placeholder signature (matches the model pattern) used while serializing
# before the real signature is computed. It is excluded from the signed stream.
_PLACEHOLDER_SIGNATURE = "A" * 21 + "Q=="


class KeyringSignatureError(Exception):
    """Raised when a keyring signature does not match the given password."""


@dataclass(slots=True)
class DecryptedInterface:
    """Plaintext secrets of a keyring ``Interface``."""

    type: InterfaceType
    individual_address: str | None
    host: str | None
    user_id: int | None
    password: str | None
    authentication: str | None


@dataclass(slots=True)
class DecryptedDevice:
    """Plaintext secrets of a keyring ``Device``."""

    individual_address: str
    tool_key: bytes | None
    management_password: str | None
    authentication: str | None
    fdsk: bytes | None
    password: str | None
    sequence_number: int | None


@dataclass(slots=True)
class DecryptedKeyring:
    """Recovered plaintext key material of a keyring."""

    backbone_key: bytes | None
    interfaces: list[DecryptedInterface]
    devices: list[DecryptedDevice]
    group_keys: dict[int, bytes]


def verify_signature_bytes(xml_bytes: bytes, password: str) -> bool:
    """Verify the ``Signature`` of a raw keyring XML byte stream.

    Authoritative for imported files: canonicalizes the original bytes exactly as
    the keyring signing format requires, without a serialization round-trip.
    """
    root = ET.fromstring(xml_bytes)
    signature = base64.b64decode(root.attrib.get("Signature", ""))
    return compute_signature(xml_bytes, password) == signature


def verify_signature(keyring: Keyring, password: str) -> bool:
    """Verify a keyring model's ``Signature`` by re-serializing it.

    Reliable only for keyrings produced by this library (self-consistent). It is
    NOT reliable for imported files: xsdata may emit attributes real keyrings omit
    (e.g. a default ``TxRfReady="false"``), which alters the signed canonical
    stream. Use :func:`verify_signature_bytes` for imported bytes.
    """
    expected = base64.b64decode(keyring.signature)
    xml_bytes = serialize_keyring(keyring)
    return compute_signature(xml_bytes, password) == expected


def load_and_decrypt(
    source: str | Path | bytes, password: str, *, verify: bool = True
) -> DecryptedKeyring:
    """Load a keyring from bytes/path, verify its signature, and decrypt it.

    This is the safe import entry point: verification runs over the original
    bytes (authoritative). Raises :class:`KeyringSignatureError` on a bad
    password or altered content when ``verify`` is true.
    """
    xml_bytes = Path(source).read_bytes() if isinstance(source, str | Path) else source
    if verify and not verify_signature_bytes(xml_bytes, password):
        msg = (
            "keyring signature verification failed (wrong password or altered content)"
        )
        raise KeyringSignatureError(msg)
    # The keyring format derives the IV from the *original* Created attribute
    # string. xsdata may normalize its lexical form on parse (e.g. "+00:00" ->
    # "Z"), so read the raw value from the source bytes rather than the model.
    created = ET.fromstring(xml_bytes).attrib.get("Created")
    return decrypt_keyring(load_keyring(xml_bytes), password, created=created)


def decrypt_keyring(
    keyring: Keyring, password: str, *, created: str | None = None
) -> DecryptedKeyring:
    """Recover all plaintext key material from a parsed ``keyring`` model.

    Performs no signature check; use :func:`load_and_decrypt` to verify an import
    against its original bytes first.

    ``created`` overrides the string used for IV derivation. Pass the raw
    ``Created`` attribute from the source XML when available; otherwise the
    model's (possibly re-normalized) value is used, which can differ from real
    keyrings for non-canonical datetime lexical forms.
    """
    key = hash_keyring_password(password.encode("utf-8"))
    iv = derive_iv(created if created is not None else str(keyring.created))

    backbone_key: bytes | None = None
    if keyring.backbone is not None and keyring.backbone.key:
        backbone_key = decrypt_aes128cbc(
            base64.b64decode(keyring.backbone.key), key, iv
        )

    interfaces: list[DecryptedInterface] = []
    for iface in keyring.interface:
        interfaces.append(
            DecryptedInterface(
                type=iface.type_value,
                individual_address=iface.individual_address,
                host=iface.host,
                user_id=iface.user_id,
                password=(
                    extract_password(
                        decrypt_aes128cbc(base64.b64decode(iface.password), key, iv)
                    )
                    if iface.password is not None
                    else None
                ),
                authentication=(
                    extract_password(
                        decrypt_aes128cbc(
                            base64.b64decode(iface.authentication), key, iv
                        )
                    )
                    if iface.authentication is not None
                    else None
                ),
            )
        )

    devices: list[DecryptedDevice] = []
    if keyring.devices is not None:
        for device in keyring.devices.device:
            devices.append(
                DecryptedDevice(
                    individual_address=device.individual_address,
                    tool_key=(
                        decrypt_aes128cbc(base64.b64decode(device.tool_key), key, iv)
                        if device.tool_key is not None
                        else None
                    ),
                    management_password=(
                        extract_password(
                            decrypt_aes128cbc(
                                base64.b64decode(device.management_password), key, iv
                            )
                        )
                        if device.management_password is not None
                        else None
                    ),
                    authentication=(
                        extract_password(
                            decrypt_aes128cbc(
                                base64.b64decode(device.authentication), key, iv
                            )
                        )
                        if device.authentication is not None
                        else None
                    ),
                    fdsk=(
                        decrypt_aes128cbc(base64.b64decode(device.fdsk), key, iv)
                        if device.fdsk is not None
                        else None
                    ),
                    password=(
                        extract_password(decrypt_aes128cbc(device.password, key, iv))
                        if device.password is not None
                        else None
                    ),
                    sequence_number=device.sequence_number,
                )
            )

    group_keys: dict[int, bytes] = {}
    if keyring.group_addresses is not None:
        for group in keyring.group_addresses.group:
            group_keys[group.address] = decrypt_aes128cbc(
                base64.b64decode(group.key), key, iv
            )

    return DecryptedKeyring(
        backbone_key=backbone_key,
        interfaces=interfaces,
        devices=devices,
        group_keys=group_keys,
    )


def encrypt_key(raw_key: bytes, key: bytes, iv: bytes) -> str:
    """Encrypt a raw 16-byte key to its base64 keyring representation."""
    return base64.b64encode(encrypt_aes128cbc(raw_key, key, iv)).decode("ascii")


def encrypt_password(
    plaintext: str,
    key: bytes,
    iv: bytes,
    *,
    payload_length: int = DEFAULT_PASSWORD_PAYLOAD_LENGTH,
) -> str:
    """Wrap and encrypt a password to its base64 keyring representation."""
    return base64.b64encode(
        encrypt_aes128cbc(wrap_password(plaintext, payload_length), key, iv)
    ).decode("ascii")


def sign_keyring(keyring: Keyring, password: str) -> Keyring:
    """Set ``keyring.signature`` to a valid keyring signature for ``password``.

    Mutates and returns the same model. Call after all secret attributes have
    been (re-)encrypted, so the signature covers the final content.
    """
    keyring.signature = _PLACEHOLDER_SIGNATURE
    xml_bytes = serialize_keyring(keyring)
    keyring.signature = base64.b64encode(compute_signature(xml_bytes, password)).decode(
        "ascii"
    )
    return keyring


def reencrypt_keyring(
    keyring: Keyring,
    old_password: str,
    new_password: str,
    *,
    created: str | None = None,
    new_created: str | None = None,
) -> Keyring:
    """Return a copy of ``keyring`` with every secret re-encrypted under
    ``new_password`` and re-signed, preserving all structure and metadata.

    Decrypts each secret with ``old_password`` (IV from ``created`` or the model's
    own ``Created``), then re-encrypts under ``new_password``. Pass ``new_created``
    to also change the ``Created`` attribute (which changes the IV and, for
    password fields, the ciphertext). The result verifies under ``new_password``.

    Use this for the "export / convert keyring" flow: hand a partner the same key
    material under a different keyring password.
    """
    import copy

    from xsdata.models.datatype import XmlDateTime

    old_key = hash_keyring_password(old_password.encode("utf-8"))
    old_iv = derive_iv(created if created is not None else str(keyring.created))

    result = copy.deepcopy(keyring)
    if new_created is not None:
        result.created = XmlDateTime.from_string(new_created)
    dst_created = new_created if new_created is not None else str(result.created)
    new_key = hash_keyring_password(new_password.encode("utf-8"))
    new_iv = derive_iv(dst_created)

    def rekey_key(b64: str) -> str:
        raw = decrypt_aes128cbc(base64.b64decode(b64), old_key, old_iv)
        return encrypt_key(raw, new_key, new_iv)

    def rekey_password(b64: str, payload_length: int) -> str:
        text = extract_password(
            decrypt_aes128cbc(base64.b64decode(b64), old_key, old_iv)
        )
        return encrypt_password(text, new_key, new_iv, payload_length=payload_length)

    if result.backbone is not None and result.backbone.key:
        result.backbone.key = rekey_key(result.backbone.key)

    for iface in result.interface:
        if iface.password is not None:
            iface.password = rekey_password(
                iface.password, DEFAULT_PASSWORD_PAYLOAD_LENGTH
            )
        if iface.authentication is not None:
            iface.authentication = rekey_password(
                iface.authentication, DEFAULT_PASSWORD_PAYLOAD_LENGTH
            )

    if result.devices is not None:
        for device in result.devices.device:
            if device.tool_key is not None:
                device.tool_key = rekey_key(device.tool_key)
            if device.fdsk is not None:
                device.fdsk = rekey_key(device.fdsk)
            if device.management_password is not None:
                device.management_password = rekey_password(
                    device.management_password, DEFAULT_PASSWORD_PAYLOAD_LENGTH
                )
            if device.authentication is not None:
                device.authentication = rekey_password(
                    device.authentication, DEFAULT_PASSWORD_PAYLOAD_LENGTH
                )
            if device.password is not None:
                # Device Password is base64Binary in the model -> raw ciphertext bytes,
                # and the keyring format wraps it to 56 payload bytes (four AES blocks).
                text = extract_password(
                    decrypt_aes128cbc(device.password, old_key, old_iv)
                )
                device.password = base64.b64decode(
                    encrypt_password(
                        text,
                        new_key,
                        new_iv,
                        payload_length=DEVICE_PASSWORD_PAYLOAD_LENGTH,
                    )
                )

    if result.group_addresses is not None:
        for group in result.group_addresses.group:
            group.key = rekey_key(group.key)

    sign_keyring(result, new_password)
    return result


__all__ = [
    "DEFAULT_PASSWORD_PAYLOAD_LENGTH",
    "DEVICE_PASSWORD_PAYLOAD_LENGTH",
    "DecryptedDevice",
    "DecryptedInterface",
    "DecryptedKeyring",
    "KeyringSignatureError",
    "decrypt_keyring",
    "encrypt_key",
    "encrypt_password",
    "load_and_decrypt",
    "reencrypt_keyring",
    "sign_keyring",
    "verify_signature",
    "verify_signature_bytes",
]
