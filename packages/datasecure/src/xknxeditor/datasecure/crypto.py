"""Low-level KNX keyring cryptography.

Implements the KNX keyring (``.knxkeys``) key protection. The cryptographic
primitives follow the KNX Standard v3.0.0 (Vol 3 / 3.8.9 KNX IP Secure):
PBKDF2-HMAC-SHA256 password-hash derivation (65 536 iterations), AES-128 and
SHA-256. The keyring-file specifics below are verified against real ``.knxkeys``
keyring files:

- key derivation: PBKDF2-HMAC-SHA256(password, "1.keyring.ets.knx.org", 65536, 16)
- IV: first 16 bytes of SHA-256 over the ASCII ``Created`` attribute string
- secret encryption: AES-128-CBC, no padding, same key and IV for every secret
- password wrapping: 8 random bytes + ASCII password + PKCS7-style padding
- signature: SHA-256(canonical-XML || base64(passwordHash))[:16]

This module operates on raw bytes and XML byte streams only; it has no
dependency on the xsdata model (see ``secure.py`` for the model integration).

Known limitations (all irrelevant for the common ASCII/default-namespace case,
exercised by the tests against real keyring files):

- Passwords are encoded as UTF-8; a non-ASCII password with a different platform
  encoding would derive a different key. ASCII passwords are identical.
- The signature canonicalizer uses the SAX-reported (qualified) element and
  attribute names. Keyrings always use the default namespace, so these equal the
  local names; prefixed XML would differ.
"""

from __future__ import annotations

import base64
import hashlib
import os
import xml.sax
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import AttributesImpl

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Fixed KNX keyring salt/label; verified against real .knxkeys keyring files.
_KEYRING_SALT = b"1.keyring.ets.knx.org"
_PBKDF2_ITERATIONS = 65_536
_KEY_LENGTH = 16

# Number of leading random bytes prepended to a wrapped password.
_PASSWORD_SALT_LENGTH = 8
# Default payload length (password + padding) for wrapped passwords, giving a
# 32-byte (two AES block) secret. Device ``Password`` uses 56 (four blocks).
DEFAULT_PASSWORD_PAYLOAD_LENGTH = 24
DEVICE_PASSWORD_PAYLOAD_LENGTH = 56


def hash_keyring_password(password: bytes) -> bytes:
    """Derive the 16-byte AES key from the keyring password (PBKDF2-HMAC-SHA256)."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=_KEY_LENGTH,
        salt=_KEYRING_SALT,
        iterations=_PBKDF2_ITERATIONS,
    )
    return kdf.derive(password)


def derive_iv(created: str) -> bytes:
    """Derive the AES IV from the ``Created`` attribute string."""
    return hashlib.sha256(created.encode("ascii")).digest()[:_KEY_LENGTH]


def decrypt_aes128cbc(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt with AES-128-CBC, no padding."""
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()


def encrypt_aes128cbc(data: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt with AES-128-CBC, no padding. ``data`` must be a block multiple."""
    if len(data) % 16 != 0:
        msg = f"data length {len(data)} is not a multiple of the 16-byte AES block"
        raise ValueError(msg)
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return encryptor.update(data) + encryptor.finalize()


def extract_password(data: bytes) -> str:
    """Unwrap a decrypted password: drop 8-byte salt prefix and trailing padding."""
    if not data:
        return ""
    length = data[-1]
    return data[_PASSWORD_SALT_LENGTH:-length].decode("utf-8")


def wrap_password(
    password: str, payload_length: int = DEFAULT_PASSWORD_PAYLOAD_LENGTH
) -> bytes:
    """Wrap a password for encryption: 8 random bytes + ASCII + PKCS7-style padding.

    The result has length ``8 + payload_length`` (a multiple of 16). ``payload_length``
    must be a multiple of 16 minus 8 offset... in practice 24 (32-byte secret) or 56
    (64-byte secret) as used by the KNX keyring format.
    """
    encoded = password.encode("utf-8")
    pad_count = payload_length - len(encoded)
    if pad_count <= 0:
        msg = (
            f"password of {len(encoded)} bytes does not fit into payload length "
            f"{payload_length}"
        )
        raise ValueError(msg)
    padding = bytes([pad_count]) * pad_count
    return os.urandom(_PASSWORD_SALT_LENGTH) + encoded + padding


class _KeyringSAXContentHandler(ContentHandler):
    """SAX handler that builds the keyring's canonical signing stream."""

    _attribute_blacklist = ("xmlns", "Signature")

    def __init__(self, password_hash: bytes) -> None:
        self._password_hash = password_hash
        self.output = bytearray()
        super().__init__()

    def startElement(self, name: str, attrs: AttributesImpl) -> None:
        self.output.append(1)
        self._append(name)
        for attr_name, attr_value in sorted(attrs.items()):
            if attr_name not in self._attribute_blacklist:
                self._append(attr_name)
                self._append(attr_value)

    def endElement(self, name: str) -> None:
        self.output.append(2)

    def endDocument(self) -> None:
        self._append(base64.b64encode(self._password_hash))

    def _append(self, value: str | bytes) -> None:
        # The keyring signs strings length-prefixed with a 7-bit-encoded (LEB128)
        # byte count followed by the UTF-8 bytes. For values < 128 bytes this is a
        # single byte, but longer values (e.g. a many-address Senders list) need
        # the multi-byte varint. Verified against real keyrings and the xknx
        # reference (which is single-byte only, so diverges for values >= 128 B).
        if isinstance(value, str):
            value = value.encode("utf-8")
        length = len(value)
        while length >= 0x80:
            self.output.append((length & 0x7F) | 0x80)
            length >>= 7
        self.output.append(length)
        self.output.extend(value)


def compute_signature(xml_bytes: bytes, password: str) -> bytes:
    """Compute the 16-byte keyring signature over the canonicalized XML."""
    handler = _KeyringSAXContentHandler(hash_keyring_password(password.encode("utf-8")))
    xml.sax.parseString(xml_bytes, handler)
    return hashlib.sha256(handler.output).digest()[:_KEY_LENGTH]
