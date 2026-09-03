from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.hardware_t_products_product_attributes_attribute import (
    HardwareProductsProductAttributesAttribute,
)


@dataclass(slots=True, kw_only=True)
class HardwareProductsProductAttributes:
    class Meta:
        global_type = False

    attribute: list[HardwareProductsProductAttributesAttribute] = field(
        default_factory=list,
        metadata={
            "name": "Attribute",
            "type": "Element",
            "min_occurs": 1,
        },
    )
