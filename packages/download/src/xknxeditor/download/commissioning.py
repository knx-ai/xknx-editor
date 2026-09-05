"""Program a device's individual address before downloading an application.

A virgin device (or one whose address is unknown) has to be given its individual
address first. Two ways are supported, both delegating to ``xknx``'s network
management procedures:

- via programming mode: exactly one device on the bus must be in programming
  mode; its address is written by broadcast.
- via serial number: the target device is addressed by its serial number, so no
  programming mode is required and several devices may be on the bus.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xknx.management.procedures.network.nm_individual_address_serial_number_write import (
    nm_individual_address_serial_number_write,
)
from xknx.management.procedures.network.nm_individual_address_write import (
    nm_individual_address_write,
)

if TYPE_CHECKING:
    from xknx import XKNX
    from xknx.telegram.address import IndividualAddressableType


async def program_individual_address(
    xknx: XKNX,
    individual_address: IndividualAddressableType,
    *,
    serial_number: bytes | None = None,
) -> None:
    """Program ``individual_address`` into a device.

    With ``serial_number`` the device is addressed by serial number; otherwise
    the single device currently in programming mode is addressed. ``xknx`` has to
    be started.
    """
    if serial_number is not None:
        await nm_individual_address_serial_number_write(
            xknx, serial_number, individual_address
        )
        return
    await nm_individual_address_write(xknx, individual_address)
