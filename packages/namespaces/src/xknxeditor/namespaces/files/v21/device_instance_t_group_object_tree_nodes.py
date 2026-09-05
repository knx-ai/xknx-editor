from __future__ import annotations

from dataclasses import dataclass, field

from xknxeditor.namespaces.files.v21.node_t import Node

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceGroupObjectTreeNodes:
    class Meta:
        global_type = False

    node: list[Node] = field(
        default_factory=list,
        metadata={
            "name": "Node",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
            "min_occurs": 1,
        },
    )
