from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.catalog_section_t import CatalogSection

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerCatalog:
    class Meta:
        global_type = False

    catalog_section: list[CatalogSection] = field(
        default_factory=list,
        metadata={
            "name": "CatalogSection",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/11",
            "min_occurs": 1,
        },
    )
