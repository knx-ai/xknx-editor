from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.ld_ctrl_base_t import LdCtrlBase

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class LdCtrlCompareBase(LdCtrlBase):
    """
    :ivar allow_cached_value: registration-relevant
    :ivar inline_data: registration-relevant
    :ivar mask: registration-relevant
    :ivar range: registration-relevant
    :ivar invert: registration-relevant
    :ivar retry_interval: registration-relevant
    :ivar time_out: registration-relevant
    """

    class Meta:
        name = "LdCtrlCompareBase_t"

    allow_cached_value: bool = field(
        default=False,
        metadata={
            "name": "AllowCachedValue",
            "type": "Attribute",
        },
    )
    inline_data: None | bytes = field(
        default=None,
        metadata={
            "name": "InlineData",
            "type": "Attribute",
            "format": "base16",
        },
    )
    mask: None | bytes = field(
        default=None,
        metadata={
            "name": "Mask",
            "type": "Attribute",
            "format": "base16",
        },
    )
    range: None | str = field(
        default=None,
        metadata={
            "name": "Range",
            "type": "Attribute",
            "pattern": r"[\[\(](-?\d+)?,(-?\d+)?[\)\]][su]?",
        },
    )
    invert: bool = field(
        default=False,
        metadata={
            "name": "Invert",
            "type": "Attribute",
        },
    )
    retry_interval: int = field(
        default=0,
        metadata={
            "name": "RetryInterval",
            "type": "Attribute",
        },
    )
    time_out: int = field(
        default=0,
        metadata={
            "name": "TimeOut",
            "type": "Attribute",
        },
    )
