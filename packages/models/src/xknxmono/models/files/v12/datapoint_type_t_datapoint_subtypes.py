from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype import (
    DatapointTypeDatapointSubtypesDatapointSubtype,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypes:
    class Meta:
        global_type = False

    datapoint_subtype: list[DatapointTypeDatapointSubtypesDatapointSubtype] = field(
        default_factory=list,
        metadata={
            "name": "DatapointSubtype",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
            "min_occurs": 1,
        },
    )
