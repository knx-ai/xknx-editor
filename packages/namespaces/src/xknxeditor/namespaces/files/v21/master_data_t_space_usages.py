from __future__ import annotations

from dataclasses import dataclass, field

from xknxeditor.namespaces.files.v21.space_usage_t import SpaceUsage

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class MasterDataSpaceUsages:
    class Meta:
        global_type = False

    space_usage: list[SpaceUsage] = field(
        default_factory=list,
        metadata={
            "name": "SpaceUsage",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
            "min_occurs": 1,
        },
    )
