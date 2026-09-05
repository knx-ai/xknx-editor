from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationTagsTag:
    class Meta:
        global_type = False

    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 20,
        }
    )
    color: str = field(
        metadata={
            "name": "Color",
            "type": "Attribute",
            "length": 7,
            "pattern": r"#[0-9A-F]{6}",
        }
    )
