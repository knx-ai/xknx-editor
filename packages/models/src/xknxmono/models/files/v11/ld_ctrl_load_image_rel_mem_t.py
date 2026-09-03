from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class LdCtrlLoadImageRelMem(LdCtrlBase):
    """
    :ivar obj_idx: registration-relevant
    :ivar offset: registration-relevant
    :ivar size: registration-relevant
    """

    class Meta:
        name = "LdCtrlLoadImageRelMem_t"

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
