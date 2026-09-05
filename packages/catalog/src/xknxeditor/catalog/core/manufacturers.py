"""Manufacturer queries."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from xknxeditor.catalog.models import Manufacturer


def list_manufacturers(db: Session) -> Sequence[Manufacturer]:
    """All manufacturers ordered by id."""
    return db.scalars(select(Manufacturer).order_by(Manufacturer.id)).all()


def get_manufacturer(db: Session, manufacturer_id: str) -> Manufacturer | None:
    """Lookup by M-XXXX id, or ``None``."""
    return db.get(Manufacturer, manufacturer_id)
