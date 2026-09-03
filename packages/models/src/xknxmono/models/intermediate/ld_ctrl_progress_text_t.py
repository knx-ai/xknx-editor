from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.ld_ctrl_base_t import LdCtrlBase


@dataclass(slots=True, kw_only=True)
class LdCtrlProgressText(LdCtrlBase):
    """
    :ivar text_id: registration-relevant
    :ivar message_ref:
    """

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
