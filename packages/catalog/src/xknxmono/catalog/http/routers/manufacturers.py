"""Manufacturers router: list and retrieve KNX manufacturers from the catalog."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from xknxmono.catalog.core.service import CatalogService
from xknxmono.catalog.http.deps import get_service
from xknxmono.catalog.http.schemas import ManufacturerResponse

router = APIRouter(prefix="/manufacturers", tags=["Manufacturers"])

ServiceDep = Annotated[CatalogService, Depends(get_service)]


@router.get("", response_model=list[ManufacturerResponse])
def list_manufacturers_endpoint(service: ServiceDep):
    """Return all manufacturers in the catalog, ordered by ID."""
    return service.list_manufacturers()


@router.get("/{manufacturer_id}", response_model=ManufacturerResponse)
def get_manufacturer_endpoint(manufacturer_id: str, service: ServiceDep):
    """Return a single manufacturer by its M-XXXX ID."""
    mfr = service.get_manufacturer(manufacturer_id)
    if not mfr:
        raise HTTPException(404, "Manufacturer not found")
    return mfr
