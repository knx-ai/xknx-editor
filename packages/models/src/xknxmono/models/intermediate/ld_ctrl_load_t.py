from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.ld_ctrl_base_t import LdCtrlBase


@dataclass(slots=True, kw_only=True)
class LdCtrlLoad(LdCtrlBase):
    """
    :ivar lsm_idx: registration-relevant
    :ivar obj_type: registration-relevant
    :ivar occurrence: registration-relevant
    """

    class Meta:
        name = "LdCtrlLoad_t"

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
