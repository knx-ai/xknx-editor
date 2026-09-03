from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.datapoint_type_t_datapoint_subtypes import (
    DatapointTypeDatapointSubtypes,
)

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class DatapointType:
    class Meta:
        name = "DatapointType_t"

    datapoint_subtypes: None | DatapointTypeDatapointSubtypes = field(
        default=None,
        metadata={
            "name": "DatapointSubtypes",
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
    number: int = field(
        metadata={
            "name": "Number",
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
    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    size_in_bit: int = field(
        metadata={
            "name": "SizeInBit",
            "type": "Attribute",
        }
    )
