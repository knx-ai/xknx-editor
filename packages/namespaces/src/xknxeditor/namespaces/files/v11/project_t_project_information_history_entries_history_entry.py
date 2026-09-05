from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ProjectProjectInformationHistoryEntriesHistoryEntry:
    class Meta:
        global_type = False

    date: XmlDateTime = field(
        metadata={
            "name": "Date",
            "type": "Attribute",
        }
    )
    user: None | str = field(
        default=None,
        metadata={
            "name": "User",
            "type": "Attribute",
            "max_length": 50,
        },
    )
    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
        }
    )
    detail: None | str = field(
        default=None,
        metadata={
            "name": "Detail",
            "type": "Attribute",
        },
    )
