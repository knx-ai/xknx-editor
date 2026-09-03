from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.master_data_t_interface_object_types_interface_object_type import (
    MasterDataInterfaceObjectTypesInterfaceObjectType,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class MasterDataInterfaceObjectTypes:
    class Meta:
        global_type = False

    interface_object_type: list[MasterDataInterfaceObjectTypesInterfaceObjectType] = (
        field(
            default_factory=list,
            metadata={
                "name": "InterfaceObjectType",
                "type": "Element",
                "namespace": "http://knx.org/xml/project/12",
                "min_occurs": 1,
            },
        )
    )
