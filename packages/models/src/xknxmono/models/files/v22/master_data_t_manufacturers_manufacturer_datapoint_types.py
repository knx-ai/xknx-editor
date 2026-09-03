from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.datapoint_type_t import DatapointType

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturerDatapointTypes:
    class Meta:
        global_type = False

    datapoint_type: list[DatapointType] = field(
        default_factory=list,
        metadata={
            "name": "DatapointType",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
