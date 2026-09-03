from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.addin_data_t import AddinData

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class ProjectAddinData:
    class Meta:
        global_type = False

    addin_data: list[AddinData] = field(
        default_factory=list,
        metadata={
            "name": "AddinData",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        },
    )
