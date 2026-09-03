from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.manufacturer_data_t_manufacturer import (
    ManufacturerDataManufacturer,
)


@dataclass(slots=True, kw_only=True)
class ManufacturerData:
    class Meta:
        name = "ManufacturerData_t"

    manufacturer: list[ManufacturerDataManufacturer] = field(
        default_factory=list,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "min_occurs": 1,
        },
    )
