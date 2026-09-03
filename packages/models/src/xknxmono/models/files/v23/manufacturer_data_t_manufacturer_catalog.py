from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.catalog_section_t import CatalogSection

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerCatalog:
    class Meta:
        global_type = False

    catalog_section: list[CatalogSection] = field(
        default_factory=list,
        metadata={
            "name": "CatalogSection",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
            "min_occurs": 1,
        },
    )
