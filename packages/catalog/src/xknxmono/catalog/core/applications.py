"""Application-centric catalog queries.

The catalog schema is hardware-centric (an :class:`Application` is reached through the hardware
programs that reference it), but consumers such as a device-picker want a flat, app-first view.
These helpers provide that: list every application with the manufacturer that ships it, and resolve
the application XML / parsed detail from a hardware-program id or straight from an application id.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from xknxmono.catalog.models import (
    Application,
    Hardware,
    HardwareProgram,
    Manufacturer,
)

if TYPE_CHECKING:
    from pathlib import Path

    from xknxmono.product import Application as ProductApplication


@dataclass(frozen=True)
class ApplicationSummary:
    """A flat, app-first catalog entry: an application plus the manufacturer that ships it."""

    application_id: str
    name: str
    manufacturer_id: str
    manufacturer_name: str | None


def list_applications(db: Session) -> list[ApplicationSummary]:
    """Every application with its manufacturer, resolved via the hardware programs that use it."""
    rows = db.execute(
        select(Application.id, Application.name, Manufacturer.id, Manufacturer.name)
        .join(HardwareProgram, HardwareProgram.application_id == Application.id)
        .join(Hardware, Hardware.id == HardwareProgram.hardware_id)
        .join(Manufacturer, Manufacturer.id == Hardware.manufacturer_id)
        .distinct()
    ).all()
    return [
        ApplicationSummary(
            application_id=app_id,
            name=name,
            manufacturer_id=mfr_id,
            manufacturer_name=mfr_name,
        )
        for app_id, name, mfr_id, mfr_name in rows
    ]


def get_application_xml(db: Session, program_id: str) -> tuple[bytes, str] | None:
    """Return the raw application XML bytes and manufacturer ID for a hardware program.

    Opens the ``.knxprod`` archive on disk for the given program and extracts the
    application XML. Returns ``None`` if the program does not exist or has no
    associated application, or if the application XML is not found in the archive.

    Args:
      db: An active SQLAlchemy session.
      program_id: The hardware program's primary-key identifier.

    Returns:
      A ``(xml_bytes, manufacturer_id)`` tuple, or ``None`` if not found.

    Raises:
      :exc:`xknxmono.product.errors.ArchiveError`: If the ``.knxprod`` archive
        cannot be opened or read.
    """
    program = db.scalars(
        select(HardwareProgram)
        .options(selectinload(HardwareProgram.hardware))
        .where(HardwareProgram.id == program_id)
    ).first()
    if not program or not program.application_id:
        return None

    from xknxmono.product.archive import Archive

    manufacturer_id = program.hardware.manufacturer_id
    archive = Archive(program.knxprod_path)
    with archive:
        app_xmls = archive.get_application_xmls(manufacturer_id)
        xml_bytes = app_xmls.get(program.application_id)
        if xml_bytes is None:
            return None
        return xml_bytes, manufacturer_id


def get_application_detail(
    db: Session,
    program_id: str,
    language: str | None = None,
    cache_dir: Path | None = None,
) -> ProductApplication | None:
    """Return the parsed application detail for a hardware program.

    Opens the ``.knxprod`` archive and parses the application XML. Returns ``None`` if
    the program does not exist, has no linked application, or the application is
    not present in the archive.

    Args:
      db: An active SQLAlchemy session.
      program_id: The hardware program's primary-key identifier.

    Returns:
      A :class:`~xknxmono.product.application.Application` instance with
      com objects, parameters, and code populated, or ``None`` if not found.

    Raises:
      :exc:`xknxmono.product.errors.ArchiveError`: If the ``.knxprod`` archive
        cannot be opened or read.
    """
    program = db.scalars(
        select(HardwareProgram)
        .options(selectinload(HardwareProgram.hardware))
        .where(HardwareProgram.id == program_id)
    ).first()
    if not program or not program.application_id:
        return None

    from xknxmono.product import parse_application_xml
    from xknxmono.product.archive import Archive

    manufacturer_id = program.hardware.manufacturer_id
    archive = Archive(program.knxprod_path)
    with archive:
        app_xmls = archive.get_application_xmls(manufacturer_id)
        xml_bytes = app_xmls.get(program.application_id)
        if xml_bytes is None:
            return None
        apps = parse_application_xml(
            xml_bytes, manufacturer_id, language, cache_dir=cache_dir
        )
        return next((a for a in apps if a.id == program.application_id), None)


def get_application_detail_by_id(
    db: Session,
    application_id: str,
    language: str | None = None,
    cache_dir: Path | None = None,
) -> ProductApplication | None:
    """Parsed application detail for an application id, via any hardware program that references it.

    Returns the IR-backed product :class:`~xknxmono.product.Application`, or ``None`` if no program
    references the id (or its archive no longer holds the application). ``language`` (KNX id such as
    "de-DE", or a prefix like "de") localizes the labels when the .knxprod carries that language.
    """
    program_id = db.scalars(
        select(HardwareProgram.id)
        .where(HardwareProgram.application_id == application_id)
        .limit(1)
    ).first()
    if program_id is None:
        return None
    return get_application_detail(db, program_id, language, cache_dir)
