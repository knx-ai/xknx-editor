from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class CalculationParameterRef:
    """
    :ivar ref_id: registration-relevant
    :ivar alias_name: registration-relevant
    :ivar internal_description:
    """

    class Meta:
        name = "CalculationParameterRef_t"

    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    alias_name: None | str = field(
        default=None,
        metadata={
            "name": "AliasName",
            "type": "Attribute",
            "max_length": 50,
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
