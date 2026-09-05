from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticAssociationTable:
    """
    :ivar code_segment: registration-relevant
    :ivar offset: registration-relevant
    :ivar max_entries: registration-relevant
    """

    class Meta:
        global_type = False

    code_segment: None | str = field(
        default=None,
        metadata={
            "name": "CodeSegment",
            "type": "Attribute",
        },
    )
    offset: None | int = field(
        default=None,
        metadata={
            "name": "Offset",
            "type": "Attribute",
            "max_inclusive": 1048575,
        },
    )
    max_entries: int = field(
        metadata={
            "name": "MaxEntries",
            "type": "Attribute",
        }
    )
