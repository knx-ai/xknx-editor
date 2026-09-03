from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.hardware_t_products_product_baggages_baggage import (
    HardwareProductsProductBaggagesBaggage,
)

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class HardwareProductsProductBaggages:
    class Meta:
        global_type = False

    baggage: list[HardwareProductsProductBaggagesBaggage] = field(
        default_factory=list,
        metadata={
            "name": "Baggage",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/14",
            "min_occurs": 1,
        },
    )
