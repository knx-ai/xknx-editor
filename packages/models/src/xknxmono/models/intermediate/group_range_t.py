from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.group_address_t import GroupAddress
from xknxmono.models.intermediate.security_mode_t import SecurityMode


@dataclass(slots=True, kw_only=True)
class GroupRange:
    class Meta:
        name = "GroupRange_t"

    group_range: list[GroupRange] = field(
        default_factory=list,
        metadata={
            "name": "GroupRange",
            "type": "Element",
            "max_occurs": 65535,
        },
    )
    group_address: list[GroupAddress] = field(
        default_factory=list,
        metadata={
            "name": "GroupAddress",
            "type": "Element",
            "max_occurs": 65535,
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
    range_start: int = field(
        metadata={
            "name": "RangeStart",
            "type": "Attribute",
        }
    )
    range_end: int = field(
        metadata={
            "name": "RangeEnd",
            "type": "Attribute",
        }
    )
    unfiltered: bool = field(
        default=False,
        metadata={
            "name": "Unfiltered",
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
    comment: None | str = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
        },
    )
    puid: int = field(
        metadata={
            "name": "Puid",
            "type": "Attribute",
        }
    )
    security: SecurityMode = field(
        default=SecurityMode.AUTO,
        metadata={
            "name": "Security",
            "type": "Attribute",
        },
    )
