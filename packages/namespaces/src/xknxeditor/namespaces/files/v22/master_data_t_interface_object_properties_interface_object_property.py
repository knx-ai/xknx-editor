from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class MasterDataInterfaceObjectPropertiesInterfaceObjectProperty:
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
    object_type: None | str = field(
        default=None,
        metadata={
            "name": "ObjectType",
            "type": "Attribute",
        },
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
    pdt: list[str] = field(
        default_factory=list,
        metadata={
            "name": "PDT",
            "type": "Attribute",
            "tokens": True,
        },
    )
    dpt: None | str = field(
        default=None,
        metadata={
            "name": "DPT",
            "type": "Attribute",
        },
    )
    array: bool = field(
        default=False,
        metadata={
            "name": "Array",
            "type": "Attribute",
        },
    )
    access_policy: None | str = field(
        default=None,
        metadata={
            "name": "AccessPolicy",
            "type": "Attribute",
            "pattern": r"[0-3][0-9A-F]{2}/[0-3][0-9A-F]{2}",
        },
    )
