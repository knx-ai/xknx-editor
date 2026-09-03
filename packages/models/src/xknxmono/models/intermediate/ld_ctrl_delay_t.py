from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.ld_ctrl_base_t import LdCtrlBase


@dataclass(slots=True, kw_only=True)
class LdCtrlDelay(LdCtrlBase):
    """
    :ivar milli_seconds: registration-relevant
    """

    class Meta:
        name = "LdCtrlDelay_t"

    milli_seconds: int = field(
        metadata={
            "name": "MilliSeconds",
            "type": "Attribute",
        }
    )
