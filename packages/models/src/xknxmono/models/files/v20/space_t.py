from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.completion_status_t import CompletionStatus
from xknxmono.models.files.v20.device_instance_ref_t import DeviceInstanceRef
from xknxmono.models.files.v20.function_t import Function
from xknxmono.models.files.v20.space_type_t import SpaceType

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class Space:
    class Meta:
        name = "Space_t"

    space: list[Space] = field(
        default_factory=list,
        metadata={
            "name": "Space",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    device_instance_ref: list[DeviceInstanceRef] = field(
        default_factory=list,
        metadata={
            "name": "DeviceInstanceRef",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/20",
        },
    )
    function: list[Function] = field(
        default_factory=list,
        metadata={
            "name": "Function",
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
    type_value: SpaceType = field(
        metadata={
            "name": "Type",
            "type": "Attribute",
        }
    )
    usage: None | str = field(
        default=None,
        metadata={
            "name": "Usage",
            "type": "Attribute",
        },
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
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
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
    puid: int = field(
        metadata={
            "name": "Puid",
            "type": "Attribute",
        }
    )
    context: None | str = field(
        default=None,
        metadata={
            "name": "Context",
            "type": "Attribute",
        },
    )
