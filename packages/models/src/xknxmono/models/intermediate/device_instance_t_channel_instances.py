from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.channel_instance_t import ChannelInstance


@dataclass(slots=True, kw_only=True)
class DeviceInstanceChannelInstances:
    class Meta:
        global_type = False

    channel_instance: list[ChannelInstance] = field(
        default_factory=list,
        metadata={
            "name": "ChannelInstance",
            "type": "Element",
        },
    )
