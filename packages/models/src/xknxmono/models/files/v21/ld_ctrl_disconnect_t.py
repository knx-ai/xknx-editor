from __future__ import annotations

from dataclasses import dataclass

from xknxmono.models.files.v21.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class LdCtrlDisconnect(LdCtrlBase):
    class Meta:
        name = "LdCtrlDisconnect_t"
