from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ParameterInstanceRef:
    class Meta:
        name = "ParameterInstanceRef_t"

    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        },
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    value: None | str = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
        },
    )
    grant_use_by_customer: bool = field(
        default=False,
        metadata={
            "name": "GrantUseByCustomer",
            "type": "Attribute",
        },
    )
    customized_text: None | str = field(
        default=None,
        metadata={
            "name": "CustomizedText",
            "type": "Attribute",
        },
    )
