from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.master_data_t_property_data_types_property_data_type import (
    MasterDataPropertyDataTypesPropertyDataType,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class MasterDataPropertyDataTypes:
    class Meta:
        global_type = False

    property_data_type: list[MasterDataPropertyDataTypesPropertyDataType] = field(
        default_factory=list,
        metadata={
            "name": "PropertyDataType",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
            "min_occurs": 1,
        },
    )
