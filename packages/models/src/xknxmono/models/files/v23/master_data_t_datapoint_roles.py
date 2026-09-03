from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.datapoint_role_t import DatapointRole

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class MasterDataDatapointRoles:
    class Meta:
        global_type = False

    datapoint_role: list[DatapointRole] = field(
        default_factory=list,
        metadata={
            "name": "DatapointRole",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
