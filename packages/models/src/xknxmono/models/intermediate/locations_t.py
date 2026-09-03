from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.space_t import Space


@dataclass(slots=True, kw_only=True)
class Locations:
    class Meta:
        name = "Locations_t"

    space: list[Space] = field(
        default_factory=list,
        metadata={
            "name": "Space",
            "type": "Element",
        },
    )
