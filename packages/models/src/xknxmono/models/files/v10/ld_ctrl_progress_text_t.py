from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class LdCtrlProgressText(LdCtrlBase):
    """
    :ivar text_id: registration-relevant
    """

    class Meta:
        name = "LdCtrlProgressText_t"

    text_id: int = field(
        metadata={
            "name": "TextId",
            "type": "Attribute",
        }
    )
