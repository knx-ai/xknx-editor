from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.manufacturer_data_t_manufacturer_baggages_baggage_file_info import (
    ManufacturerDataManufacturerBaggagesBaggageFileInfo,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerBaggagesBaggage:
    class Meta:
        global_type = False

    file_info: ManufacturerDataManufacturerBaggagesBaggageFileInfo = field(
        metadata={
            "name": "FileInfo",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        }
    )
    target_path: str = field(
        metadata={
            "name": "TargetPath",
            "type": "Attribute",
            "max_length": 255,
            "pattern": r'(([^"<>\|:\*\?/\\\t\n\r]+\\)*[^"<>\|:\*\?/\\\t\n\r]+)?',
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
            "pattern": r'[^"<>\|:\*\?/\\\t\n\r]+',
        }
    )
    file_integrity: str = field(
        default="00000000",
        metadata={
            "name": "FileIntegrity",
            "type": "Attribute",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    guid: None | str = field(
        default=None,
        metadata={
            "name": "Guid",
            "type": "Attribute",
            "pattern": r"\{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}\}",
        },
    )
