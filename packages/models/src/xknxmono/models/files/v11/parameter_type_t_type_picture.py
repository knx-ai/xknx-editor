from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.horizontal_alignment_t import HorizontalAlignment

__NAMESPACE__ = "http://knx.org/xml/project/11"


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
    horizontal_alignment: None | HorizontalAlignment = field(
        default=None,
        metadata={
            "name": "HorizontalAlignment",
            "type": "Attribute",
        },
    )
