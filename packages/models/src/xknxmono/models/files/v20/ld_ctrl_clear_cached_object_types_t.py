from __future__ import annotations

from dataclasses import dataclass

from xknxmono.models.files.v20.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class LdCtrlClearCachedObjectTypes(LdCtrlBase):
    class Meta:
        name = "LdCtrlClearCachedObjectTypes_t"
