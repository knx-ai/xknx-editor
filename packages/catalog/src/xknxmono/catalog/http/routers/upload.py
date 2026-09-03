"""Upload router: accept .knxprod file uploads and ingest them into the catalog."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from xknxmono.catalog.core.service import CatalogService
from xknxmono.catalog.http.deps import get_service
from xknxmono.product.errors import ArchiveError

router = APIRouter(prefix="/upload", tags=["Upload"])

ServiceDep = Annotated[CatalogService, Depends(get_service)]


@router.post("")
async def upload_knxprod(file: UploadFile, service: ServiceDep):
    """Accept a .knxprod file upload and ingest it into the catalog database.

    Returns the stored filename. Duplicate uploads (same content) are ignored silently.
    """
    if not file.filename or not file.filename.endswith(".knxprod"):
        raise HTTPException(400, "File must be a .knxprod archive")
    content = await file.read()
    try:
        saved = service.import_knxprod(content)
    except ArchiveError as e:
        raise HTTPException(422, str(e)) from e
    except Exception as e:
        raise HTTPException(500, str(e)) from e
    return {"filename": saved.name}
