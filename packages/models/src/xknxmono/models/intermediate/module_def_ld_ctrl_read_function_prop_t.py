from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.ld_ctrl_read_function_prop_t import (
    LdCtrlReadFunctionProp,
)


@dataclass(slots=True, kw_only=True)
class ModuleDefLdCtrlReadFunctionProp(LdCtrlReadFunctionProp):
    """
    :ivar base_obj_idx: registration-relevant
    :ivar base_occurrence: registration-relevant
    """

    class Meta:
        name = "ModuleDefLdCtrlReadFunctionProp_t"

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
