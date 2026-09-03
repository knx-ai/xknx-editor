from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.access_t import Access

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ParameterRef:
    """
    :ivar id: registration-relevant
    :ivar ref_id: registration-relevant
    :ivar name:
    :ivar text:
    :ivar suffix_text:
    :ivar tag:
    :ivar display_order:
    :ivar access:
    :ivar value: registration-relevant
    :ivar initial_value:
    :ivar customer_adjustable: registration-relevant
    :ivar text_parameter_ref_id:
    :ivar internal_description:
    :ivar forbid_granting_use_by_customer:
    :ivar semantics:
    """

    class Meta:
        name = "ParameterRef_t"

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    suffix_text: None | str = field(
        default=None,
        metadata={
            "name": "SuffixText",
            "type": "Attribute",
            "max_length": 20,
        },
    )
    tag: None | str = field(
        default=None,
        metadata={
            "name": "Tag",
            "type": "Attribute",
            "max_length": 50,
        },
    )
    display_order: None | int = field(
        default=None,
        metadata={
            "name": "DisplayOrder",
            "type": "Attribute",
        },
    )
    access: None | Access = field(
        default=None,
        metadata={
            "name": "Access",
            "type": "Attribute",
        },
    )
    value: None | str = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
        },
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "InitialValue",
            "type": "Attribute",
        },
    )
    customer_adjustable: None | bool = field(
        default=None,
        metadata={
            "name": "CustomerAdjustable",
            "type": "Attribute",
        },
    )
    text_parameter_ref_id: None | str = field(
        default=None,
        metadata={
            "name": "TextParameterRefId",
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
    forbid_granting_use_by_customer: bool = field(
        default=False,
        metadata={
            "name": "ForbidGrantingUseByCustomer",
            "type": "Attribute",
        },
    )
    semantics: None | str = field(
        default=None,
        metadata={
            "name": "Semantics",
            "type": "Attribute",
        },
    )
