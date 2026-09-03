"""Query functions for KNX hardware items, programs, and application details."""

import datetime
from collections.abc import Sequence

from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from xknxmono.catalog.core.catalog_sections import collect_section_ids
from xknxmono.catalog.models import (
    Application,
    CatalogSection,
    CatalogSectionProduct,
    Hardware,
    HardwareProgram,
    HardwareProgramMediumType,
)


class HardwareFilters(BaseModel):
    """Filter parameters for :func:`list_hardware`.

    All fields default to their "no filter" state so callers only set what they
    need. String and boolean filters are ANDed together. Repeatable list filters
    (``manufacturer_id``, ``medium_type``) match any item in the list (OR within
    the list, AND with other filters).

    This is a Pydantic model so it doubles as a FastAPI query-parameter model
    (``Annotated[HardwareFilters, Query()]``) with working list defaults.
    """

    manufacturer_id: list[str] = Field(default_factory=list)
    """Restrict results to hardware belonging to these manufacturer M-XXXX IDs."""
    medium_type: list[str] = Field(default_factory=list)
    """Restrict results to hardware that supports at least one of these medium types (e.g. ``"TP"``, ``"IP"``, ``"RF"``)."""
    section_id: str | None = None
    """Restrict results to hardware listed in this catalog section or any of its descendants."""
    is_secure_enabled: bool | None = None
    """Filter by whether the linked application program has KNX Secure enabled."""
    is_rail_mounted: bool | None = None
    """Filter by DIN rail mounting flag."""
    is_coupler: bool | None = None
    """Filter by coupler flag."""
    is_power_supply: bool | None = None
    """Filter by power supply flag."""
    is_ip_enabled: bool | None = None
    """Filter by IP-enabled flag."""
    has_application_program: bool | None = None
    """Filter by whether the hardware has an associated application program."""
    no_download_without_plugin: bool | None = None
    """Filter by whether download requires an ETS plug-in."""
    registration_status: str | None = None
    """Filter by registration status string (e.g. ``"Registered"``)."""
    registration_number: str | None = None
    """Filter by exact registration number."""
    registration_date_from: datetime.date | None = None
    """Inclusive lower bound for registration date."""
    registration_date_to: datetime.date | None = None
    """Inclusive upper bound for registration date."""
    mask_version: str | None = None
    """Filter by application mask version string."""
    search: str | None = None
    """Case-insensitive substring search across hardware name and order number."""
    limit: int = 50
    """Maximum number of results to return (hard cap enforced by the HTTP layer)."""
    offset: int = 0
    """Number of results to skip before returning (for pagination)."""


def _base_query():
    """Return a base SQLAlchemy select for Hardware with programs and medium types eagerly loaded."""
    return select(Hardware).options(
        selectinload(Hardware.programs).selectinload(HardwareProgram.medium_types),
        selectinload(Hardware.programs).selectinload(HardwareProgram.application),
    )


