from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.segment_base_t import SegmentBase

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticCodeRelativeSegment(SegmentBase):
    """
    :ivar load_state_machine: registration-relevant
    :ivar offset: registration-relevant
    """

    class Meta:
        global_type = False

    load_state_machine: int = field(
        metadata={
            "name": "LoadStateMachine",
            "type": "Attribute",
        }
    )
    offset: int = field(
        metadata={
            "name": "Offset",
            "type": "Attribute",
            "max_inclusive": 1048575,
        }
    )
