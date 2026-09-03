from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormat,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypesDatapointSubtype:
    class Meta:
        global_type = False

    format: None | DatapointTypeDatapointSubtypesDatapointSubtypeFormat = field(
        default=None,
        metadata={
            "name": "Format",
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
    default: bool = field(
        default=False,
        metadata={
            "name": "Default",
            "type": "Attribute",
        },
    )
    pdt: None | str = field(
        default=None,
        metadata={
            "name": "PDT",
            "type": "Attribute",
        },
    )
