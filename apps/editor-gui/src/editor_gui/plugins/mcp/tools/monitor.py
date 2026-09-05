# The @mcp.tool decorator registers each tool via its side effect, not a direct call.
# pyright: reportUnusedFunction=false
"""Group/bus monitor tools: read latest values and the telegram log, send GroupValue read/write."""

from __future__ import annotations

import time
from datetime import datetime
from typing import TYPE_CHECKING, Any

from fastmcp.exceptions import ToolError

from editor_gui.plugins.mcp.context import McpContext, make_tool

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP, ctx: McpContext) -> None:
    tool = make_tool(mcp, ctx)
    monitor = ctx.monitor

    def _require_connection() -> None:
        if ctx.api.connection.xknx is None:
            raise ToolError("no KNX connection")

    @tool
    def monitor_latest(address: str) -> dict[str, Any]:
        """The latest value seen on a group address (raw payload, timestamp, service)."""
        value = monitor.latest(address)
        if value is None:
            raise ToolError(f"no value seen for {address!r}")
        return {
            "address": address,
            "service": value.service,
            "timestamp": value.timestamp.isoformat(),
            "payload": str(value.payload),
        }

    @tool
    def monitor_telegrams(limit: int = 100) -> dict[str, Any]:
        """A snapshot of the live bus telegram log. ``limit`` caps the most recent entries (<=0 = all).

        Returns ``{items, count}`` with items oldest→newest."""
        records = monitor.telegrams()
        if limit > 0:
            records = records[-limit:]
        items = [
            {
                "timestamp": r.timestamp.isoformat(),
                "source": r.source,
                "destination": r.destination,
                "service": r.service,
                "payload": None if r.payload is None else str(r.payload),
            }
            for r in records
        ]
        return {"items": items, "count": len(items)}

    @tool
    def monitor_read_value(address: str, timeout: float = 3.0) -> dict[str, Any]:
        """Send a GroupValueRead and wait for a fresh response (``timeout`` seconds).

        Unlike monitor_send_read (fire-and-forget), this blocks until a telegram newer than the read
        is seen on ``address`` and returns it, or raises on timeout. Needs an open connection."""
        _require_connection()
        sent_at = datetime.now()
        monitor.send_read(address)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            value = monitor.latest(address)
            if value is not None and value.timestamp >= sent_at:
                return {
                    "address": address,
                    "service": value.service,
                    "timestamp": value.timestamp.isoformat(),
                    "payload": str(value.payload),
                }
            time.sleep(0.1)
        raise ToolError(
            f"no response on {address!r} within {timeout}s (device may not answer reads)"
        )

    @tool
    def monitor_clear() -> dict[str, str]:
        """Clear the monitor's stored values and telegram log."""
        monitor.clear()
        return {"status": "cleared"}

    @tool
    def monitor_send_write(
        address: str, value: str, dpt: str | None = None
    ) -> dict[str, str]:
        """Send a GroupValueWrite. ``dpt`` defaults to the group address' configured DPT if known."""
        _require_connection()
        resolved = dpt
        if resolved is None:
            resolved = ctx.run_locked(
                lambda: next(
                    (
                        g.datapoint_type
                        for g in ctx.api.project.group_addresses
                        if g.address == address
                    ),
                    None,
                )
            )
        if not monitor.send_write(address, resolved, value):
            raise ToolError(f"could not encode value {value!r} for DPT {resolved!r}")
        # Fire-and-forget: the value was encoded and queued onto the bus loop; actual delivery is not
        # awaited here. Read it back with monitor_latest to confirm the effect.
        return {"status": "queued", "address": address}

    @tool
    def monitor_send_read(address: str) -> dict[str, str]:
        """Send a GroupValueRead to a group address (fire-and-forget; poll monitor_latest for the reply)."""
        _require_connection()
        monitor.send_read(address)
        return {"status": "queued", "address": address}
