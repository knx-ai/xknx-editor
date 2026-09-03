"""FastAPI dependencies for the catalog HTTP layer.

The application owns a single :class:`~xknxmono.catalog.core.service.CatalogService` (created in the
lifespan handler in :mod:`xknxmono.catalog.http.app` and stored on ``app.state.service``); routers
depend on it rather than on a session or engine directly.
"""

from fastapi import Request

from xknxmono.catalog.core.service import CatalogService


def get_service(request: Request) -> CatalogService:
    """Return the application's catalog service."""
    return request.app.state.service
