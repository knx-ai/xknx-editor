from __future__ import annotations

from dataclasses import dataclass

from xknxmono.models.intermediate.ld_ctrl_base_t import LdCtrlBase


@dataclass(slots=True, kw_only=True)
class LdCtrlClearCachedObjectTypes(LdCtrlBase):
    class Meta:
        name = "LdCtrlClearCachedObjectTypes_t"
