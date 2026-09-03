from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_application_programs import (
    ManufacturerDataManufacturerApplicationPrograms,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_baggages import (
    ManufacturerDataManufacturerBaggages,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_catalog import (
    ManufacturerDataManufacturerCatalog,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_hardware import (
    ManufacturerDataManufacturerHardware,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_languages import (
    ManufacturerDataManufacturerLanguages,
)

__NAMESPACE__ = "http://knx.org/xml/project/12"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturer:
    class Meta:
        global_type = False

    catalog: None | ManufacturerDataManufacturerCatalog = field(
        default=None,
        metadata={
            "name": "Catalog",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    application_programs: None | ManufacturerDataManufacturerApplicationPrograms = (
        field(
            default=None,
            metadata={
                "name": "ApplicationPrograms",
                "type": "Element",
                "namespace": "http://knx.org/xml/project/12",
            },
        )
    )
    baggages: None | ManufacturerDataManufacturerBaggages = field(
        default=None,
        metadata={
            "name": "Baggages",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    hardware: None | ManufacturerDataManufacturerHardware = field(
        default=None,
        metadata={
            "name": "Hardware",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    languages: None | ManufacturerDataManufacturerLanguages = field(
        default=None,
        metadata={
            "name": "Languages",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/12",
        },
    )
    ref_id: str = field(
        metadata={
            "name": "RefId",
            "type": "Attribute",
        }
    )
