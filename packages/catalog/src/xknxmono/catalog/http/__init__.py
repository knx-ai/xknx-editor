"""Thin FastAPI HTTP layer over the catalog query functions.

The ``app`` object and ``main`` entry point are the primary exports. Import
them when you need to mount the catalog API into another ASGI application or
start the server programmatically::

  from xknxmono.catalog.http import app, main
"""

from xknxmono.catalog.http.app import app, main

__all__ = ["app", "main"]
