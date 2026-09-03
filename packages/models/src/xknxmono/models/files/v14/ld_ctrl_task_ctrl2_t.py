from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class LdCtrlTaskCtrl2(LdCtrlBase):
    """
    :ivar lsm_idx: registration-relevant
    :ivar obj_type: registration-relevant
    :ivar occurrence: registration-relevant
    :ivar callback: registration-relevant
    :ivar address: registration-relevant
    :ivar seg0: registration-relevant
    :ivar seg1: registration-relevant
    """

    class Meta:
        name = "LdCtrlTaskCtrl2_t"

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
    callback: int = field(
        metadata={
            "name": "Callback",
            "type": "Attribute",
        }
    )
    address: int = field(
        metadata={
            "name": "Address",
            "type": "Attribute",
        }
    )
    seg0: int = field(
        metadata={
            "name": "Seg0",
            "type": "Attribute",
        }
    )
    seg1: int = field(
        metadata={
            "name": "Seg1",
            "type": "Attribute",
        }
    )
