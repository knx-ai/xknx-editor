from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.completion_status_t import CompletionStatus
from xknxmono.models.files.v10.device_instance_ref_t import DeviceInstanceRef

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class Trade:
    class Meta:
        name = "Trade_t"

    trade: list[Trade] = field(
        default_factory=list,
        metadata={
            "name": "Trade",
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
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        },
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
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
    description: None | str = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Attribute",
        },
    )
