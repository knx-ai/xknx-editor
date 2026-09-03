from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class FunctionTypeFunctionPoint:
    class Meta:
        global_type = False

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
    role: str = field(
        metadata={
            "name": "Role",
            "type": "Attribute",
        }
    )
    datapoint_type: str = field(
        metadata={
            "name": "DatapointType",
            "type": "Attribute",
        }
    )
    characteristics: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Characteristics",
            "type": "Attribute",
            "tokens": True,
        },
    )
    semantics: None | str = field(
        default=None,
        metadata={
            "name": "Semantics",
            "type": "Attribute",
        },
    )
