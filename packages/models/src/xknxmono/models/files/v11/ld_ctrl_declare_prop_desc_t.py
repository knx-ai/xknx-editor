from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.ld_ctrl_base_t import LdCtrlBase
from xknxmono.models.files.v11.prop_type_t import PropType

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class LdCtrlDeclarePropDesc(LdCtrlBase):
    """
    :ivar obj_idx: registration-relevant
    :ivar obj_type: registration-relevant
    :ivar occurrence: registration-relevant
    :ivar prop_id: registration-relevant
    :ivar prop_type: registration-relevant
    :ivar max_elements: registration-relevant
    :ivar read_access: registration-relevant
    :ivar write_access: registration-relevant
    :ivar writable: registration-relevant
    """

    class Meta:
        name = "LdCtrlDeclarePropDesc_t"

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
    prop_type: PropType = field(
        metadata={
            "name": "PropType",
            "type": "Attribute",
        }
    )
    max_elements: int = field(
        metadata={
            "name": "MaxElements",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )
    read_access: int = field(
        metadata={
            "name": "ReadAccess",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 15,
        }
    )
    write_access: int = field(
        metadata={
            "name": "WriteAccess",
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 15,
        }
    )
    writable: bool = field(
        metadata={
            "name": "Writable",
            "type": "Attribute",
        }
    )
