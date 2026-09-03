from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.channel_instance_t import ChannelInstance

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceChannelInstances:
    class Meta:
        global_type = False

    channel_instance: list[ChannelInstance] = field(
        default_factory=list,
        metadata={
            "name": "ChannelInstance",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
