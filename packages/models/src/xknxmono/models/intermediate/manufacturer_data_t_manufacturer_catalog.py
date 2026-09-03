from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.catalog_section_t import CatalogSection


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerCatalog:
    class Meta:
        global_type = False

    catalog_section: list[CatalogSection] = field(
        default_factory=list,
        metadata={
            "name": "CatalogSection",
            "type": "Element",
            "min_occurs": 1,
        },
    )
