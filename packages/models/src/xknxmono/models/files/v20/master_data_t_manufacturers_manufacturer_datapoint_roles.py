from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.datapoint_role_t import DatapointRole

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturerDatapointRoles:
    class Meta:
        global_type = False

    datapoint_role: list[DatapointRole] = field(
        default_factory=list,
        metadata={
            "name": "DatapointRole",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
            "min_occurs": 1,
        },
    )
