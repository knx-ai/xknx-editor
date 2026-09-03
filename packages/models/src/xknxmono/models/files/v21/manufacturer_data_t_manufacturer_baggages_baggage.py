from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.manufacturer_data_t_manufacturer_baggages_baggage_file_info import (
    ManufacturerDataManufacturerBaggagesBaggageFileInfo,
)

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerBaggagesBaggage:
    class Meta:
        global_type = False

    file_info: ManufacturerDataManufacturerBaggagesBaggageFileInfo = field(
        metadata={
            "name": "FileInfo",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
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
