from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class CalculationParameterRef:
    """
    :ivar ref_id: registration-relevant
    :ivar internal_description:
    :ivar alias_name: registration-relevant
    """

    class Meta:
        name = "CalculationParameterRef_t"

    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
    alias_name: None | str = field(
        default=None,
        metadata={
            "name": "AliasName",
            "type": "Attribute",
            "max_length": 50,
        },
    )
