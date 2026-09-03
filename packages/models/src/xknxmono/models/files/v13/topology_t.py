from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.topology_t_area import TopologyArea
from xknxmono.models.files.v13.topology_t_unassigned_devices import (
    TopologyUnassignedDevices,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class Topology:
    class Meta:
        name = "Topology_t"

    area: list[TopologyArea] = field(
        default_factory=list,
        metadata={
            "name": "Area",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
            "max_occurs": 16,
        },
    )
    unassigned_devices: None | TopologyUnassignedDevices = field(
        default=None,
        metadata={
            "name": "UnassignedDevices",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        },
    )
