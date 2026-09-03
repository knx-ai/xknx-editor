from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/23"


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
