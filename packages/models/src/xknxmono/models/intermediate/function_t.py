from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.completion_status_t import CompletionStatus
from xknxmono.models.intermediate.group_address_ref_t import GroupAddressRef


@dataclass(slots=True, kw_only=True)
class Function:
    class Meta:
        name = "Function_t"

    group_address_ref: list[GroupAddressRef] = field(
        default_factory=list,
        metadata={
            "name": "GroupAddressRef",
            "type": "Element",
        },
    )
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
    type_value: None | str = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    number: None | str = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    comment: None | str = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
        },
    )
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
        },
    )
    completion_status: CompletionStatus = field(
        default=CompletionStatus.UNDEFINED,
        metadata={
            "name": "CompletionStatus",
            "type": "Attribute",
        },
    )
    default_group_range: None | str = field(
        default=None,
        metadata={
            "name": "DefaultGroupRange",
            "type": "Attribute",
        },
    )
    puid: int = field(
        metadata={
            "name": "Puid",
            "type": "Attribute",
        }
    )
    implements: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Implements",
            "type": "Attribute",
            "tokens": True,
        },
    )
    context: None | str = field(
        default=None,
        metadata={
            "name": "Context",
            "type": "Attribute",
        },
    )
