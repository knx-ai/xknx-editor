from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.resource_addr_space_t import ResourceAddrSpace
from xknxmono.models.files.v12.resource_name_t import ResourceName

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ResourceLocation:
    class Meta:
        name = "ResourceLocation_t"

    address_space: ResourceAddrSpace = field(
        metadata={
            "name": "AddressSpace",
            "type": "Attribute",
        }
    )
    interface_object_ref: None | int = field(
        default=None,
        metadata={
            "name": "InterfaceObjectRef",
            "type": "Attribute",
        },
    )
    property_id: None | int = field(
        default=None,
        metadata={
            "name": "PropertyID",
            "type": "Attribute",
        },
    )
    start_address: None | int = field(
        default=None,
        metadata={
            "name": "StartAddress",
            "type": "Attribute",
        },
    )
    occurrence: int = field(
        default=0,
        metadata={
            "name": "Occurrence",
            "type": "Attribute",
        },
    )
    ptr_resource: None | ResourceName = field(
        default=None,
        metadata={
            "name": "PtrResource",
            "type": "Attribute",
        },
    )
