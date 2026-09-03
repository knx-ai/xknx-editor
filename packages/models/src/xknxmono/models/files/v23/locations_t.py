from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.space_t import Space

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class Locations:
    class Meta:
        name = "Locations_t"

    space: list[Space] = field(
        default_factory=list,
        metadata={
            "name": "Space",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
