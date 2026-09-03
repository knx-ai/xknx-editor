from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v20.horizontal_alignment_t import HorizontalAlignment

__NAMESPACE__ = "http://knx.org/xml/project/20"


@dataclass(slots=True, kw_only=True)
class ParameterTypeTypePicture:
    class Meta:
        global_type = False

    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
    horizontal_alignment: HorizontalAlignment = field(
        default=HorizontalAlignment.LEFT,
        metadata={
            "name": "HorizontalAlignment",
            "type": "Attribute",
        },
    )
