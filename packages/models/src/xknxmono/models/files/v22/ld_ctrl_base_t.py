from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v22.ld_ctrl_base_t_on_error import LdCtrlBaseOnError
from xknxmono.models.files.v22.ld_ctrl_proc_type_t import LdCtrlProcType

__NAMESPACE__ = "http://knx.org/xml/project/22"


@dataclass(slots=True, kw_only=True)
class LdCtrlBase:
    """
    :ivar on_error: registration-relevant set
    :ivar applies_to: registration-relevant
    :ivar internal_description:
    """

    class Meta:
        name = "LdCtrlBase_t"

    on_error: list[LdCtrlBaseOnError] = field(
        default_factory=list,
        metadata={
            "name": "OnError",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/22",
        },
    )
    applies_to: LdCtrlProcType = field(
        default=LdCtrlProcType.AUTO,
        metadata={
            "name": "AppliesTo",
            "type": "Attribute",
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
