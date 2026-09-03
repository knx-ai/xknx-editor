from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypeText:
    """
    :ivar size_in_bit: registration-relevant
    :ivar pattern:
    """

    class Meta:
        global_type = False

    size_in_bit: int = field(
        metadata={
            "name": "SizeInBit",
            "type": "Attribute",
            "min_inclusive": 8,
            "max_inclusive": 1048575,
        }
    )
    pattern: None | str = field(
        default=None,
        metadata={
            "name": "Pattern",
            "type": "Attribute",
        },
    )
