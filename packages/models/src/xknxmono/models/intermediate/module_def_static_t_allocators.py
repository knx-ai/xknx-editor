from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.allocator_t import Allocator


@dataclass(slots=True, kw_only=True)
class ModuleDefStaticAllocators:
    class Meta:
        global_type = False

    allocator: list[Allocator] = field(
        default_factory=list,
        metadata={
            "name": "Allocator",
            "type": "Element",
            "min_occurs": 1,
        },
    )
