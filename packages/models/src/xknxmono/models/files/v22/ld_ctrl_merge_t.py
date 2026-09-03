from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class LdCtrlMerge(LdCtrlBase):
    """
    :ivar merge_id: registration-relevant
    """

    class Meta:
        name = "LdCtrlMerge_t"

    merge_id: int = field(
        metadata={
            "name": "MergeId",
            "type": "Attribute",
        }
    )
