from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.deprecation_status_t import DeprecationStatus


@dataclass(slots=True, kw_only=True)
class SpaceUsage:
    class Meta:
        name = "SpaceUsage_t"

    space_usage: list[SpaceUsage] = field(
        default_factory=list,
        metadata={
            "name": "SpaceUsage",
            "type": "Element",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    number: int = field(
        metadata={
            "name": "Number",
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
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    relations: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Relations",
            "type": "Attribute",
            "tokens": True,
        },
    )
    status: DeprecationStatus = field(
        default=DeprecationStatus.ACTIVE,
        metadata={
            "name": "Status",
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
