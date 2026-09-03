from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.bus_access_t import BusAccess
from xknxmono.models.files.v10.completion_status_t import CompletionStatus
from xknxmono.models.files.v10.device_instance_t import DeviceInstance
from xknxmono.models.files.v10.topology_t_area_line_additional_group_addresses import (
    TopologyAreaLineAdditionalGroupAddresses,
)

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class TopologyAreaLine:
    class Meta:
        global_type = False

    device_instance: list[DeviceInstance] = field(
        default_factory=list,
        metadata={
            "name": "DeviceInstance",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    bus_access: None | BusAccess = field(
        default=None,
        metadata={
            "name": "BusAccess",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    additional_group_addresses: None | TopologyAreaLineAdditionalGroupAddresses = field(
        default=None,
        metadata={
            "name": "AdditionalGroupAddresses",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
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
    domain_address_is_checked: bool = field(
        default=False,
        metadata={
            "name": "DomainAddressIsChecked",
            "type": "Attribute",
        },
    )
    iprouting_multicast_address: str = field(
        default="224.0.23.12",
        metadata={
            "name": "IPRoutingMulticastAddress",
            "type": "Attribute",
            "pattern": r"((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
        },
    )
    multicast_ttl: int = field(
        default=16,
        metadata={
            "name": "MulticastTTL",
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
