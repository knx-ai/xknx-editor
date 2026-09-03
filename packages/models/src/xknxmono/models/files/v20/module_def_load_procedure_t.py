from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.ld_ctrl_declare_prop_desc_t import LdCtrlDeclarePropDesc
from xknxmono.models.files.v20.ld_ctrl_delay_t import LdCtrlDelay
from xknxmono.models.files.v20.ld_ctrl_merge_t import LdCtrlMerge
from xknxmono.models.files.v20.ld_ctrl_progress_text_t import LdCtrlProgressText
from xknxmono.models.files.v20.module_def_ld_ctrl_base_choose_t import (
    ModuleDefLdCtrlBaseChoose,
)
from xknxmono.models.files.v20.module_def_ld_ctrl_compare_prop_t import (
    ModuleDefLdCtrlCompareProp,
)
from xknxmono.models.files.v20.module_def_ld_ctrl_invoke_function_prop_t import (
    ModuleDefLdCtrlInvokeFunctionProp,
)
from xknxmono.models.files.v20.module_def_ld_ctrl_read_function_prop_t import (
    ModuleDefLdCtrlReadFunctionProp,
)
from xknxmono.models.files.v20.module_def_ld_ctrl_write_prop_t import (
    ModuleDefLdCtrlWriteProp,
)

__NAMESPACE__ = "http://knx.org/xml/project/20"


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
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "LdCtrlCompareProp",
                    "type": ModuleDefLdCtrlCompareProp,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "LdCtrlInvokeFunctionProp",
                    "type": ModuleDefLdCtrlInvokeFunctionProp,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "LdCtrlReadFunctionProp",
                    "type": ModuleDefLdCtrlReadFunctionProp,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "LdCtrlDelay",
                    "type": LdCtrlDelay,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "LdCtrlProgressText",
                    "type": LdCtrlProgressText,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "LdCtrlDeclarePropDesc",
                    "type": LdCtrlDeclarePropDesc,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "LdCtrlMerge",
                    "type": LdCtrlMerge,
                    "namespace": "http://knx.org/xml/project/20",
                },
                {
                    "name": "choose",
                    "type": ModuleDefLdCtrlBaseChoose,
                    "namespace": "http://knx.org/xml/project/20",
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
