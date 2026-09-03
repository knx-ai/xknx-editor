from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.catalog_section_t_catalog_item import (
    CatalogSectionCatalogItem,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class CatalogSection:
    class Meta:
        name = "CatalogSection_t"

    catalog_section: list[CatalogSection] = field(
        default_factory=list,
        metadata={
            "name": "CatalogSection",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
        },
    )
    catalog_item: list[CatalogSectionCatalogItem] = field(
        default_factory=list,
        metadata={
            "name": "CatalogItem",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/23",
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
    number: str = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
            "max_length": 20,
        }
    )
    visible_description: None | str = field(
        default=None,
        metadata={
            "name": "VisibleDescription",
            "type": "Attribute",
        },
    )
    default_language: None | str = field(
        default=None,
        metadata={
            "name": "DefaultLanguage",
            "type": "Attribute",
        },
    )
    non_reg_relevant_data_version: int = field(
        default=0,
        metadata={
            "name": "NonRegRelevantDataVersion",
            "type": "Attribute",
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
