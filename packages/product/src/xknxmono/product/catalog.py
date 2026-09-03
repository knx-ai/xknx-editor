"""Catalog browse tree. `parse_catalog_xml` builds the section hierarchy and the flat items
(holding only product / hardware2program ref-ids); resolution + traversal happen via the Registry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from xknxmono.models import detect_version

from .data import to_ir

if TYPE_CHECKING:
    from xknxmono.models import intermediate as ir


@dataclass(frozen=True, slots=True)
class CatalogSection:
    """A node in the catalog browse tree (`parent_id` is None for a top-level section)."""

    id: str
    name: str | None
    number: str | None
    parent_id: str | None


@dataclass(frozen=True, slots=True)
class CatalogItem:
    """A browse/selection entry: an orderable product running a specific hardware+program binding,
    referenced by id (resolve via the Registry)."""

    id: str
    name: str | None
    number: int | None
    product_ref_id: str | None
    hardware2_program_ref_id: str | None


@dataclass(frozen=True, slots=True)
class CatalogDoc:
    """The result of parsing one Catalog XML: section/item stores plus id-list edges."""

    sections: dict[str, CatalogSection]
    items: dict[str, CatalogItem]
    section_to_subsection: dict[str, list[str]]
    section_to_item: dict[str, list[str]]


def parse_catalog_xml(xml_bytes: bytes) -> CatalogDoc:
    knx = to_ir(xml_bytes, detect_version(xml_bytes))
    sections: dict[str, CatalogSection] = {}
    items: dict[str, CatalogItem] = {}
    section_to_subsection: dict[str, list[str]] = {}
    section_to_item: dict[str, list[str]] = {}

    def walk(section: ir.CatalogSection, parent_id: str | None) -> None:
        sections[section.id] = CatalogSection(
            id=section.id,
            name=section.name,
            number=section.number,
            parent_id=parent_id,
        )
        section_to_subsection[section.id] = [s.id for s in section.catalog_section]
        section_to_item[section.id] = [item.id for item in section.catalog_item]
        for item in section.catalog_item:
            items[item.id] = CatalogItem(
                id=item.id,
                name=item.name,
                number=item.number,
                product_ref_id=item.product_ref_id,
                hardware2_program_ref_id=item.hardware2_program_ref_id,
            )
        for sub in section.catalog_section:
            walk(sub, section.id)

    if knx.manufacturer_data is not None:
        for manufacturer in knx.manufacturer_data.manufacturer:
            if manufacturer.catalog is not None:
                for section in manufacturer.catalog.catalog_section:
                    walk(section, None)

    return CatalogDoc(
        sections=sections,
        items=items,
        section_to_subsection=section_to_subsection,
        section_to_item=section_to_item,
    )
