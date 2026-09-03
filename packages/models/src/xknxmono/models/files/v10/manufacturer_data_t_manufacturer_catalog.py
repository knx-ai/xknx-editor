from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v10.catalog_section_t import CatalogSection

__NAMESPACE__ = "http://knx.org/xml/project/10"


@dataclass(slots=True, kw_only=True)
class ManufacturerDataManufacturerCatalog:
    class Meta:
        global_type = False

    catalog_section: list[CatalogSection] = field(
        default_factory=list,
        metadata={
            "name": "CatalogSection",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/10",
            "min_occurs": 1,
        },
    )
