from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.bus_access_t import BusAccess
from xknxmono.models.files.v23.completion_status_t import CompletionStatus
from xknxmono.models.files.v23.device_instance_t import DeviceInstance
from xknxmono.models.files.v23.topology_t_area_line_segment_additional_group_addresses import (
    TopologyAreaLineSegmentAdditionalGroupAddresses,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class TopologyAreaLineSegment:
    class Meta:
        global_type = False

    device_instance: list[DeviceInstance] = field(
        default_factory=list,
        metadata={
            "name": "DeviceInstance",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    bus_access: None | BusAccess = field(
        default=None,
        metadata={
            "name": "BusAccess",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    additional_group_addresses: (
        None | TopologyAreaLineSegmentAdditionalGroupAddresses
    ) = field(
        default=None,
        metadata={
            "name": "AdditionalGroupAddresses",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    number: int = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 127,
        }
    )
    medium_type_ref_id: str = field(
        metadata={
            "name": "MediumTypeRefId",
            "type": "Attribute",
        }
    )
    domain_address: None | int = field(
        default=None,
        metadata={
            "name": "DomainAddress",
            "type": "Attribute",
        },
    )
    master_salt: None | str = field(
        default=None,
        metadata={
            "name": "MasterSalt",
            "type": "Attribute",
        },
    )
    comment: None | str = field(
        default=None,
        metadata={
            "name": "Comment",
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
