from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.ld_ctrl_invoke_function_prop_t import (
    LdCtrlInvokeFunctionProp,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ModuleDefLdCtrlInvokeFunctionProp(LdCtrlInvokeFunctionProp):
    """
    :ivar base_obj_idx: registration-relevant
    :ivar base_occurrence: registration-relevant
    """

    class Meta:
        name = "ModuleDefLdCtrlInvokeFunctionProp_t"

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
