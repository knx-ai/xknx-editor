"""Load a .knxprod and index the per-file parse results into a `Registry`.

Each file type owns its `parse_*_xml`; the loader reads each XML's bytes once, parses it, and fills
the registry's object stores and relationship maps. Cross-file references are recorded as edges
(`program_to_application`), never baked into the objects — resolution is via the registry.
"""

from __future__ import annotations

from pathlib import Path

from .application import parse_application_xml
from .archive import Archive
from .catalog import parse_catalog_xml
from .hardware import parse_hardware_xml
from .master import parse_master_xml
from .registry import Registry


def load(source: str | bytes | Path) -> Registry:
    """Load a .knxprod (path or bytes) into a single queryable `Registry` (ids globally unique)."""
    with Archive(source) as archive:
        registry = Registry(master=parse_master_xml(archive.get_master_xml()))

        for manufacturer_id in sorted(archive.manufacturer_ids):
            doc = parse_hardware_xml(archive.get_hardware_xml(manufacturer_id))
            registry.hardware.update(doc.hardware)
            registry.products.update(doc.products)
            registry.programs.update(doc.programs)
            registry.hardware_to_product.update(doc.hardware_to_product)
            registry.hardware_to_program.update(doc.hardware_to_program)
            registry.manufacturer_to_hardware[manufacturer_id] = list(doc.hardware)

            for app_xml in archive.get_application_xmls(manufacturer_id).values():
                for application in parse_application_xml(app_xml, manufacturer_id):
                    registry.applications[application.id] = application

            cat = parse_catalog_xml(archive.get_catalog_xml(manufacturer_id))
            registry.catalog_sections.update(cat.sections)
            registry.catalog_items.update(cat.items)
            registry.section_to_subsection.update(cat.section_to_subsection)
            registry.section_to_item.update(cat.section_to_item)
            registry.manufacturer_to_section[manufacturer_id] = list(cat.sections)

        # Record program → application edges once every application is indexed.
        for program_id, program in registry.programs.items():
            app_ids = [
                a for a in program.application_ref_ids if a in registry.applications
            ]
            if app_ids:
                registry.program_to_application[program_id] = app_ids

    return registry
