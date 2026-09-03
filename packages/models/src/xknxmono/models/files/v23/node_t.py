from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.node_t_type import NodeType

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class Node:
    class Meta:
        name = "Node_t"

    nodes: None | NodeNodes = field(
        default=None,
        metadata={
            "name": "Nodes",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    type_value: NodeType = field(
        metadata={
            "name": "Type",
            "type": "Attribute",
        }
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
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


@dataclass(slots=True, kw_only=True)
class NodeNodes:
    class Meta:
        global_type = False

    node: list[Node] = field(
        default_factory=list,
        metadata={
            "name": "Node",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
