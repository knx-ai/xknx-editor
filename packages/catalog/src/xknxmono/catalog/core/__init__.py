"""Core catalog operations — database queries and ingestion — with no FastAPI dependency.

These functions operate directly on a SQLAlchemy :class:`~sqlalchemy.orm.Session`
and return ORM model instances or plain dataclasses. They can be used from any
Python context (scripts, GUI applications, tests) without starting an HTTP server.

Example::

  from pathlib import Path
  from sqlalchemy.orm import Session
  from xknxmono.catalog.db import make_engine, knxprod_dir_for
  from xknxmono.catalog.core import HardwareFilters, list_hardware, upload_knxprod

  engine = make_engine("sqlite:///catalog.db")
  upload_knxprod(Path("device.knxprod").read_bytes(), knxprod_dir_for(Path("catalog.db")), engine)

  with Session(engine) as db:
      results = list_hardware(db, HardwareFilters(manufacturer_id=["M-0001"], limit=10))
      for hw in results:
          print(hw.name, hw.order_number)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

_LAZY: dict[str, tuple[str, str]] = {
    "ApplicationSummary": (".applications", "ApplicationSummary"),
    "get_application_detail": (".applications", "get_application_detail"),
    "get_application_detail_by_id": (".applications", "get_application_detail_by_id"),
    "get_application_xml": (".applications", "get_application_xml"),
    "list_applications": (".applications", "list_applications"),
    "CatalogSectionNode": (".catalog_sections", "CatalogSectionNode"),
    "build_catalog_tree": (".catalog_sections", "build_catalog_tree"),
    "collect_section_ids": (".catalog_sections", "collect_section_ids"),
    "list_catalog_sections": (".catalog_sections", "list_catalog_sections"),
    "HardwareFilters": (".hardware", "HardwareFilters"),
    "get_hardware": (".hardware", "get_hardware"),
    "get_hardware_program": (".hardware", "get_hardware_program"),
    "list_hardware": (".hardware", "list_hardware"),
    "get_manufacturer": (".manufacturers", "get_manufacturer"),
    "list_manufacturers": (".manufacturers", "list_manufacturers"),
    "ProductSummary": (".products", "ProductSummary"),
    "list_products": (".products", "list_products"),
    "CatalogService": (".service", "CatalogService"),
    "upload_knxprod": (".upload", "upload_knxprod"),
}

__all__ = [
    "ApplicationSummary",
    "CatalogSectionNode",
    "CatalogService",
    "HardwareFilters",
    "ProductSummary",
    "build_catalog_tree",
    "collect_section_ids",
    "get_application_detail",
    "get_application_detail_by_id",
    "get_application_xml",
    "get_hardware",
    "get_hardware_program",
    "get_manufacturer",
    "list_applications",
    "list_catalog_sections",
    "list_hardware",
    "list_manufacturers",
    "list_products",
    "upload_knxprod",
]

if TYPE_CHECKING:
    from .applications import (
        ApplicationSummary,
        get_application_detail,
        get_application_detail_by_id,
        get_application_xml,
        list_applications,
    )
    from .catalog_sections import (
        CatalogSectionNode,
        build_catalog_tree,
        collect_section_ids,
        list_catalog_sections,
    )
    from .hardware import (
        HardwareFilters,
        get_hardware,
        get_hardware_program,
        list_hardware,
    )
    from .manufacturers import get_manufacturer, list_manufacturers
    from .products import ProductSummary, list_products
    from .service import CatalogService
    from .upload import upload_knxprod


def __getattr__(name: str) -> object:
    if name in _LAZY:
        import importlib

        module_path, attr = _LAZY[name]
        mod = importlib.import_module(module_path, __package__)
        value = getattr(mod, attr)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
