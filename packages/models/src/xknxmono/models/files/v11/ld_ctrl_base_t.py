from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.ld_ctrl_proc_type_t import LdCtrlProcType

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class LdCtrlBase:
    """
    :ivar applies_to: registration-relevant
    """

    class Meta:
        name = "LdCtrlBase_t"

    applies_to: LdCtrlProcType = field(
        default=LdCtrlProcType.AUTO,
        metadata={
            "name": "AppliesTo",
            "type": "Attribute",
        },
    )
