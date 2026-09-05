"""Keyring service: import a password-protected KNX ``.knxkeys`` keyring, hold its decrypted
contents in memory, and export (convert) it under a new password.

Uses this project's own, verified ``xknxeditor-datasecure`` crypto (``xknxeditor.datasecure``) — decrypt,
re-encrypt and re-sign — rather than xknx's read-only loader. The keyring is runtime-only state
(never persisted into the project document)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from xknx.exceptions import CouldNotParseAddress
from xknx.telegram.address import IndividualAddress

from xknxeditor.datasecure import (
    DecryptedKeyring,
    KeyringSignatureError,
    load_and_decrypt,
    load_keyring,
    reencrypt_keyring,
    serialize_keyring,
)
from xknxeditor.datasecure.files.knx_keyring import Keyring

if TYPE_CHECKING:
    from editor_gui.plugins.base import Logger
    from xknxeditor.download.data_secure import DeviceSecurity


class KeyringService:
    def __init__(self) -> None:
        self._log: Logger
        self._model: Keyring | None = None
        self._decrypted: DecryptedKeyring | None = None
        self._password: str | None = None
        self._path: Path | None = None

    def set_logger(self, log: Logger) -> None:
        self._log = log

    @property
    def keyring(self) -> Keyring | None:
        """The parsed keyring model (metadata + encrypted attributes), or ``None``."""
        return self._model

    @property
    def decrypted(self) -> DecryptedKeyring | None:
        """The decrypted key material, or ``None`` when no keyring is loaded."""
        return self._decrypted

    @property
    def path(self) -> Path | None:
        return self._path

    @property
    def project_name(self) -> str:
        return self._model.project if self._model is not None else ""

    @property
    def created_by(self) -> str:
        return self._model.created_by if self._model is not None else ""

    def load(self, path: Path, password: str) -> None:
        """Decrypt and load a keyring. Raises on a wrong password / invalid file.

        Verification runs over the original bytes (authoritative), then the model
        is parsed for metadata and re-export.
        """
        data = path.read_bytes()
        decrypted = load_and_decrypt(data, password)  # raises KeyringSignatureError
        self._model = load_keyring(data)
        self._decrypted = decrypted
        self._password = password
        self._path = path
        self._log.info("keyring loaded", path=str(path))

    def export(
        self, path: Path, password: str, *, new_created: str | None = None
    ) -> None:
        """Write the loaded keyring to ``path``, re-encrypted+signed under ``password``.

        The same key material under a (possibly) different keyring password — a
        "convert / export keyring" operation. Requires a keyring to be loaded.
        """
        if self._model is None or self._password is None:
            raise KeyringSignatureError("no keyring loaded to export")
        converted = reencrypt_keyring(
            self._model, self._password, password, new_created=new_created
        )
        path.write_bytes(serialize_keyring(converted))
        self._log.info("keyring exported", path=str(path))

    def clear(self) -> None:
        self._model = None
        self._decrypted = None
        self._password = None
        self._path = None

    def device_security(self, individual_address: str) -> DeviceSecurity | None:
        """KNX Data Secure Tool-Key material for ``individual_address`` from the loaded keyring, or
        ``None`` when no keyring is loaded or it holds no tool key for that address.

        A returned value means the device was commissioned secure and a point-to-point download to
        it must be secured with this tool key; ``None`` means program in the clear."""
        # Snapshot once: load()/clear() may run on another thread (the MCP server).
        decrypted = self._decrypted
        if decrypted is None or not individual_address:
            return None
        from xknxeditor.download.data_secure import DeviceSecurity

        try:
            target = IndividualAddress(individual_address)
        except CouldNotParseAddress:
            return None
        for device in decrypted.devices:
            if device.tool_key is None:
                continue
            try:
                if IndividualAddress(device.individual_address) == target:
                    return DeviceSecurity(target, device.tool_key)
            except CouldNotParseAddress:
                continue
        return None

    def is_loaded(self) -> bool:
        """Whether a keyring is currently loaded (a single snapshot read)."""
        return self._model is not None
