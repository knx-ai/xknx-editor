from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class DeviceInstanceBinaryDataBinaryData:
    class Meta:
        global_type = False

    data: None | bytes = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
            "format": "base64",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
        },
    )
    ref_id: None | str = field(
        default=None,
        metadata={
            "name": "RefId",
            "type": "Attribute",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 50,
        },
    )
