from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.manufacturer_data_t_manufacturer import (
    ManufacturerDataManufacturer,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class ManufacturerData:
    class Meta:
        name = "ManufacturerData_t"

    manufacturer: list[ManufacturerDataManufacturer] = field(
        default_factory=list,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
            "min_occurs": 1,
        },
    )
