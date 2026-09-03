from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class LdCtrlMaxLength(LdCtrlBase):
    """
    :ivar lsm_idx: registration-relevant
    :ivar obj_type: registration-relevant
    :ivar occurrence: registration-relevant
    :ivar size: registration-relevant
    """

    class Meta:
        name = "LdCtrlMaxLength_t"

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
    size: int = field(
        metadata={
            "name": "Size",
            "type": "Attribute",
        }
    )
