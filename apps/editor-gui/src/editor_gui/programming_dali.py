"""Glue between the GUI/connection stack and the MDT DALI commissioning library.

Opens a (optionally Tool-Key secured) point-to-point connection to a DALI gateway, builds an
``MdtDaliCommissioner`` on the same ``DeviceProgrammer`` the download flows use, runs one caller
supplied coroutine against it, and always closes the connection. Kept out of the plugins so the
connection service stays thin and this is unit-testable.
"""

from __future__ import annotations

import contextlib
from collections.abc import Awaitable, Callable

from xknx import XKNX
from xknx.telegram import IndividualAddress

from xknxeditor.dali import MdtDaliCommissioner, MdtDaliConnection
from xknxeditor.download import DeviceProgrammer, DeviceSecurity

# Reuse the download package's own connection builders (plain or Tool-Key secured) so a DALI session
# gets the same secure handling as a normal download. Repo-internal; intentional cross-module use.
from xknxeditor.download.download import (
    _apdu_overhead,  # pyright: ignore[reportPrivateUsage]
    _connection_manager,  # pyright: ignore[reportPrivateUsage]
)

# MDT DALI Control gateway application-id prefixes (manufacturer M-0083; 1x64 / 2x64 + presence
# variants). Matched as a prefix of the full ``Application.id`` (e.g. "M-0083_A-0154-40-0F69-O00EF").
_MDT_DALI_PREFIXES = tuple(f"M-0083_A-{n}" for n in ("0153", "0154", "0155", "0158"))


def is_mdt_dali_app(app_id: str | None) -> bool:
    """Whether ``app_id`` is an MDT DALI Control gateway application (gates the commissioning tab)."""
    return bool(app_id) and app_id.upper().startswith(_MDT_DALI_PREFIXES)


async def run_dali_operation[T](
    xknx: XKNX,
    address: str,
    security: DeviceSecurity | None,
    channel: int,
    op: Callable[[MdtDaliCommissioner], Awaitable[T]],
) -> T:
    """Open a connection to ``address``, run ``op`` against an ``MdtDaliCommissioner``, then close.

    ``security`` (from the keyring) enables a Tool-Key secured session, matching the download flows.
    """
    target = IndividualAddress(address)
    manager = _connection_manager(xknx, target, security)
    connection = await manager.open()
    try:
        programmer = DeviceProgrammer(
            connection, apdu_overhead=_apdu_overhead(security)
        )
        # Negotiate the device's real APDU length (defaults to the mandatory 15). Multi-byte DALI
        # property writes (and a secure session's overhead) would not fit the 15-octet default.
        programmer.max_apdu_length = await programmer.read_max_apdu_length()
        commissioner = MdtDaliCommissioner(MdtDaliConnection(programmer, channel))
        return await op(commissioner)
    finally:
        with contextlib.suppress(Exception):
            await manager.close()
