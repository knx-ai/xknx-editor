# The @mcp.tool decorator registers each tool via its side effect, not a direct call.
# pyright: reportUnusedFunction=false
"""Network-capture (diagnostics) tools: start/stop a CEMI/telegram capture and read the buffers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from editor_gui.plugins.mcp.context import McpContext, make_tool

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP, ctx: McpContext) -> None:
    tool = make_tool(mcp, ctx)
    network = ctx.network

    @tool
    def network_state() -> dict[str, Any]:
        """Whether a CEMI capture is running and how many records are buffered."""
        return {
            "state": network.state.value,
            "telegrams": len(network.telegrams),
            "cemi_records": len(network.cemi_records),
        }

    @tool
    def network_start() -> dict[str, str]:
        """Start capturing CEMI frames/telegrams (clears the buffers)."""
        network.start()
        return {"status": "capturing"}

    @tool
    def network_stop() -> dict[str, str]:
        """Stop capturing."""
        network.stop()
        return {"status": "stopped"}

    @tool
    def network_clear() -> dict[str, str]:
        """Clear the capture buffers."""
        network.clear()
        return {"status": "cleared"}

    @tool
    def network_telegrams(limit: int = 100) -> dict[str, Any]:
        """A snapshot of captured telegrams (``limit`` caps most recent; <=0 = all). Returns {items, count}."""
        records = network.telegrams
        if limit > 0:
            records = records[-limit:]
        items = [
            {
                "timestamp": r.timestamp.isoformat(),
                "source_type": r.source_type.value,
                "telegram": str(r.telegram),
            }
            for r in records
        ]
        return {"items": items, "count": len(items)}

    @tool
    def network_cemi_records(limit: int = 100) -> dict[str, Any]:
        """A snapshot of captured raw CEMI records (``limit`` caps most recent; <=0 = all)."""
        records = network.cemi_records
        if limit > 0:
            records = records[-limit:]
        items = [
            {
                "timestamp": r.timestamp.isoformat(),
                "source_type": r.source_type.value,
                "msg_code": r.msg_code,
                "src_addr": r.src_addr,
                "dst_addr": r.dst_addr,
                "hops": r.hops,
                "raw": r.raw.hex(" "),
            }
            for r in records
        ]
        return {"items": items, "count": len(items)}
