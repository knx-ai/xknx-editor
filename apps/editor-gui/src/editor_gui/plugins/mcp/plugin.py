"""Embedded MCP server lifecycle: run FastMCP over Streamable HTTP on a daemon thread.

The editor's main thread is blocked by the imgui run loop, so the server (uvicorn + its own asyncio
loop) runs on a dedicated thread — mirroring the connection plugin's "KNX-Async" thread. Start/stop is
driven from the Settings > MCP tab; ``stop`` asks uvicorn to exit and joins the thread.
"""

from __future__ import annotations

import os
import threading
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from editor_gui.plugins.base import Logger
from editor_gui.plugins.mcp.context import McpContext
from editor_gui.plugins.mcp.server import build_server

if TYPE_CHECKING:
    import uvicorn

    from editor_gui.plugins.base import PluginAPI
    from editor_gui.plugins.connection.plugin import ConnectionPlugin
    from editor_gui.plugins.keyring.service import KeyringService
    from editor_gui.plugins.monitor.service import MonitorService
    from editor_gui.plugins.network.service import NetworkService


def _build_auth(token: str = "") -> Any:
    """Optional bearer-token auth for the HTTP endpoint.

    The token comes from the Settings > MCP field (``token`` arg); if empty it falls back to the
    ``XKNX_MCP_AUTH_TOKEN`` env var. When neither is set, the endpoint is unauthenticated."""
    token = (token or os.environ.get("XKNX_MCP_AUTH_TOKEN", "")).strip()
    if not token:
        return None
    from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

    return StaticTokenVerifier(
        tokens={token: {"client_id": "xknx-editor", "scopes": []}}
    )


class McpServerPlugin:
    """Owns the embedded MCP server thread. Wired directly in ``main.py`` (not via the registry)."""

    name = "mcp"

    def __init__(
        self,
        api: PluginAPI,
        run_on_ui: Callable[..., Any],
        connection_plugin: ConnectionPlugin,
        monitor: MonitorService,
        network: NetworkService,
        keyring: KeyringService,
    ) -> None:
        self._log = Logger(api.log, "mcp")
        self._ctx = McpContext(
            api=api,
            run_on_ui=run_on_ui,
            connection_plugin=connection_plugin,
            monitor=monitor,
            network=network,
            keyring=keyring,
            log=self._log,
        )
        self._server: uvicorn.Server | None = None
        self._thread: threading.Thread | None = None

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self, host: str, port: int, token: str = "") -> None:
        if self.is_running:
            return
        import uvicorn

        auth = _build_auth(token)
        if auth is None and host not in ("127.0.0.1", "::1", "localhost"):
            # No token on a non-loopback bind means anyone who can reach this host can read/edit the
            # project and drive the KNX bus. Surface it loudly; do not silently expose it.
            self._log.warning(
                "MCP server exposed on a non-loopback address without a bearer token",
                host=host,
            )
        app = build_server(self._ctx, auth=auth).http_app()
        config = uvicorn.Config(app, host=host, port=port, log_level="warning")
        self._server = uvicorn.Server(config)
        self._thread = threading.Thread(
            target=self._server.run, daemon=True, name="xknxeditor-mcp"
        )
        self._thread.start()
        self._log.info(
            "MCP server started", host=host, port=port, auth=auth is not None
        )

    def stop(self) -> None:
        if self._server is not None:
            self._server.should_exit = True
        if self._thread is not None:
            self._thread.join(timeout=10.0)
            if self._thread.is_alive():
                # The server did not exit in time. Keep the references so is_running stays true and a
                # second server cannot be started on the same port while this one is still finishing.
                self._log.warning(
                    "MCP server did not stop within timeout; still shutting down"
                )
                return
        self._server = None
        self._thread = None
        self._log.info("MCP server stopped")
