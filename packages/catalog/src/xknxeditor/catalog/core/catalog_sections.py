"""Catalog section queries and tree assembly."""

from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass, field

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from xknxeditor.catalog.models import CatalogSection


@dataclass
class CatalogSectionNode:
    """Pre-nested catalog section node (plain dataclass, not ORM)."""

    id: str
    name: str
    number: str | None
    manufacturer_id: str
    parent_id: str | None
    children: list["CatalogSectionNode"] = field(default_factory=list)  # type: ignore[assignment]


def list_catalog_sections(
    db: Session, manufacturer_id: str
) -> Sequence[CatalogSection]:
    """Flat list of catalog sections for a manufacturer (feed to ``build_catalog_tree``)."""
    return db.scalars(
        select(CatalogSection).where(CatalogSection.manufacturer_id == manufacturer_id)
    ).all()


def collect_section_ids(db: Session, section_id: str) -> list[str]:
    """Collect ``section_id`` and all descendant ids via a recursive CTE."""
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
    """Nest flat sections into a tree sorted alphabetically at each level."""
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
