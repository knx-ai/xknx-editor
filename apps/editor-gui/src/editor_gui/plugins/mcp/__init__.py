"""Embedded MCP server plugin: exposes the editor's live services as MCP tools over HTTP."""

from editor_gui.plugins.mcp.context import McpContext
from editor_gui.plugins.mcp.plugin import McpServerPlugin
from editor_gui.plugins.mcp.server import build_server

__all__ = ["McpContext", "McpServerPlugin", "build_server"]
