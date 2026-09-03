"""Catalog sections router: return the hierarchical product catalog for a manufacturer."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from xknxmono.catalog.core.catalog_sections import CatalogSectionNode
from xknxmono.catalog.core.service import CatalogService
from xknxmono.catalog.http.deps import get_service
from xknxmono.catalog.http.schemas import CatalogSectionResponse

router = APIRouter(prefix="/manufacturers", tags=["Manufacturers"])

ServiceDep = Annotated[CatalogService, Depends(get_service)]

_cache: dict[str, list[CatalogSectionResponse]] = {}


def _node_to_out(node: CatalogSectionNode) -> CatalogSectionResponse:
    """Convert a :class:`~xknxmono.catalog.core.catalog_sections.CatalogSectionNode` to its API response schema."""
    return CatalogSectionResponse(
        id=node.id,
        name=node.name,
        number=node.number,
        manufacturer_id=node.manufacturer_id,
        parent_id=node.parent_id,
        children=[_node_to_out(child) for child in node.children],
    )


@router.get(
    "/{manufacturer_id}/catalog-sections", response_model=list[CatalogSectionResponse]
)
def list_catalog_sections_endpoint(manufacturer_id: str, service: ServiceDep):
    """Return the full catalog section tree for a manufacturer, with results cached in memory."""
    if not service.get_manufacturer(manufacturer_id):
        raise HTTPException(404, "Manufacturer not found")
    if manufacturer_id not in _cache:
        tree = service.catalog_tree(manufacturer_id)
        _cache[manufacturer_id] = [_node_to_out(node) for node in tree]
    return _cache[manufacturer_id]
