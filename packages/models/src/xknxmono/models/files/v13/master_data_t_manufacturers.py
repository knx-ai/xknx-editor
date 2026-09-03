from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.master_data_t_manufacturers_manufacturer import (
    MasterDataManufacturersManufacturer,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturers:
    class Meta:
        global_type = False

    manufacturer: list[MasterDataManufacturersManufacturer] = field(
        default_factory=list,
        metadata={
            "name": "Manufacturer",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
            "min_occurs": 1,
        },
    )
