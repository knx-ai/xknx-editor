from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.hardware_t_products_product_baggages_baggage import (
    HardwareProductsProductBaggagesBaggage,
)


@dataclass(slots=True, kw_only=True)
class HardwareProductsProductBaggages:
    class Meta:
        global_type = False

    baggage: list[HardwareProductsProductBaggagesBaggage] = field(
        default_factory=list,
        metadata={
            "name": "Baggage",
            "type": "Element",
            "min_occurs": 1,
        },
    )
