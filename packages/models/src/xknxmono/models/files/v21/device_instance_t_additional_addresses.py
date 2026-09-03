from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.device_instance_t_additional_addresses_address import (
    DeviceInstanceAdditionalAddressesAddress,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceAdditionalAddresses:
    class Meta:
        global_type = False

    address: list[DeviceInstanceAdditionalAddressesAddress] = field(
        default_factory=list,
        metadata={
            "name": "Address",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
            "min_occurs": 1,
            "max_occurs": 254,
        },
    )
