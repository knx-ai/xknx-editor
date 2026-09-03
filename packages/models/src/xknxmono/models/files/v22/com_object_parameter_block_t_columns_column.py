from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.text_alignment_t import TextAlignment

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ComObjectParameterBlockColumnsColumn:
    class Meta:
        global_type = False

    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    text: None | str = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Attribute",
            "max_length": 255,
        },
    )
    text_parameter_ref_id: None | str = field(
        default=None,
        metadata={
            "name": "TextParameterRefId",
            "type": "Attribute",
        },
    )
    width: str = field(
        metadata={
            "name": "Width",
            "type": "Attribute",
            "pattern": r"(100|\d\d|\d)%",
        }
    )
    text_alignment: None | TextAlignment = field(
        default=None,
        metadata={
            "name": "TextAlignment",
            "type": "Attribute",
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
