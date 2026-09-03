from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.master_data_t_interface_object_properties_interface_object_property import (
    MasterDataInterfaceObjectPropertiesInterfaceObjectProperty,
)


@dataclass(slots=True, kw_only=True)
class MasterDataInterfaceObjectProperties:
    class Meta:
        global_type = False

    interface_object_property: list[
        MasterDataInterfaceObjectPropertiesInterfaceObjectProperty
    ] = field(
        default_factory=list,
        metadata={
            "name": "InterfaceObjectProperty",
            "type": "Element",
        },
    )
