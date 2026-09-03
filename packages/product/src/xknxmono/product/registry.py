"""`Registry` — the queryable index over a loaded .knxprod.

Everything is keyed by id (as in KNX itself): flat object stores (`id → object`) plus relationship
edges (`parent id → [child ids]`). Nothing is mutated or pre-linked onto the objects; helpers
resolve refs on demand against the stores and return `id → object` dicts (never lists to scan).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .application import Application
from .catalog import CatalogItem, CatalogSection
from .hardware import DeviceProgram, Hardware, Product
from .master import MasterData


@dataclass(slots=True)
class Registry:
    master: MasterData

    # id → object
    hardware: dict[str, Hardware] = field(default_factory=dict[str, Hardware])
    products: dict[str, Product] = field(default_factory=dict[str, Product])
    programs: dict[str, DeviceProgram] = field(default_factory=dict[str, DeviceProgram])
    applications: dict[str, Application] = field(default_factory=dict[str, Application])
    catalog_sections: dict[str, CatalogSection] = field(
        default_factory=dict[str, CatalogSection]
    )
    catalog_items: dict[str, CatalogItem] = field(
        default_factory=dict[str, CatalogItem]
    )

    # relationship edges: parent id → [child ids]
    manufacturer_to_hardware: dict[str, list[str]] = field(
        default_factory=dict[str, list[str]]
    )
    manufacturer_to_section: dict[str, list[str]] = field(
        default_factory=dict[str, list[str]]
    )
    hardware_to_product: dict[str, list[str]] = field(
        default_factory=dict[str, list[str]]
    )
    hardware_to_program: dict[str, list[str]] = field(
        default_factory=dict[str, list[str]]
    )
    program_to_application: dict[str, list[str]] = field(
        default_factory=dict[str, list[str]]
    )
    section_to_subsection: dict[str, list[str]] = field(
        default_factory=dict[str, list[str]]
    )
    section_to_item: dict[str, list[str]] = field(default_factory=dict[str, list[str]])

    def update_master(self, master: MasterData) -> None:
        """Replace the global master data independently of the rest of the registry."""
        self.master = master

    # --- ergonomic resolvers (all return id → object) ------------------------
    def hardware_for_manufacturer(self, manufacturer_id: str) -> dict[str, Hardware]:
        return {
            h: self.hardware[h]
            for h in self.manufacturer_to_hardware.get(manufacturer_id, [])
        }

    def products_for_hardware(self, hardware_id: str) -> dict[str, Product]:
        return {
            p: self.products[p] for p in self.hardware_to_product.get(hardware_id, [])
        }

    def programs_for_hardware(self, hardware_id: str) -> dict[str, DeviceProgram]:
        return {
            p: self.programs[p] for p in self.hardware_to_program.get(hardware_id, [])
        }

    def applications_for_program(self, program_id: str) -> dict[str, Application]:
        return {
            a: self.applications[a]
            for a in self.program_to_application.get(program_id, [])
            if a in self.applications
        }

    def applications_for_hardware(self, hardware_id: str) -> dict[str, Application]:
        out: dict[str, Application] = {}
        for program_id in self.hardware_to_program.get(hardware_id, []):
            out.update(self.applications_for_program(program_id))
        return out

    def product_for_item(self, item: CatalogItem) -> Product | None:
        return self.products.get(item.product_ref_id or "")

    def program_for_item(self, item: CatalogItem) -> DeviceProgram | None:
        return self.programs.get(item.hardware2_program_ref_id or "")

    def sections_for_manufacturer(
        self, manufacturer_id: str
    ) -> dict[str, CatalogSection]:
        return {
            s: self.catalog_sections[s]
            for s in self.manufacturer_to_section.get(manufacturer_id, [])
        }

    def subsections(self, section_id: str) -> dict[str, CatalogSection]:
        return {
            s: self.catalog_sections[s]
            for s in self.section_to_subsection.get(section_id, [])
        }

    def items_for_section(self, section_id: str) -> dict[str, CatalogItem]:
        return {
            i: self.catalog_items[i] for i in self.section_to_item.get(section_id, [])
        }
