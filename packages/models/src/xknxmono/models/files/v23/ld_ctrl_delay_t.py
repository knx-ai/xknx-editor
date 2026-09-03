from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/23"


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
