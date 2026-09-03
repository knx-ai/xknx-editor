from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.allocator_t import Allocator

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticAllocators:
    class Meta:
        global_type = False

    allocator: list[Allocator] = field(
        default_factory=list,
        metadata={
            "name": "Allocator",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
