from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class UserFile:
    class Meta:
        name = "UserFile_t"

    filename: str = field(
        metadata={
            "name": "Filename",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    comment: None | str = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
        },
    )
