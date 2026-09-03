"""Query functions for KNX manufacturers stored in the catalog database."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from xknxmono.catalog.models import Manufacturer


def list_manufacturers(db: Session) -> Sequence[Manufacturer]:
    """Return all manufacturers in the catalog, ordered by their M-XXXX ID.

    Args:
      db: An active SQLAlchemy session.

    Returns:
      A sequence of :class:`~xknxmono.catalog.models.Manufacturer` ORM objects,
      sorted ascending by ``id``.
    """
    return db.scalars(select(Manufacturer).order_by(Manufacturer.id)).all()


def get_manufacturer(db: Session, manufacturer_id: str) -> Manufacturer | None:
    """Return a single manufacturer by its M-XXXX ID, or ``None`` if not found.

    Args:
      db: An active SQLAlchemy session.
      manufacturer_id: The manufacturer's primary-key identifier (e.g. ``"M-0001"``).

    Returns:
      A :class:`~xknxmono.catalog.models.Manufacturer` instance, or ``None`` if
      no manufacturer with that ID exists in the database.
    """
    return db.get(Manufacturer, manufacturer_id)
