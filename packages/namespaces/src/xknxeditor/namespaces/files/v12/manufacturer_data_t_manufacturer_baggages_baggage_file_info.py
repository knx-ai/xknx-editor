from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerBaggagesBaggageFileInfo:
    class Meta:
        global_type = False

    version: None | str = field(
        default=None,
        metadata={
            "name": "Version",
            "type": "Attribute",
            "pattern": r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+",
        },
    )
    time_info: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "TimeInfo",
            "type": "Attribute",
        },
    )
    hidden: bool = field(
        default=False,
        metadata={
            "name": "Hidden",
            "type": "Attribute",
        },
    )
    read_only: bool = field(
        default=False,
        metadata={
            "name": "ReadOnly",
            "type": "Attribute",
        },
    )
