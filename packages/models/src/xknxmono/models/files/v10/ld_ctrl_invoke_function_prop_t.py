from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class LdCtrlInvokeFunctionProp(LdCtrlBase):
    """
    :ivar obj_idx: registration-relevant
    :ivar obj_type: registration-relevant
    :ivar occurrence: registration-relevant
    :ivar prop_id: registration-relevant
    :ivar inline_data: registration-relevant
    """

    class Meta:
        name = "LdCtrlInvokeFunctionProp_t"

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
    inline_data: None | bytes = field(
        default=None,
        metadata={
            "name": "InlineData",
            "type": "Attribute",
            "format": "base16",
        },
    )
