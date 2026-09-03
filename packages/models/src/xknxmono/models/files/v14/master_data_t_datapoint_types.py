from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.datapoint_type_t import DatapointType

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class MasterDataDatapointTypes:
    class Meta:
        global_type = False

    datapoint_type: list[DatapointType] = field(
        default_factory=list,
        metadata={
            "name": "DatapointType",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/14",
            "min_occurs": 1,
        },
    )
