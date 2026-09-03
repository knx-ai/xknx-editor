from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.bus_access_t import BusAccess
from xknxmono.models.files.v20.completion_status_t import CompletionStatus
from xknxmono.models.files.v20.device_instance_t import DeviceInstance
from xknxmono.models.files.v20.topology_t_area_line_additional_group_addresses import (
    TopologyAreaLineAdditionalGroupAddresses,
)

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class TopologyAreaLine:
    class Meta:
        global_type = False

    device_instance: list[DeviceInstance] = field(
        default_factory=list,
        metadata={
            "name": "DeviceInstance",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    bus_access: None | BusAccess = field(
        default=None,
        metadata={
            "name": "BusAccess",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    additional_group_addresses: None | TopologyAreaLineAdditionalGroupAddresses = field(
        default=None,
        metadata={
            "name": "AdditionalGroupAddresses",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    address: int = field(
        metadata={
            "name": "Address",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 15,
        }
    )
    medium_type_ref_id: str = field(
        metadata={
            "name": "MediumTypeRefId",
            "type": "Attribute",
        }
    )
    comment: None | str = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
        },
    )
    domain_address: None | int = field(
        default=None,
        metadata={
            "name": "DomainAddress",
            "type": "Attribute",
        },
    )
    completion_status: None | CompletionStatus = field(
        default=None,
        metadata={
            "name": "CompletionStatus",
            "type": "Attribute",
        },
    )
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
        },
    )
    puid: int = field(
        metadata={
            "name": "Puid",
            "type": "Attribute",
        }
    )