def list_hardware(
    db: Session, filters: HardwareFilters | None = None
) -> Sequence[Hardware]:
    """Return hardware items matching the given filters, with programs eagerly loaded.

    All filter fields in :class:`HardwareFilters` are optional. Passing ``None``
    (or omitting the argument) returns up to ``filters.limit`` results with no
    filtering applied.

    Args:
      db: An active SQLAlchemy session.
      filters: A :class:`HardwareFilters` instance describing which hardware to
        include. Defaults to ``HardwareFilters()`` (50 results, no filters).

    Returns:
      A sequence of :class:`~xknxmono.catalog.models.Hardware` ORM objects with
      ``programs``, ``medium_types``, and ``application`` relationships loaded.
    """
    if filters is None:
        filters = HardwareFilters()

    q = _base_query()

    needs_program_join = bool(
        filters.medium_type
        or filters.is_secure_enabled is not None
        or filters.mask_version is not None
        or filters.registration_status is not None
        or filters.registration_number is not None
        or filters.registration_date_from is not None
        or filters.registration_date_to is not None
        or filters.section_id is not None
    )
    if needs_program_join:
        q = q.join(Hardware.programs)

    if filters.manufacturer_id:
        q = q.where(Hardware.manufacturer_id.in_(filters.manufacturer_id))
    if filters.is_rail_mounted is not None:
        q = q.where(Hardware.is_rail_mounted == filters.is_rail_mounted)
    if filters.is_coupler is not None:
        q = q.where(Hardware.is_coupler == filters.is_coupler)
    if filters.is_power_supply is not None:
        q = q.where(Hardware.is_power_supply == filters.is_power_supply)
    if filters.is_ip_enabled is not None:
        q = q.where(Hardware.is_ip_enabled == filters.is_ip_enabled)
    if filters.has_application_program is not None:
        q = q.where(Hardware.has_application_program == filters.has_application_program)
    if filters.no_download_without_plugin is not None:
        q = q.where(
            Hardware.no_download_without_plugin == filters.no_download_without_plugin
        )
    if filters.search:
        term = f"%{filters.search}%"
        q = q.where(Hardware.name.ilike(term) | Hardware.order_number.ilike(term))
    if filters.medium_type:
        q = q.join(HardwareProgram.medium_types).where(
            HardwareProgramMediumType.medium_type.in_(filters.medium_type)
        )
    if filters.is_secure_enabled is not None or filters.mask_version is not None:
        q = q.join(HardwareProgram.application, isouter=True)
        if filters.is_secure_enabled is not None:
            q = q.where(Application.is_secure_enabled == filters.is_secure_enabled)
        if filters.mask_version is not None:
            q = q.where(Application.mask_version == filters.mask_version)
    if filters.registration_status is not None:
        q = q.where(HardwareProgram.registration_status == filters.registration_status)
    if filters.registration_number is not None:
        q = q.where(HardwareProgram.registration_number == filters.registration_number)
    if filters.registration_date_from is not None:
        q = q.where(HardwareProgram.registration_date >= filters.registration_date_from)
    if filters.registration_date_to is not None:
        q = q.where(HardwareProgram.registration_date <= filters.registration_date_to)
    if filters.section_id is not None:
        ids = collect_section_ids(db, filters.section_id)
        q = (
            q.join(
                CatalogSectionProduct,
                CatalogSectionProduct.hardware_program_id == HardwareProgram.id,
            )
            .join(CatalogSection, CatalogSection.id == CatalogSectionProduct.section_id)
            .where(CatalogSection.id.in_(ids))
        )

    q = q.distinct().offset(filters.offset).limit(filters.limit)
    return db.scalars(q).unique().all()


def get_hardware(db: Session, hardware_id: str) -> Hardware | None:
    """Return a single hardware item by ID with programs eagerly loaded, or ``None`` if not found.

    Args:
      db: An active SQLAlchemy session.
      hardware_id: The hardware's primary-key identifier.

    Returns:
      A :class:`~xknxmono.catalog.models.Hardware` instance with ``programs``,
      ``medium_types``, and ``application`` relationships loaded, or ``None``.
    """
    return db.scalars(_base_query().where(Hardware.id == hardware_id)).first()


def get_hardware_program(
    db: Session, hardware_id: str, program_id: str
) -> HardwareProgram | None:
    """Return a hardware program that belongs to the given hardware item, or ``None`` if not found.

    The ``hardware_id`` check ensures the program is actually associated with the
    specified hardware, which is useful for access-control in the HTTP layer.

    Args:
      db: An active SQLAlchemy session.
      hardware_id: The hardware's primary-key identifier.
      program_id: The hardware program's primary-key identifier.

    Returns:
      A :class:`~xknxmono.catalog.models.HardwareProgram` instance with the
      ``hardware`` relationship loaded, or ``None``.
    """
    return db.scalars(
        select(HardwareProgram)
        .options(selectinload(HardwareProgram.hardware))
        .where(
            HardwareProgram.id == program_id,
            HardwareProgram.hardware_id == hardware_id,
        )
    ).first()


def get_program_source(db: Session, program_id: str) -> tuple[str, str] | None:
    """Return ``(knxprod_path, manufacturer_id)`` for a hardware program, or ``None``.

    Resolves a program by its id alone (as stored on a project device's
    ``hardware2program_ref_id``) to the on-disk ``.knxprod`` it was imported from and its
    manufacturer, so callers can re-extract the manufacturer XMLs from that archive.

    Args:
      db: An active SQLAlchemy session.
      program_id: The hardware program's primary-key identifier.

    Returns:
      A ``(knxprod_path, manufacturer_id)`` tuple, or ``None`` if the program is unknown.
    """
    row = db.execute(
        select(HardwareProgram.knxprod_path, Hardware.manufacturer_id)
        .join(Hardware, Hardware.id == HardwareProgram.hardware_id)
        .where(HardwareProgram.id == program_id)
    ).first()
    if row is None:
        return None
    return row[0], row[1]
