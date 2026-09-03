from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class ProjectTrace:
    class Meta:
        name = "ProjectTrace_t"

    date: XmlDateTime = field(
        metadata={
            "name": "Date",
            "type": "Attribute",
        }
    )
    user_name: str = field(
        metadata={
            "name": "UserName",
            "type": "Attribute",
        }
    )
    comment: str = field(
        metadata={
            "name": "Comment",
            "type": "Attribute",
        }
    )
