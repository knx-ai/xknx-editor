from __future__ import annotations

from dataclasses import dataclass

from xknxmono.models.files.v23.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class LdCtrlDisconnect(LdCtrlBase):
    class Meta:
        name = "LdCtrlDisconnect_t"
