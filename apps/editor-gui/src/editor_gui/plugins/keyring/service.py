"""Keyring service: load a password-protected ETS ``.knxkeys`` keyring and hold it in memory.

Uses xknx's own keyring loader (which decrypts), not the toolkit's plaintext-only ``xknx-keyring``
package. The keyring is runtime-only state (never persisted into the project document)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from xknx.exceptions import CouldNotParseAddress
from xknx.secure.keyring import Keyring, sync_load_keyring

if TYPE_CHECKING:
    from editor_gui.plugins.base import Logger
    from xknxmono.download.data_secure import DeviceSecurity


class KeyringService:
    def __init__(self) -> None:
        self._log: Logger
        self._keyring: Keyring | None = None
        self._path: Path | None = None

    def set_logger(self, log: Logger) -> None:
        self._log = log

    @property
    def keyring(self) -> Keyring | None:
        return self._keyring

    @property
    def path(self) -> Path | None:
        return self._path

    def load(self, path: Path, password: str) -> None:
        """Decrypt and load a keyring. Raises on a wrong password / invalid file."""
        keyring = sync_load_keyring(path, password)
        self._keyring = keyring
        self._path = path
        self._log.info("keyring loaded", path=str(path))

    def clear(self) -> None:
        self._keyring = None
        self._path = None

    def device_security(self, individual_address: str) -> DeviceSecurity | None:
        """KNX Data Secure tool-key material for ``individual_address`` from the loaded keyring, or
        ``None`` when no keyring is loaded or it holds no (decrypted) tool key for that address.

        A returned value means the device was commissioned secure and a point-to-point download to
        it must be secured with this tool key; ``None`` means program in the clear."""
        # Snapshot the keyring once: load()/clear() may run on another thread (the MCP server), so
        # reading self._keyring separately for a check and a use would race to an AttributeError.
        keyring = self._keyring
        if keyring is None or not individual_address:
            return None
        # Reuse the download package's keyring->tool-key bridge (single source of truth); it raises
        # when the keyring has no entry / no tool key for the address, which here just means "not
        # secure -> program in the clear".
        from xknxmono.download import device_security_from_keyring
        from xknxmono.download.data_secure import SecureProgrammingError

        try:
            return device_security_from_keyring(keyring, individual_address)
        except (SecureProgrammingError, CouldNotParseAddress):
            return None

    def is_loaded(self) -> bool:
        """Whether a keyring is currently loaded (a single snapshot read)."""
        return self._keyring is not None
