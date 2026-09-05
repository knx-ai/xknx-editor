# The @mcp.tool decorator registers each tool via its side effect, not a direct call.
# pyright: reportUnusedFunction=false
"""Keyring tools: load a password-protected KNX .knxkeys keyring, clear it, report status."""

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
        """Decrypt and load a KNX .knxkeys keyring into memory (raises on a wrong password)."""
        keyring.load(Path(path), password)
        return {"loaded": True, "path": str(keyring.path) if keyring.path else None}

    @tool
    def keyring_export(path: str, password: str) -> dict[str, Any]:
        """Export the loaded keyring to ``path``, re-encrypted and signed under ``password``.

        Same key material under a (possibly) different keyring password. Requires a loaded keyring.
        """
        keyring.export(Path(path), password)
        return {"exported": True, "path": path}

    @tool
    def keyring_clear() -> dict[str, str]:
        """Discard the loaded keyring."""
        keyring.clear()
        return {"status": "cleared"}

    @tool
    def keyring_status() -> dict[str, Any]:
        """Whether a keyring is loaded, its source path and project name."""
        return {
            "loaded": keyring.keyring is not None,
            "path": str(keyring.path) if keyring.path else None,
            "project": keyring.project_name or None,
        }
