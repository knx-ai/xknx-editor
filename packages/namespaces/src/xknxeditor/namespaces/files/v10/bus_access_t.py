from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class BusAccess:
    class Meta:
        name = "BusAccess_t"

    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
        }
    )
    edi: str = field(
        metadata={
            "name": "Edi",
            "type": "Attribute",
            "pattern": r"\{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}\}",
        }
    )
    parameter: str = field(
        metadata={
            "name": "Parameter",
            "type": "Attribute",
        }
    )
