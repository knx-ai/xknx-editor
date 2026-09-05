"""Build a :class:`DeviceSecurity` from a KNX keyring (``.knxkeys``).

A keyring stores each secure device's Tool Key encrypted with the keyring
password (KNX Standard v3.0.0, 3/5/1; the KNX keyring/.knxkeys format). xknx already
parses and decrypts a keyring - :func:`xknx.secure.keyring.sync_load_keyring`
returns a :class:`~xknx.secure.keyring.Keyring` whose ``devices`` carry the
``decrypted_tool_key`` - so this module only bridges that to the Tool-Key
material a secure download needs, keyed by the device's individual address.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xknx.secure.keyring import sync_load_keyring
from xknx.telegram.address import IndividualAddress

from .data_secure import DeviceSecurity, SecureProgrammingError

if TYPE_CHECKING:
    import os

    from xknx.secure.keyring import Keyring
    from xknx.telegram.address import IndividualAddressableType


def device_security_from_keyring(
    keyring: Keyring, address: IndividualAddressableType
) -> DeviceSecurity:
    """Return the Tool-Key security material for ``address`` from a loaded keyring.

    ``keyring`` must already be decrypted (as returned by
    :func:`xknx.secure.keyring.sync_load_keyring`). Raises
    :class:`SecureProgrammingError` if the keyring has no entry for the device
    or the entry carries no Tool Key.
    """
    individual_address = IndividualAddress(address)
    for device in keyring.devices:
        if device.individual_address != individual_address:
            continue
        if device.decrypted_tool_key is None:
            raise SecureProgrammingError(
                f"keyring entry for {individual_address} has no Tool Key"
            )
        return DeviceSecurity(individual_address, device.decrypted_tool_key)
    raise SecureProgrammingError(f"device {individual_address} not found in keyring")


def load_device_security(
    path: str | os.PathLike[str],
    password: str,
    address: IndividualAddressableType,
    *,
    validate_signature: bool = True,
) -> DeviceSecurity:
    """Load a ``.knxkeys`` file and return the Tool-Key material for ``address``.

    Convenience wrapper over :func:`xknx.secure.keyring.sync_load_keyring` and
    :func:`device_security_from_keyring`. Reads and decrypts the file
    synchronously; call it off the event loop in async contexts.
    """
    keyring = sync_load_keyring(path, password, validate_signature=validate_signature)
    return device_security_from_keyring(keyring, address)
