from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.device_instance_t_binary_data_binary_data import (
    DeviceInstanceBinaryDataBinaryData,
)

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceBinaryData:
    class Meta:
        global_type = False

    binary_data: list[DeviceInstanceBinaryDataBinaryData] = field(
        default_factory=list,
        metadata={
            "name": "BinaryData",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
            "min_occurs": 1,
        },
    )
