from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.hardware_t_products_product_attributes_attribute import (
    HardwareProductsProductAttributesAttribute,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class HardwareProductsProductAttributes:
    class Meta:
        global_type = False

    attribute: list[HardwareProductsProductAttributesAttribute] = field(
        default_factory=list,
        metadata={
            "name": "Attribute",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
            "min_occurs": 1,
        },
    )
