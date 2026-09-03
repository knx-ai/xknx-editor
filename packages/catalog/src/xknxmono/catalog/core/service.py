"""CatalogService — an instantiable, database-owning facade over the catalog core operations.

Construct one with a database path: it owns the engine (and the matching ``.knxprod`` store) and
exposes every core query/ingest operation as a method, opening a short-lived session per call. It is
the single object the HTTP API and embedding applications (e.g. the GUI) build on, so no caller has
to thread a `Session` or engine around by hand.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from sqlalchemy.orm import Session

from xknxmono.catalog.core.applications import (
    ApplicationSummary,
    get_application_detail,
    get_application_detail_by_id,
    get_application_xml,
    list_applications,
)
from xknxmono.catalog.core.catalog_sections import (
    CatalogSectionNode,
    build_catalog_tree,
    collect_section_ids,
    list_catalog_sections,
)
from xknxmono.catalog.core.hardware import (
    HardwareFilters,
    get_hardware,
    get_hardware_program,
    get_program_source,
    list_hardware,
)
from xknxmono.catalog.core.manufacturers import get_manufacturer, list_manufacturers
from xknxmono.catalog.core.products import (
    ProductSummary,
    find_products_for_application,
    list_products,
)
from xknxmono.catalog.core.upload import upload_knxprod
from xknxmono.catalog.db import knxprod_dir_for, make_engine
from xknxmono.catalog.models import (
    CatalogSection,
    Hardware,
    HardwareProgram,
    Manufacturer,
)
from xknxmono.product import Application


class CatalogService:
    """Owns a catalog database (engine + its ``.knxprod`` store) and exposes the core operations."""

    def __init__(self, db_path: str | Path) -> None:
        db_path = Path(db_path)
        self._engine = make_engine(f"sqlite:///{db_path}")
        self._knxprod_dir = knxprod_dir_for(db_path)
        # Content-addressed cache for parsed application IR (see product.parse_cache), next to the
        # .knxprod store so it lives with the catalog it belongs to.
        self._parse_cache_dir = self._knxprod_dir.parent / "ir_cache"

    # --- ingest -----------------------------------------------------------

    def import_knxprod(self, content: bytes) -> Path:
        """Ingest ``.knxprod`` bytes; returns the stored file path (idempotent by content hash)."""
        return upload_knxprod(content, self._knxprod_dir, self._engine)

    # --- manufacturers ----------------------------------------------------

    def list_manufacturers(self) -> Sequence[Manufacturer]:
        with Session(self._engine) as db:
            return list_manufacturers(db)

    def get_manufacturer(self, manufacturer_id: str) -> Manufacturer | None:
        with Session(self._engine) as db:
            return get_manufacturer(db, manufacturer_id)

    # --- hardware ---------------------------------------------------------

    def list_hardware(
        self, filters: HardwareFilters | None = None
    ) -> Sequence[Hardware]:
        with Session(self._engine) as db:
            return list_hardware(db, filters)

    def get_hardware(self, hardware_id: str) -> Hardware | None:
        with Session(self._engine) as db:
            return get_hardware(db, hardware_id)

    def get_hardware_program(
        self, hardware_id: str, program_id: str
    ) -> HardwareProgram | None:
        with Session(self._engine) as db:
            return get_hardware_program(db, hardware_id, program_id)

    def get_application_xml(self, program_id: str) -> tuple[bytes, str] | None:
        with Session(self._engine) as db:
            return get_application_xml(db, program_id)

    def get_program_source(self, program_id: str) -> tuple[str, str] | None:
        """Return ``(knxprod_path, manufacturer_id)`` for a program id, or ``None``."""
        with Session(self._engine) as db:
            return get_program_source(db, program_id)

    def get_application_detail(self, program_id: str) -> Application | None:
        with Session(self._engine) as db:
            return get_application_detail(db, program_id)

    # --- catalog sections -------------------------------------------------

    def list_catalog_sections(self, manufacturer_id: str) -> Sequence[CatalogSection]:
        with Session(self._engine) as db:
            return list_catalog_sections(db, manufacturer_id)

    def catalog_tree(self, manufacturer_id: str) -> list[CatalogSectionNode]:
        """The manufacturer's catalog sections as a nested tree."""
        with Session(self._engine) as db:
            return build_catalog_tree(list_catalog_sections(db, manufacturer_id))

    def collect_section_ids(self, section_id: str) -> list[str]:
        with Session(self._engine) as db:
            return collect_section_ids(db, section_id)

    # --- applications -----------------------------------------------------

    def list_applications(self) -> list[ApplicationSummary]:
        """Every application with its manufacturer (an app-first view over the schema)."""
        with Session(self._engine) as db:
            return list_applications(db)

    def list_products(self) -> list[ProductSummary]:
        """Every orderable product with its program/application refs (a product-first view)."""
        with Session(self._engine) as db:
            return list_products(db)

    def get_application(
        self, application_id: str, language: str | None = None
    ) -> Application | None:
        """The parsed (IR-backed) application for an application id, or ``None``.

        ``language`` (KNX id like "de-DE" or prefix "de") localizes labels when available.
        The expensive XML parse is cached on disk next to the ``.knxprod`` store (content-addressed,
        so it stays correct across re-imports)."""
        with Session(self._engine) as db:
            return get_application_detail_by_id(
                db, application_id, language, cache_dir=self._parse_cache_dir
            )

    def find_products_for_application(
        self,
        *,
        manufacturer_id: str,
        application_number: int,
        application_version: int | None = None,
        mask_version: str | None = None,
    ) -> list[ProductSummary]:
        """Candidate products matching an application id read off a device."""
        with Session(self._engine) as db:
            return find_products_for_application(
                db,
                manufacturer_id=manufacturer_id,
                application_number=application_number,
                application_version=application_version,
                mask_version=mask_version,
            )
