from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.addin_data_t import AddinData

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ProjectAddInData:
    class Meta:
        global_type = False

    add_in_data: list[AddinData] = field(
        default_factory=list,
        metadata={
            "name": "AddInData",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
        },
    )
