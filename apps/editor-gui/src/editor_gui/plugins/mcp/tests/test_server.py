"""End-to-end tests for the embedded MCP server against the live GUI services (headless).

The GUI services are imgui-free, so we build them directly, wire a synchronous ``run_on_ui`` (tools
run inline instead of on a real imgui thread), and drive the tools through FastMCP's in-memory
``Client``. Bus tools are not exercised (no gateway); this covers the project/catalog DATA surface.
"""

from __future__ import annotations

import io
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

import pytest
from fastmcp import Client

from editor_gui.plugins.base import API_VERSION, Logger, PluginAPI
from editor_gui.plugins.catalog.service import CatalogService
from editor_gui.plugins.connection.service import ConnectionService
from editor_gui.plugins.keyring.service import KeyringService
from editor_gui.plugins.logger.service import LogService
from editor_gui.plugins.mcp.context import McpContext
from editor_gui.plugins.mcp.server import build_server
from editor_gui.plugins.monitor.service import MonitorService
from editor_gui.plugins.network.service import NetworkService
from editor_gui.plugins.project.service import ProjectService

T = TypeVar("T")

_FIXTURE = (
    Path(__file__).parents[7]
    / "packages/product/tests/fixtures/gira_2gang_button_interface.knxprod"
)


class _StubConnectionPlugin:
    """Stand-in for ConnectionPlugin so connection tools register without a real bus."""

    from editor_gui.plugins.connection.plugin import ConnectionState

    state = ConnectionState.DISCONNECTED
    connected = False
    controller_ip = "127.0.0.1"
    multicast_group = "224.0.23.12"
    is_routing = False


def _build_ctx(tmp_path: Path) -> McpContext:
    log = LogService()
    catalog = CatalogService(tmp_path / "catalog.xknxcatalog")
    project = ProjectService(catalog)
    connection = ConnectionService()
    for svc, name in (
        (catalog, "catalog"),
        (project, "project"),
        (connection, "connection"),
    ):
        if hasattr(svc, "set_logger"):
            svc.set_logger(Logger(log, name))
    monitor = MonitorService(connection)
    monitor.set_logger(Logger(log, "monitor"))
    network = NetworkService()
    network.set_logger(Logger(log, "network"))
    keyring = KeyringService()
    keyring.set_logger(Logger(log, "keyring"))

    api = PluginAPI(
        api_version=API_VERSION,
        project=project,
        catalog=catalog,
        connection=connection,
        log=log,
    )

    def run_on_ui(fn: Callable[[], T], *, timeout: float = 30.0) -> T:
        return fn()

    return McpContext(
        api=api,
        run_on_ui=run_on_ui,
        connection_plugin=_StubConnectionPlugin(),  # type: ignore[arg-type]
        monitor=monitor,
        network=network,
        keyring=keyring,
        log=Logger(log, "mcp"),
    )


def _build(tmp_path: Path) -> tuple[Any, ProjectService]:
    ctx = _build_ctx(tmp_path)
    return build_server(ctx), ctx.api.project


async def _data(client: Client, tool: str, /, **args: Any) -> Any:
    result = await client.call_tool(tool, args)
    return result.data


