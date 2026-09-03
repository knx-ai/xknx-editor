from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class LdCtrlWriteProp(LdCtrlBase):
    """
    :ivar obj_idx: registration-relevant
    :ivar obj_type: registration-relevant
    :ivar occurrence: registration-relevant
    :ivar prop_id: registration-relevant
    :ivar start_element: registration-relevant
    :ivar count: registration-relevant
    :ivar verify: registration-relevant
    :ivar inline_data: registration-relevant
    """

    class Meta:
        name = "LdCtrlWriteProp_t"

    obj_idx: None | int = field(
        default=None,
        metadata={
            "name": "ObjIdx",
            "type": "Attribute",
        },
    )
    obj_type: None | int = field(
        default=None,
        metadata={
            "name": "ObjType",
            "type": "Attribute",
        },
    )
    occurrence: int = field(
        default=0,
        metadata={
            "name": "Occurrence",
            "type": "Attribute",
        },
    )
    prop_id: int = field(
        metadata={
            "name": "PropId",
            "type": "Attribute",
        }
    )
    start_element: int = field(
        default=1,
        metadata={
            "name": "StartElement",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 4095,
        },
    )
    count: int = field(
        default=1,
        metadata={
            "name": "Count",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 4095,
        },
    )
    verify: bool = field(
        metadata={
            "name": "Verify",
            "type": "Attribute",
        }
    )
    inline_data: None | bytes = field(
        default=None,
        metadata={
            "name": "InlineData",
            "type": "Attribute",
            "format": "base16",
        },
    )
