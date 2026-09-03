from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.access_t import Access

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ParameterBase:
    """
    :ivar id: registration-relevant
    :ivar name:
    :ivar parameter_type: registration-relevant
    :ivar parameter_type_params:
    :ivar text:
    :ivar suffix_text:
    :ivar access:
    :ivar value: registration-relevant
    :ivar initial_value:
    :ivar customer_adjustable: registration-relevant
    :ivar internal_description:
    """

    class Meta:
        name = "ParameterBase_t"

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    parameter_type: str = field(
        metadata={
            "name": "ParameterType",
            "type": "Attribute",
        }
    )
    parameter_type_params: list[str] = field(
        default_factory=list,
        metadata={
            "name": "ParameterTypeParams",
            "type": "Attribute",
            "tokens": True,
        },
    )
    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    suffix_text: None | str = field(
        default=None,
        metadata={
            "name": "SuffixText",
            "type": "Attribute",
            "max_length": 20,
        },
    )
    access: Access = field(
        default=Access.READ_WRITE,
        metadata={
            "name": "Access",
            "type": "Attribute",
        },
    )
    value: str = field(
        metadata={
            "name": "Value",
            "type": "Attribute",
        }
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "InitialValue",
            "type": "Attribute",
        },
    )
    customer_adjustable: bool = field(
        default=False,
        metadata={
            "name": "CustomerAdjustable",
            "type": "Attribute",
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
