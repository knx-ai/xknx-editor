from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.manufacturer_data_t_manufacturer_baggages_baggage import (
    ManufacturerDataManufacturerBaggagesBaggage,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerBaggages:
    class Meta:
        global_type = False

    baggage: list[ManufacturerDataManufacturerBaggagesBaggage] = field(
        default_factory=list,
        metadata={
            "name": "Baggage",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
            "min_occurs": 1,
        },
    )
