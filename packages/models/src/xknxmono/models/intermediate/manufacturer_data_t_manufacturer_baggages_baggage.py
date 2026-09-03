from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.manufacturer_data_t_manufacturer_baggages_baggage_file_info import (
    ManufacturerDataManufacturerBaggagesBaggageFileInfo,
)


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerBaggagesBaggage:
    class Meta:
        global_type = False

    file_info: ManufacturerDataManufacturerBaggagesBaggageFileInfo = field(
        metadata={
            "name": "FileInfo",
            "type": "Element",
        }
    )
    data: None | bytes = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "format": "base64",
        },
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
    install_on_import: bool = field(
        default=True,
        metadata={
            "name": "InstallOnImport",
            "type": "Attribute",
        },
    )
    group_addresses16_bit_enabled: bool = field(
        default=True,
        metadata={
            "name": "GroupAddresses16BitEnabled",
            "type": "Attribute",
        },
    )
