from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class LdCtrlLoadImageProp(LdCtrlBase):
    """
    :ivar obj_idx: registration-relevant
    :ivar obj_type: registration-relevant
    :ivar occurrence: registration-relevant
    :ivar prop_id: registration-relevant
    :ivar count: registration-relevant
    :ivar start_element: registration-relevant
    """

    class Meta:
        name = "LdCtrlLoadImageProp_t"

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
    count: int = field(
        default=1,
        metadata={
            "name": "Count",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 4095,
        },
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
