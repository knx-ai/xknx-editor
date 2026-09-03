from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v14.manufacturer_data_t import ManufacturerData
from xknxmono.models.files.v14.master_data_t import MasterData
from xknxmono.models.files.v14.project_t import Project

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class Knx:
    class Meta:
        name = "KNX"
        namespace = "http://knx.org/xml/project/14"

    master_data: None | MasterData = field(
        default=None,
        metadata={
            "name": "MasterData",
            "type": "Element",
        },
    )
    manufacturer_data: None | ManufacturerData = field(
        default=None,
        metadata={
            "name": "ManufacturerData",
            "type": "Element",
        },
    )
    project: list[Project] = field(
        default_factory=list,
        metadata={
            "name": "Project",
            "type": "Element",
        },
    )
    created_by: None | str = field(
        default=None,
        metadata={
            "name": "CreatedBy",
            "type": "Attribute",
        },
    )
    tool_version: None | str = field(
        default=None,
        metadata={
            "name": "ToolVersion",
            "type": "Attribute",
        },
    )
