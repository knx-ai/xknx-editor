from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v13.master_data_t_manufacturers_manufacturer_import_restriction import (
    MasterDataManufacturersManufacturerImportRestriction,
)
from xknxmono.models.files.v13.master_data_t_manufacturers_manufacturer_public_keys import (
    MasterDataManufacturersManufacturerPublicKeys,
)

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturer:
    class Meta:
        global_type = False

    order_number_formatting_script: None | str = field(
        default=None,
        metadata={
            "name": "OrderNumberFormattingScript",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        },
    )
    public_keys: None | MasterDataManufacturersManufacturerPublicKeys = field(
        default=None,
        metadata={
            "name": "PublicKeys",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    knx_manufacturer_id: int = field(
        metadata={
            "name": "KnxManufacturerId",
            "type": "Attribute",
        }
    )
    default_language: None | str = field(
        default=None,
        metadata={
            "name": "DefaultLanguage",
            "type": "Attribute",
        },
    )
    compatibility_group: None | int = field(
        default=None,
        metadata={
            "name": "CompatibilityGroup",
            "type": "Attribute",
        },
    )
    import_restriction: MasterDataManufacturersManufacturerImportRestriction = field(
        default=MasterDataManufacturersManufacturerImportRestriction.OWN,
        metadata={
            "name": "ImportRestriction",
            "type": "Attribute",
        },
    )
    import_group: list[str] = field(
        default_factory=list,
        metadata={
            "name": "ImportGroup",
            "type": "Attribute",
            "tokens": True,
        },
    )
