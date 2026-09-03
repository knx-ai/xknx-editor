from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.ld_ctrl_base_t import LdCtrlBase
from xknxmono.models.files.v13.ld_ctrl_control_variable_t import LdCtrlControlVariable

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class LdCtrlSetControlVariable(LdCtrlBase):
    """
    :ivar name: registration-relevant
    :ivar value: registration-relevant
    """

    class Meta:
        name = "LdCtrlSetControlVariable_t"

    name: LdCtrlControlVariable = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
        }
    )
    value: bool = field(
        metadata={
            "name": "Value",
            "type": "Attribute",
        }
    )
