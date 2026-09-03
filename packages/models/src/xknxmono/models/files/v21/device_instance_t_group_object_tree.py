from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.device_instance_t_group_object_tree_nodes import (
    DeviceInstanceGroupObjectTreeNodes,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceGroupObjectTree:
    class Meta:
        global_type = False

    nodes: None | DeviceInstanceGroupObjectTreeNodes = field(
        default=None,
        metadata={
            "name": "Nodes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        },
    )
    group_object_instances: list[str] = field(
        default_factory=list,
        metadata={
            "name": "GroupObjectInstances",
            "type": "Attribute",
            "tokens": True,
        },
    )
