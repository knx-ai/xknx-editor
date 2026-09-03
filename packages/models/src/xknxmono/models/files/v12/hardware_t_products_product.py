from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.hardware_t_products_product_attributes import (
    HardwareProductsProductAttributes,
)
from xknxmono.models.files.v12.hardware_t_products_product_baggages import (
    HardwareProductsProductBaggages,
)
from xknxmono.models.files.v12.registration_info_t import RegistrationInfo

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class HardwareProductsProduct:
    """
    :ivar baggages:
    :ivar attributes:
    :ivar registration_info:
    :ivar id: registration-relevant
    :ivar text:
    :ivar order_number: registration-relevant
    :ivar is_rail_mounted:
    :ivar width_in_millimeter:
    :ivar visible_description:
    :ivar default_language:
    :ivar non_reg_relevant_data_version:
    :ivar hash:
    :ivar internal_description:
    """

    class Meta:
        global_type = False

    baggages: None | HardwareProductsProductBaggages = field(
        default=None,
        metadata={
            "name": "Baggages",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    attributes: None | HardwareProductsProductAttributes = field(
        default=None,
        metadata={
            "name": "Attributes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    registration_info: None | RegistrationInfo = field(
        default=None,
        metadata={
            "name": "RegistrationInfo",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    order_number: str = field(
        metadata={
            "name": "OrderNumber",
            "type": "Attribute",
            "max_length": 50,
        }
    )
    is_rail_mounted: bool = field(
        metadata={
            "name": "IsRailMounted",
            "type": "Attribute",
        }
    )
    width_in_millimeter: None | float = field(
        default=None,
        metadata={
            "name": "WidthInMillimeter",
            "type": "Attribute",
        },
    )
    visible_description: None | str = field(
        default=None,
        metadata={
            "name": "VisibleDescription",
            "type": "Attribute",
        },
    )
    default_language: None | str = field(
        default=None,
        metadata={
            "name": "DefaultLanguage",
            "type": "Attribute",
        },
    )
    non_reg_relevant_data_version: int = field(
        default=0,
        metadata={
            "name": "NonRegRelevantDataVersion",
            "type": "Attribute",
        },
    )
    hash: None | bytes = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Attribute",
            "format": "base64",
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
