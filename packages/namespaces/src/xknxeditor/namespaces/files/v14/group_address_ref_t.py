from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class GroupAddressRef:
    class Meta:
        name = "GroupAddressRef_t"

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
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    role: None | str = field(
        default=None,
        metadata={
            "name": "Role",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    puid: int = field(
        metadata={
            "name": "Puid",
            "type": "Attribute",
        }
    )
