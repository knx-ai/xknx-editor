from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.hawk_configuration_data_t_interface_objects_interface_object_property import (
    HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataInterfaceObjectsInterfaceObject:
    class Meta:
        global_type = False

    property: list[HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty] = (
        field(
            default_factory=list,
            metadata={
                "name": "Property",
                "type": "Element",
                "namespace": "http://knx.org/xml/project/12",
            },
        )
    )
    index: None | int = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Attribute",
        },
    )
    object_type: int = field(
        metadata={
            "name": "ObjectType",
            "type": "Attribute",
        }
    )
