from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class LdCtrlAbsSegment(LdCtrlBase):
    """
    :ivar lsm_idx: registration-relevant
    :ivar obj_type: registration-relevant
    :ivar occurrence: registration-relevant
    :ivar seg_type: registration-relevant
    :ivar address: registration-relevant
    :ivar size: registration-relevant
    :ivar access: registration-relevant
    :ivar mem_type: registration-relevant
    :ivar seg_flags: registration-relevant
    """

    class Meta:
        name = "LdCtrlAbsSegment_t"

    lsm_idx: None | int = field(
        default=None,
        metadata={
            "name": "LsmIdx",
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
    seg_type: int = field(
        metadata={
            "name": "SegType",
            "type": "Attribute",
        }
    )
    address: int = field(
        metadata={
            "name": "Address",
            "type": "Attribute",
        }
    )
    size: int = field(
        metadata={
            "name": "Size",
            "type": "Attribute",
        }
    )
    access: int = field(
        metadata={
            "name": "Access",
            "type": "Attribute",
        }
    )
    mem_type: int = field(
        metadata={
            "name": "MemType",
            "type": "Attribute",
        }
    )
    seg_flags: int = field(
        metadata={
            "name": "SegFlags",
            "type": "Attribute",
        }
    )
