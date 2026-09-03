from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.datapoint_type_t_datapoint_subtypes_datapoint_subtype import (
    DatapointTypeDatapointSubtypesDatapointSubtype,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypes:
    class Meta:
        global_type = False

    datapoint_subtype: list[DatapointTypeDatapointSubtypesDatapointSubtype] = field(
        default_factory=list,
        metadata={
            "name": "DatapointSubtype",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
