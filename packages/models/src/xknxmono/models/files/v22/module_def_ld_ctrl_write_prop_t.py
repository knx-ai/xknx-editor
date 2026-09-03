from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.ld_ctrl_write_prop_t import LdCtrlWriteProp

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class ModuleDefLdCtrlWriteProp(LdCtrlWriteProp):
    """
    :ivar base_obj_idx: registration-relevant
    :ivar base_occurrence: registration-relevant
    :ivar base_start_element: registration-relevant
    """

    class Meta:
        name = "ModuleDefLdCtrlWriteProp_t"

    base_obj_idx: None | str = field(
        default=None,
        metadata={
            "name": "BaseObjIdx",
            "type": "Attribute",
        },
    )
    base_occurrence: None | str = field(
        default=None,
        metadata={
            "name": "BaseOccurrence",
            "type": "Attribute",
        },
    )
    base_start_element: None | str = field(
        default=None,
        metadata={
            "name": "BaseStartElement",
            "type": "Attribute",
        },
    )
