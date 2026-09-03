from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.text_encoding_t import TextEncoding

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class DatapointTypeDatapointSubtypesDatapointSubtypeFormatString:
    class Meta:
        global_type = False

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    width: int = field(
        metadata={
            "name": "Width",
            "type": "Attribute",
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
        },
    )
    unit: None | str = field(
        default=None,
        metadata={
            "name": "Unit",
            "type": "Attribute",
        },
    )
    encoding: None | TextEncoding = field(
        default=None,
        metadata={
            "name": "Encoding",
            "type": "Attribute",
        },
    )
    variable_length: bool = field(
        default=False,
        metadata={
            "name": "VariableLength",
            "type": "Attribute",
        },
    )
    null_terminated: bool = field(
        default=False,
        metadata={
            "name": "NullTerminated",
            "type": "Attribute",
        },
    )
