from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class LdCtrlMasterReset(LdCtrlBase):
    """
    :ivar erase_code: registration-relevant
    :ivar channel_number: registration-relevant
    """

    class Meta:
        name = "LdCtrlMasterReset_t"

    erase_code: int = field(
        metadata={
            "name": "EraseCode",
            "type": "Attribute",
        }
    )
    channel_number: int = field(
        metadata={
            "name": "ChannelNumber",
            "type": "Attribute",
        }
    )
