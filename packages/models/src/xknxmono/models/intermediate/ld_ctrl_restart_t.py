from __future__ import annotations
from dataclasses import dataclass
from xknxmono.models.intermediate.ld_ctrl_base_t import LdCtrlBase


@dataclass(slots=True, kw_only=True)
class LdCtrlRestart(LdCtrlBase):
    class Meta:
        name = "LdCtrlRestart_t"
