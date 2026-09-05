from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class MasterDataInterfaceObjectTypesInterfaceObjectType:
    class Meta:
        global_type = False

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
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        },
    )
