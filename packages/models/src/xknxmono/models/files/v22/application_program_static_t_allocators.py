from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.allocator_t import Allocator

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticAllocators:
    class Meta:
        global_type = False

    allocator: list[Allocator] = field(
        default_factory=list,
        metadata={
            "name": "Allocator",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
