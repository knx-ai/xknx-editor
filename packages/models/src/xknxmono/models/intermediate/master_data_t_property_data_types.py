from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.master_data_t_property_data_types_property_data_type import (
    MasterDataPropertyDataTypesPropertyDataType,
)


@dataclass(slots=True, kw_only=True)
class MasterDataPropertyDataTypes:
    class Meta:
        global_type = False

    property_data_type: list[MasterDataPropertyDataTypesPropertyDataType] = field(
        default_factory=list,
        metadata={
            "name": "PropertyDataType",
            "type": "Element",
        },
    )
