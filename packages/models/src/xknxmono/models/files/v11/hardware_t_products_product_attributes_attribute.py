from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.hardware_t_products_product_attributes_attribute_name import (
    HardwareProductsProductAttributesAttributeName,
)

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class HardwareProductsProductAttributesAttribute:
    class Meta:
        global_type = False

    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        },
    )
    name: HardwareProductsProductAttributesAttributeName = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
        }
    )
    value: str = field(
        metadata={
            "name": "Value",
            "type": "Attribute",
            "max_length": 255,
        }
    )
