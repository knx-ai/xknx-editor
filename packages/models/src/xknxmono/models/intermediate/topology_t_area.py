from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.completion_status_t import CompletionStatus
from xknxmono.models.intermediate.topology_t_area_line import TopologyAreaLine


@dataclass(slots=True, kw_only=True)
class TopologyArea:
    class Meta:
        global_type = False

    line: list[TopologyAreaLine] = field(
        default_factory=list,
        metadata={
            "name": "Line",
            "type": "Element",
            "max_occurs": 16,
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    address: int = field(
        metadata={
            "name": "Address",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 15,
        }
    )
    comment: None | str = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
        },
    )
    completion_status: None | CompletionStatus = field(
        default=None,
        metadata={
            "name": "CompletionStatus",
            "type": "Attribute",
        },
    )
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
        },
    )
    puid: int = field(
        metadata={
            "name": "Puid",
            "type": "Attribute",
        }
    )
