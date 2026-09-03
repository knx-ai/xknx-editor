from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.node_t import Node


@dataclass(slots=True, kw_only=True)
class DeviceInstanceGroupObjectTreeNodes:
    class Meta:
        global_type = False

    node: list[Node] = field(
        default_factory=list,
        metadata={
            "name": "Node",
            "type": "Element",
        },
    )
