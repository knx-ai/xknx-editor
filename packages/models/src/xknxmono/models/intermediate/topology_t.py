from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.topology_t_area import TopologyArea
from xknxmono.models.intermediate.topology_t_unassigned_devices import (
    TopologyUnassignedDevices,
)


@dataclass(slots=True, kw_only=True)
class Topology:
    class Meta:
        name = "Topology_t"

    area: list[TopologyArea] = field(
        default_factory=list,
        metadata={
            "name": "Area",
            "type": "Element",
            "max_occurs": 16,
        },
    )
    unassigned_devices: None | TopologyUnassignedDevices = field(
        default=None,
        metadata={
            "name": "UnassignedDevices",
            "type": "Element",
        },
    )
