from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.ld_ctrl_base_t import LdCtrlBase


@dataclass(slots=True, kw_only=True)
class LdCtrlClearLcfilterTable(LdCtrlBase):
    """
    :ivar use_function_prop: registration-relevant
    """

    class Meta:
        name = "LdCtrlClearLCFilterTable_t"

    use_function_prop: bool = field(
        default=False,
        metadata={
            "name": "UseFunctionProp",
            "type": "Attribute",
        },
    )
