from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.device_instance_t_additional_addresses_address import (
    DeviceInstanceAdditionalAddressesAddress,
)


@dataclass(slots=True, kw_only=True)
class DeviceInstanceAdditionalAddresses:
    class Meta:
        global_type = False

    address: list[DeviceInstanceAdditionalAddressesAddress] = field(
        default_factory=list,
        metadata={
            "name": "Address",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 254,
        },
    )
