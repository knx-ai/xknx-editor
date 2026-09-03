from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class LdCtrlProgressText(LdCtrlBase):
    class Meta:
        name = "LdCtrlProgressText_t"

    text_id: None | int = field(
        default=None,
        metadata={
            "name": "TextId",
            "type": "Attribute",
        },
    )
    message_ref: None | str = field(
        default=None,
        metadata={
            "name": "MessageRef",
            "type": "Attribute",
        },
    )
