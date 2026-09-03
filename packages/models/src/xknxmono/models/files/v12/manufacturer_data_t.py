from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.manufacturer_data_t_manufacturer import (
    ManufacturerDataManufacturer,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ManufacturerData:
    class Meta:
        name = "ManufacturerData_t"

    manufacturer: list[ManufacturerDataManufacturer] = field(
        default_factory=list,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
            "min_occurs": 1,
        },
    )
