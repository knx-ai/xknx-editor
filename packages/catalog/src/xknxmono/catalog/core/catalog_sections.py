"""Query functions and tree-building utilities for the hierarchical KNX catalog sections."""

from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass, field

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from xknxmono.catalog.models import CatalogSection


@dataclass
class CatalogSectionNode:
    """A node in a manufacturer's catalog hierarchy, ready for display or traversal.

    This is a plain Python dataclass (no ORM, no Pydantic) returned by
    :func:`build_catalog_tree`. It mirrors :class:`~xknxmono.catalog.models.CatalogSection`
    but with children already nested rather than stored flat in the database.
    """

    id: str
    """The section's unique identifier (e.g. ``"M-0001_CS-001"``)."""
    name: str
    """Human-readable section name."""
    number: str | None
    """Optional ordering/reference number assigned by the manufacturer."""
    manufacturer_id: str
    """The M-XXXX identifier of the manufacturer who owns this section."""
    parent_id: str | None
    """ID of the parent section, or ``None`` for top-level sections."""
    children: list["CatalogSectionNode"] = field(default_factory=list)  # type: ignore[assignment]
    """Nested child sections, sorted alphabetically by name."""


def list_catalog_sections(
    db: Session, manufacturer_id: str
) -> Sequence[CatalogSection]:
    """Return all catalog sections for a manufacturer as a flat list of ORM objects.

    Use :func:`build_catalog_tree` to convert the flat list into a nested tree.

    Args:
      db: An active SQLAlchemy session.
      manufacturer_id: The M-XXXX identifier of the manufacturer.

    Returns:
      A flat sequence of :class:`~xknxmono.catalog.models.CatalogSection` instances
      belonging to the given manufacturer.
    """
    return db.scalars(
        select(CatalogSection).where(CatalogSection.manufacturer_id == manufacturer_id)
    ).all()


def collect_section_ids(db: Session, section_id: str) -> list[str]:
    """Return the given section ID and all of its descendant section IDs.

    Uses a recursive CTE so the lookup is a single database round-trip regardless
    of hierarchy depth.

    Args:
      db: An active SQLAlchemy session.
      section_id: The root section whose subtree should be collected.

    Returns:
      A list of string IDs — the root section plus every descendant section.
    """
    result = db.execute(
        text("""
      WITH RECURSIVE subtree(id) AS (
        SELECT id FROM catalog_sections WHERE id = :sid
        UNION ALL
        SELECT s.id FROM catalog_sections s JOIN subtree st ON s.parent_id = st.id
      )
      SELECT id FROM subtree
    """),
        {"sid": section_id},
    )
    return [row[0] for row in result]


def build_catalog_tree(sections: Sequence[CatalogSection]) -> list[CatalogSectionNode]:
    """Convert a flat sequence of catalog sections into a nested tree.

    Sections are sorted alphabetically by name at each level. The input is
    typically the result of :func:`list_catalog_sections`.

    Args:
      sections: A flat collection of :class:`~xknxmono.catalog.models.CatalogSection`
        instances, all belonging to the same manufacturer.

    Returns:
      A list of top-level :class:`CatalogSectionNode` objects, each with
      ``children`` already populated recursively.
    """
    by_parent: dict[str | None, list[CatalogSection]] = defaultdict(list)
    for s in sections:
        by_parent[s.parent_id].append(s)

    def _build(parent_id: str | None) -> list[CatalogSectionNode]:
        return [
            CatalogSectionNode(
                id=s.id,
                name=s.name,
                number=s.number,
                manufacturer_id=s.manufacturer_id,
                parent_id=s.parent_id,
                children=_build(s.id),
            )
            for s in sorted(by_parent.get(parent_id, []), key=lambda x: x.name)
        ]

    return _build(None)
