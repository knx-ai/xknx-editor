from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class SplitInfo:
    class Meta:
        name = "SplitInfo_t"

    object_path: str = field(
        metadata={
            "name": "ObjectPath",
            "type": "Attribute",
        }
    )
    cookie: str = field(
        metadata={
            "name": "Cookie",
            "type": "Attribute",
            "pattern": r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
        }
    )
