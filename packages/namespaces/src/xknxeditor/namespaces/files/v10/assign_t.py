from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class Assign:
    """
    :ivar target_param_ref_ref: registration-relevant
    :ivar source_param_ref_ref: registration-relevant
    :ivar value: registration-relevant
    """

    class Meta:
        name = "Assign_t"

    target_param_ref_ref: str = field(
        metadata={
            "name": "TargetParamRefRef",
            "type": "Attribute",
        }
    )
    source_param_ref_ref: None | str = field(
        default=None,
        metadata={
            "name": "SourceParamRefRef",
            "type": "Attribute",
        },
    )
    value: None | str = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
        },
    )
