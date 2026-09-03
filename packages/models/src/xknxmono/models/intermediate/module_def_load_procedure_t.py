from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.ld_ctrl_declare_prop_desc_t import (
    LdCtrlDeclarePropDesc,
)
from xknxmono.models.intermediate.ld_ctrl_delay_t import LdCtrlDelay
from xknxmono.models.intermediate.ld_ctrl_merge_t import LdCtrlMerge
from xknxmono.models.intermediate.ld_ctrl_progress_text_t import LdCtrlProgressText
from xknxmono.models.intermediate.module_def_ld_ctrl_base_choose_t import (
    ModuleDefLdCtrlBaseChoose,
)
from xknxmono.models.intermediate.module_def_ld_ctrl_compare_prop_t import (
    ModuleDefLdCtrlCompareProp,
)
from xknxmono.models.intermediate.module_def_ld_ctrl_invoke_function_prop_t import (
    ModuleDefLdCtrlInvokeFunctionProp,
)
from xknxmono.models.intermediate.module_def_ld_ctrl_read_function_prop_t import (
    ModuleDefLdCtrlReadFunctionProp,
)
from xknxmono.models.intermediate.module_def_ld_ctrl_write_prop_t import (
    ModuleDefLdCtrlWriteProp,
)


@dataclass(slots=True, kw_only=True)
class ModuleDefLoadProcedure:
    """
    :ivar choice:
    :ivar merge_id: registration-relevant
    """

    class Meta:
        name = "ModuleDefLoadProcedure_t"

    choice: list[
        ModuleDefLdCtrlWriteProp
        | ModuleDefLdCtrlCompareProp
        | ModuleDefLdCtrlInvokeFunctionProp
        | ModuleDefLdCtrlReadFunctionProp
        | LdCtrlDelay
        | LdCtrlProgressText
        | LdCtrlDeclarePropDesc
        | LdCtrlMerge
        | ModuleDefLdCtrlBaseChoose
    ] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "LdCtrlWriteProp",
                    "type": ModuleDefLdCtrlWriteProp,
                },
                {
                    "name": "LdCtrlCompareProp",
                    "type": ModuleDefLdCtrlCompareProp,
                },
                {
                    "name": "LdCtrlInvokeFunctionProp",
                    "type": ModuleDefLdCtrlInvokeFunctionProp,
                },
                {
                    "name": "LdCtrlReadFunctionProp",
                    "type": ModuleDefLdCtrlReadFunctionProp,
                },
                {
                    "name": "LdCtrlDelay",
                    "type": LdCtrlDelay,
                },
                {
                    "name": "LdCtrlProgressText",
                    "type": LdCtrlProgressText,
                },
                {
                    "name": "LdCtrlDeclarePropDesc",
                    "type": LdCtrlDeclarePropDesc,
                },
                {
                    "name": "LdCtrlMerge",
                    "type": LdCtrlMerge,
                },
                {
                    "name": "choose",
                    "type": ModuleDefLdCtrlBaseChoose,
                },
            ),
        },
    )
    merge_id: int = field(
        metadata={
            "name": "MergeId",
            "type": "Attribute",
        }
    )
