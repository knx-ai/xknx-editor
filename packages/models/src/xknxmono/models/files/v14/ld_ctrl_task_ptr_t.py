from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class LdCtrlTaskPtr(LdCtrlBase):
    """
    :ivar lsm_idx: registration-relevant
    :ivar obj_type: registration-relevant
    :ivar occurrence: registration-relevant
    :ivar init_ptr: registration-relevant
    :ivar save_ptr: registration-relevant
    :ivar serial_ptr: registration-relevant
    """

    class Meta:
        name = "LdCtrlTaskPtr_t"

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
    init_ptr: int = field(
        metadata={
            "name": "InitPtr",
            "type": "Attribute",
        }
    )
    save_ptr: int = field(
        metadata={
            "name": "SavePtr",
            "type": "Attribute",
        }
    )
    serial_ptr: int = field(
        metadata={
            "name": "SerialPtr",
            "type": "Attribute",
        }
    )
