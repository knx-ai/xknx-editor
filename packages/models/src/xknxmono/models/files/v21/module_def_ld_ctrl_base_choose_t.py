from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.module_def_ld_ctrl_base_choose_t_when import (
    ModuleDefLdCtrlBaseChooseWhen,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ModuleDefLdCtrlBaseChoose:
    """
    :ivar when: registration-relevant list
    :ivar param_ref_id: registration-relevant
    :ivar internal_description:
    """

    class Meta:
        name = "ModuleDefLdCtrlBaseChoose_t"

    when: list[ModuleDefLdCtrlBaseChooseWhen] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
            "min_occurs": 1,
        },
    )
    param_ref_id: str = field(
        metadata={
            "name": "ParamRefId",
            "type": "Attribute",
        }
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
