from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.building_part_t import BuildingPart

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class Locations:
    class Meta:
        name = "Locations_t"

    building_part: list[BuildingPart] = field(
        default_factory=list,
        metadata={
            "name": "BuildingPart",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        },
    )
