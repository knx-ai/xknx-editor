from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.master_data_t_interface_object_properties_interface_object_property import (
    MasterDataInterfaceObjectPropertiesInterfaceObjectProperty,
)

__NAMESPACE__ = "http://knx.org/xml/project/22"


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
            "namespace": "http://knx.org/xml/project/22",
            "min_occurs": 1,
        },
    )
