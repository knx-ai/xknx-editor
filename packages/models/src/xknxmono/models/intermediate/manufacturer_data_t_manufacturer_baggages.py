from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.manufacturer_data_t_manufacturer_baggages_baggage import (
    ManufacturerDataManufacturerBaggagesBaggage,
)


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerBaggages:
    class Meta:
        global_type = False

    baggage: list[ManufacturerDataManufacturerBaggagesBaggage] = field(
        default_factory=list,
        metadata={
            "name": "Baggage",
            "type": "Element",
            "min_occurs": 1,
        },
    )
