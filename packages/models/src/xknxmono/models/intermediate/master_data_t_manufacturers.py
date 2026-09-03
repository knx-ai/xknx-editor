from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer import (
    MasterDataManufacturersManufacturer,
)


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturers:
    class Meta:
        global_type = False

    manufacturer: list[MasterDataManufacturersManufacturer] = field(
        default_factory=list,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "min_occurs": 1,
        },
    )