@pytest.mark.skipif(not _FIXTURE.exists(), reason="knxprod fixture missing")
async def test_full_edit_flow(tmp_path: Path) -> None:
    mcp, _project = _build(tmp_path)
    async with Client(mcp) as client:
        # New project.
        assert (await _data(client, "project_new", path=str(tmp_path / "p.xknx")))[
            "open"
        ] is True

        # Import a product into the catalog and find it (list tools return {items, count}).
        added = await _data(client, "catalog_import_knxprod", path=str(_FIXTURE))
        assert added["added_refs"]
        products = await _data(client, "catalog_list_products")
        assert products["count"] >= 1
        product_ref = products["items"][0]["product_ref_id"]

        # Add the device (returns the created device), then list its com-objects.
        device = await _data(client, "project_add_device", product_ref_id=product_ref)
        node_id = device["node_id"]
        assert isinstance(node_id, int)
        com_objects = (
            await _data(client, "project_list_com_objects", node_id=node_id)
        )["items"]
        assert com_objects
        linkable = next(co for co in com_objects if co["linkable"])
        ref_id, db_id = linkable["ref_id"], linkable["db_id"]

        # Parameters are introspectable (ref_id + allowed values), enabling project_set_parameter.
        params = await _data(client, "project_list_parameters", node_id=node_id)
        assert "count" in params and isinstance(params["items"], list)

        # Batch: create a GA and link the com-object atomically in one call.
        batch = await _data(
            client,
            "project_batch",
            operations=[
                {
                    "op": "create_group_address",
                    "params": {"address": "1/1/1", "name": "Test"},
                },
            ],
        )
        assert batch["applied"] is True and batch["ok"] == 1
        ga_id = batch["results"][0]["result"]["group_address_id"]

        link = await _data(
            client,
            "project_link_com_object",
            node_id=node_id,
            com_object_ref_id=ref_id,
            group_address_id=ga_id,
        )
        assert isinstance(link["link_id"], int)
        assert link["com_object_db_id"] == db_id

        # The link shows up in the GA's assignments.
        assignments = (
            await _data(client, "project_get_ga_assignments", group_address_id=ga_id)
        )["items"]
        assert any(a["com_object_db_id"] == db_id for a in assignments)

        # Undo removes the link.
        assert (await _data(client, "project_undo"))["undone"] is True
        assignments = (
            await _data(client, "project_get_ga_assignments", group_address_id=ga_id)
        )["items"]
        assert not any(a["com_object_db_id"] == db_id for a in assignments)

        # status aggregates project + capabilities.
        st = await _data(client, "status")
        assert st["project"]["open"] is True
        assert "FULL" in st["capabilities"]["download_scopes"]

        # Export to a .knxproj archive.
        dest = tmp_path / "out.knxproj"
        assert (await _data(client, "project_export_knxproj", dest=str(dest)))[
            "status"
        ] == "exported"
        assert dest.exists()


@pytest.mark.skipif(not _FIXTURE.exists(), reason="knxprod fixture missing")
async def test_project_tools_require_open_project(tmp_path: Path) -> None:
    mcp, _project = _build(tmp_path)
    async with Client(mcp) as client:
        status = await _data(client, "project_status")
        assert status["open"] is False
        with pytest.raises(Exception, match="no project is open"):
            await client.call_tool("project_add_device", {"product_ref_id": "x"})


async def test_catalog_docs_builds_manufacturer_links(tmp_path: Path) -> None:
    """catalog_docs returns a site-scoped manufacturer search plus a web search (no network/project)."""
    mcp, _project = _build(tmp_path)
    async with Client(mcp) as client:
        result = await _data(
            client,
            "catalog_docs",
            query="dimming curve",
            manufacturer="MDT technologies",
        )
        assert result["manufacturer"] == "MDT technologies"
        assert result["note"]  # guidance about large PDFs / preferring structured tools
        kinds = {r["kind"] for r in result["references"]}
        assert {"knx_database", "manufacturer_site", "web"} <= kinds
        knx = next(r for r in result["references"] if r["kind"] == "knx_database")
        assert "knx.org" in knx["url"]
        site = next(r for r in result["references"] if r["kind"] == "manufacturer_site")
        assert "mdt.de" in site["url"]


def test_manufacturer_domain_resolution() -> None:
    """Domain lookup is substring-based, so ordering and qualified keys matter (regression guard)."""
    from editor_gui.plugins.mcp.tools.catalog import _domain_for

    # more specific key wins where one catalog name contains another
    assert _domain_for("ABB AG - BUSCH-JAEGER") == "busch-jaeger.de"
    assert _domain_for("ABB AG - STOTZ-KONTAKT") == "abb.com"
    # qualified keys do not leak into unrelated names
    assert _domain_for("Insta GmbH") == "insta.de"
    assert _domain_for("Instell") is None
    assert _domain_for("MDT technologies") == "mdt.de"
    assert _domain_for(None) is None
    assert _domain_for("Totally Unknown Maker") is None


def _two_page_pdf() -> bytes:
    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.add_blank_page(width=200, height=200)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


async def test_docs_fetch_reads_pages_without_dumping(
    tmp_path: Path, monkeypatch: Any
) -> None:
    """catalog_docs_fetch returns page count + outline, a single page, and rejects bad input."""
    import editor_gui.plugins.mcp.tools.catalog as catalog_tools

    monkeypatch.setattr(
        catalog_tools, "_download_doc", lambda url, refresh=False: _two_page_pdf()
    )
    mcp, _project = _build(tmp_path)
    async with Client(mcp) as client:
        meta = await _data(client, "catalog_docs_fetch", url="https://knx.org/x.pdf")
        assert meta["total_pages"] == 2
        assert "outline" in meta

        one = await _data(
            client, "catalog_docs_fetch", url="https://knx.org/x.pdf", page=1
        )
        assert one["page"] == 1 and "text" in one

        with pytest.raises(Exception, match="out of range"):
            await client.call_tool(
                "catalog_docs_fetch", {"url": "https://knx.org/x.pdf", "page": 9}
            )


