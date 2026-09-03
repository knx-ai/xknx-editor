from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.completion_status_t import CompletionStatus
from xknxmono.models.files.v10.device_instance_ref_t import DeviceInstanceRef
from xknxmono.models.files.v10.space_type_t import SpaceType

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class BuildingPart:
    class Meta:
        name = "BuildingPart_t"

    building_part: list[BuildingPart] = field(
        default_factory=list,
        metadata={
            "name": "BuildingPart",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
        },
    )
    device_instance_ref: list[DeviceInstanceRef] = field(
        default_factory=list,
        metadata={
            "name": "DeviceInstanceRef",
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
    type_value: SpaceType = field(
        metadata={
            "name": "Type",
            "type": "Attribute",
        }
    )
    number: None | str = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    comment: None | str = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Attribute",
        },
    )
    completion_status: CompletionStatus = field(
        default=CompletionStatus.UNDEFINED,
        metadata={
            "name": "CompletionStatus",
            "type": "Attribute",
        },
    )
    default_line: None | str = field(
        default=None,
        metadata={
            "name": "DefaultLine",
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
