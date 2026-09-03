from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class AddinData:
    class Meta:
        name = "AddinData_t"

    addin_id: str = field(
        metadata={
            "name": "AddinId",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 50,
        }
    )
