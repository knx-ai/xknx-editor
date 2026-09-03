from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.hawk_configuration_data_t_interface_objects_interface_object import (
    HawkConfigurationDataInterfaceObjectsInterfaceObject,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class HawkConfigurationDataInterfaceObjects:
    class Meta:
        global_type = False

    interface_object: list[HawkConfigurationDataInterfaceObjectsInterfaceObject] = (
        field(
            default_factory=list,
            metadata={
                "name": "InterfaceObject",
                "type": "Element",
                "namespace": "http://knx.org/xml/project/13",
                "min_occurs": 1,
            },
        )
    )
