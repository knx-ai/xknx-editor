from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.hardware_t_products_product import (
    HardwareProductsProduct,
)


@dataclass(slots=True, kw_only=True)
class HardwareProducts:
    class Meta:
        global_type = False

    product: list[HardwareProductsProduct] = field(
        default_factory=list,
        metadata={
            "name": "Product",
            "type": "Element",
            "min_occurs": 1,
        },
    )
