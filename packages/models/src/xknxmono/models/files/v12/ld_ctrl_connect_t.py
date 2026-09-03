from __future__ import annotations

from dataclasses import dataclass

from xknxmono.models.files.v12.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class LdCtrlConnect(LdCtrlBase):
    class Meta:
        name = "LdCtrlConnect_t"
