from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class LdCtrlCompareRelMem(LdCtrlBase):
    """
    :ivar obj_idx: registration-relevant
    :ivar offset: registration-relevant
    :ivar size: registration-relevant
    :ivar inline_data: registration-relevant
    """

    class Meta:
        name = "LdCtrlCompareRelMem_t"

    obj_idx: int = field(
        metadata={
            "name": "ObjIdx",
            "type": "Attribute",
        }
    )
    offset: int = field(
        metadata={
            "name": "Offset",
            "type": "Attribute",
        }
    )
    size: int = field(
        metadata={
            "name": "Size",
            "type": "Attribute",
        }
    )
    inline_data: bytes = field(
        metadata={
            "name": "InlineData",
            "type": "Attribute",
            "format": "base16",
        }
    )
