from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.hardware_t import Hardware

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerHardware:
    class Meta:
        global_type = False

    hardware: list[Hardware] = field(
        default_factory=list,
        metadata={
            "name": "Hardware",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
            "min_occurs": 1,
        },
    )
