from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class When:
    """
    :ivar test: registration-relevant
    :ivar default: registration-relevant
    """

    class Meta:
        name = "When_t"

    test: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"((-?\d+\s)*-?\d+)|((=|(!=)|>|<|(>=)|(<=))-?\d+)",
        },
    )
    default: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
