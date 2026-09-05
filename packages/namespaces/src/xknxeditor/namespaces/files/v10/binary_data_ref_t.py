from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class BinaryDataRef:
    """
    :ivar data: registration-relevant
    :ivar ref_id: registration-relevant
    """

    class Meta:
        name = "BinaryDataRef_t"

    data: None | bytes = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
            "format": "base64",
        },
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
