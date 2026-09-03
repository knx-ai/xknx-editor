from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.datapoint_role_t import DatapointRole


@dataclass(slots=True, kw_only=True)
class MasterDataDatapointRoles:
    class Meta:
        global_type = False

    datapoint_role: list[DatapointRole] = field(
        default_factory=list,
        metadata={
            "name": "DatapointRole",
            "type": "Element",
        },
    )
