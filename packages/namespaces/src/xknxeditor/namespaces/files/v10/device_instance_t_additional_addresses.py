from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceAdditionalAddresses:
    class Meta:
        global_type = False

    address: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Address",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
            "min_occurs": 1,
            "max_occurs": 254,
            "min_inclusive": 1,
            "max_inclusive": 255,
        },
    )
