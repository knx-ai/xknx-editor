from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.com_object_t import ComObject

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticComObjectTable:
    """
    :ivar com_object: registration-relevant set
    :ivar code_segment: registration-relevant
    :ivar offset: registration-relevant
    """

    class Meta:
        global_type = False

    com_object: list[ComObject] = field(
        default_factory=list,
        metadata={
            "name": "ComObject",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
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
