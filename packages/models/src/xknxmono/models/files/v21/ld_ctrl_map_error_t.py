from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class LdCtrlMapError(LdCtrlBase):
    """
    :ivar ld_ctrl_filter: registration-relevant
    :ivar original_error: registration-relevant
    :ivar mapped_error: registration-relevant
    """

    class Meta:
        name = "LdCtrlMapError_t"

    ld_ctrl_filter: int = field(
        default=0,
        metadata={
            "name": "LdCtrlFilter",
            "type": "Attribute",
        },
    )
    original_error: int = field(
        metadata={
            "name": "OriginalError",
            "type": "Attribute",
        }
    )
    mapped_error: int = field(
        metadata={
            "name": "MappedError",
            "type": "Attribute",
        }
    )
