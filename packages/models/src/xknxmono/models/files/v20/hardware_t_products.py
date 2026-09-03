from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.hardware_t_products_product import (
    HardwareProductsProduct,
)

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class HardwareProducts:
    class Meta:
        global_type = False

    product: list[HardwareProductsProduct] = field(
        default_factory=list,
        metadata={
            "name": "Product",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
