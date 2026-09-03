# The @mcp.tool decorator registers each tool via its side effect, not a direct call.
# pyright: reportUnusedFunction=false
"""Keyring tools: load a password-protected ETS .knxkeys keyring, clear it, report status."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from editor_gui.plugins.mcp.context import McpContext, make_tool

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP, ctx: McpContext) -> None:
    tool = make_tool(mcp, ctx)
    keyring = ctx.keyring

    @tool
    def keyring_load(path: str, password: str) -> dict[str, Any]:
        """Decrypt and load an ETS .knxkeys keyring into memory (raises on a wrong password)."""
        keyring.load(Path(path), password)
        return {"loaded": True, "path": str(keyring.path) if keyring.path else None}

    @tool
    def keyring_clear() -> dict[str, str]:
        """Discard the loaded keyring."""
        keyring.clear()
        return {"status": "cleared"}

    @tool
    def keyring_status() -> dict[str, Any]:
        """Whether a keyring is loaded and its source path."""
        return {
            "loaded": keyring.keyring is not None,
            "path": str(keyring.path) if keyring.path else None,
        }
