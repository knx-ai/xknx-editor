from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.ld_ctrl_compare_base_t import LdCtrlCompareBase


@dataclass(slots=True, kw_only=True)
class LdCtrlCompareRelMem(LdCtrlCompareBase):
    """
    :ivar obj_idx: registration-relevant
    :ivar offset: registration-relevant
    :ivar size: registration-relevant
    :ivar inline_data: registration-relevant
    :ivar obj_type: registration-relevant
    :ivar occurrence: registration-relevant
    """

    class Meta:
        name = "LdCtrlCompareRelMem_t"

    obj_idx: None | int = field(
        default=None,
        metadata={
            "name": "ObjIdx",
            "type": "Attribute",
        },
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