def test_download_pdf_is_cached(tmp_path: Path, monkeypatch: Any) -> None:
    """A PDF URL is downloaded once, then served from the on-disk cache (and re-read offline)."""
    import editor_gui.plugins.mcp.tools.catalog as catalog_tools

    monkeypatch.setattr(catalog_tools, "_docs_cache_dir", lambda: tmp_path)
    catalog_tools._MEM_CACHE.clear()
    calls = {"n": 0}

    def _fake_get(url: str) -> bytes:
        calls["n"] += 1
        return _two_page_pdf()

    monkeypatch.setattr(catalog_tools, "_http_get", _fake_get)
    first = catalog_tools._download_doc("https://knx.org/a.pdf")
    catalog_tools._MEM_CACHE.clear()  # force the on-disk path, not the process cache
    second = catalog_tools._download_doc("https://knx.org/a.pdf")
    assert first == second and calls["n"] == 1
    # it was persisted and indexed under a recognisable filename
    assert catalog_tools._read_index()
    catalog_tools._MEM_CACHE.clear()


def test_normalize_github_blob_url() -> None:
    """A github.com blob URL is rewritten to the raw file so the document (not HTML) is fetched."""
    from editor_gui.plugins.mcp.tools.catalog import _normalize_doc_url

    assert (
        _normalize_doc_url(
            "https://github.com/OpenKNX/OFM-LedModule/blob/v1/doc/Applikationsbeschreibung-LedDimmer.md"
        )
        == "https://raw.githubusercontent.com/OpenKNX/OFM-LedModule/v1/doc/Applikationsbeschreibung-LedDimmer.md"
    )
    # non-blob / non-github URLs pass through unchanged
    assert _normalize_doc_url("https://www.mdt.de/x.pdf") == "https://www.mdt.de/x.pdf"


async def test_docs_fetch_reads_markdown(tmp_path: Path, monkeypatch: Any) -> None:
    """A markdown doc is read as text (heading outline + capped text), and find returns line hits."""
    import editor_gui.plugins.mcp.tools.catalog as catalog_tools

    md = b"# Title\n\nintro line\n\n## Section A\n\nthe magic value is 42\n\n## Section B\n"
    monkeypatch.setattr(catalog_tools, "_download_doc", lambda url, refresh=False: md)
    mcp, _project = _build(tmp_path)
    async with Client(mcp) as client:
        meta = await _data(
            client,
            "catalog_docs_fetch",
            url="https://raw.githubusercontent.com/OpenKNX/x/v1/doc/a.md",
        )
        assert meta["content_type"] == "text"
        titles = [h["title"] for h in meta["outline"]]
        assert titles == ["Title", "Section A", "Section B"]
        assert "magic value" in meta["text"]

        hit = await _data(
            client,
            "catalog_docs_fetch",
            url="https://raw.githubusercontent.com/OpenKNX/x/v1/doc/a.md",
            find="magic",
        )
        assert hit["match_count"] == 1
        assert hit["matches"][0]["line"] == 7


async def test_docs_fetch_rejects_disallowed_host(tmp_path: Path) -> None:
    """The fetch is restricted to documentation hosts (no open SSRF)."""
    mcp, _project = _build(tmp_path)
    async with Client(mcp) as client:
        with pytest.raises(Exception, match="host not allowed"):
            await client.call_tool(
                "catalog_docs_fetch", {"url": "https://evil.example.com/x.pdf"}
            )


async def test_mutation_rejected_while_project_locked(tmp_path: Path) -> None:
    """A project mutation must reject with 'project busy' while a background worker holds io_lock."""
    ctx = _build_ctx(tmp_path)
    mcp = build_server(ctx)
    lock = ctx.api.catalog.io_lock
    async with Client(mcp) as client:
        await _data(client, "project_new", path=str(tmp_path / "p.xknx"))

        holding, release = threading.Event(), threading.Event()

        def _hold() -> None:  # stand-in for a background import/open worker
            lock.acquire()
            holding.set()
            release.wait(5.0)
            lock.release()

        worker = threading.Thread(target=_hold)
        worker.start()
        try:
            assert holding.wait(5.0)
            with pytest.raises(Exception, match="project busy"):
                await client.call_tool(
                    "project_create_group_address", {"address": "1/1/1"}
                )
        finally:
            release.set()
            worker.join(5.0)
