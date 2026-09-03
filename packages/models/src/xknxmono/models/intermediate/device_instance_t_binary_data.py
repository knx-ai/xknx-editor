from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.device_instance_t_binary_data_binary_data import (
    DeviceInstanceBinaryDataBinaryData,
)


@dataclass(slots=True, kw_only=True)
class DeviceInstanceBinaryData:
    class Meta:
        global_type = False

    binary_data: list[DeviceInstanceBinaryDataBinaryData] = field(
        default_factory=list,
        metadata={
            "name": "BinaryData",
            "type": "Element",
        },
    )
