import asyncio
import contextlib
import math
import threading
from collections.abc import Coroutine
from concurrent.futures import Future
from enum import Enum
from typing import Any

from imgui_bundle import imgui, imspinner
from xknx import XKNX
from xknx.io.connection import ConnectionConfig, ConnectionType
from xknx.io.const import DEFAULT_MCAST_GRP
from xknx.io.gateway_scanner import GatewayDescriptor, GatewayScanner
from xknx.io.self_description import request_description

from editor_gui.color import color_u32
from editor_gui.plugins.base import Logger, PanelDefinition, PluginAPI
from editor_gui.plugins.connection.interface import ObservableKNXIPInterfaceThreaded
from editor_gui.plugins.connection.strings import S
from editor_gui.settings import load_settings, save_settings

_SETTINGS = "connection"

# Delay before the one-shot autostart re-scan (macOS Local Network permission grant window).
_AUTOSTART_RETRY_SECONDS = 30.0


class ConnectionState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTING = "disconnecting"
    ERROR = "error"


class ConnectionPlugin:
    name = "connection"

    def __init__(self, api: PluginAPI) -> None:
        self._api = api
        api.connection.set_logger(Logger(api.log, "connection"))
        self._log = Logger(api.log, "connection")
        self._state = ConnectionState.DISCONNECTED
        self._error_message: str | None = None
        self._controller_ip: str = "192.168.1.1"
        self._connection_type: ConnectionType = ConnectionType.TUNNELING
        self._multicast_group: str = DEFAULT_MCAST_GRP
        self._selected_gateway: GatewayDescriptor | None = None
        # The gateway the user last connected to; preferred on startup auto-connect.
        self._preferred_gateway_ip: str | None = None
        self._panels: list[PanelDefinition] = []
        self._load_saved_settings()

        self._xknx: XKNX | None = None
        self._interface: ObservableKNXIPInterfaceThreaded | None = None
        self._gateway_info: GatewayDescriptor | None = None
        self._async_loop: asyncio.AbstractEventLoop | None = None
        self._async_thread: threading.Thread | None = None

        self._gateways: list[GatewayDescriptor] = []
        self._scanning = False
        # One-shot re-scan after autostart found nothing: on macOS the first discovery triggers the
        # "Local Network" permission prompt and returns no gateways; a delayed retry picks them up
        # once the user has allowed it. Guarded so it fires at most once per autostart.
        self._autostart_retry_done = False

    @property
    def state(self) -> ConnectionState:
        return self._state

    @property
    def connected(self) -> bool:
        return self._state == ConnectionState.CONNECTED

    @property
    def controller_ip(self) -> str:
        return self._controller_ip

    @property
    def multicast_group(self) -> str:
        return self._multicast_group

    @property
    def is_routing(self) -> bool:
        return self._connection_type == ConnectionType.ROUTING

    @property
    def scanning(self) -> bool:
        """Whether a gateway discovery scan is currently running."""
        return self._scanning

    @property
    def gateways(self) -> list[GatewayDescriptor]:
        """The gateways found by the most recent scan."""
        return list(self._gateways)

    def connect_to_gateway_by_ip(self, ip: str) -> bool:
        """Connect to a previously discovered gateway by IP. Returns ``False`` if none matches."""
        gateway = next((g for g in self._gateways if g.ip_addr == ip), None)
        if gateway is None:
            return False
        self.connect_to_gateway(gateway)
        return True

    def configure(
        self, controller_ip: str, multicast_group: str, routing: bool
    ) -> None:
        """Apply and persist connection settings from the options dialog (takes effect on next
        connect)."""
        self._controller_ip = controller_ip.strip() or self._controller_ip
        self._multicast_group = multicast_group.strip() or self._multicast_group
        self._connection_type = (
            ConnectionType.ROUTING if routing else ConnectionType.TUNNELING
        )
        self._save_current_settings()
        self._log.info(
            "connection settings saved",
            controller_ip=self._controller_ip,
            routing=routing,
        )

    def _ensure_async_loop(self) -> asyncio.AbstractEventLoop:
        if self._async_loop is not None and self._async_loop.is_running():
            return self._async_loop

        loop_ready = threading.Event()

        def run_loop() -> None:
            self._async_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._async_loop)
            loop_ready.set()
            self._async_loop.run_forever()

        self._async_thread = threading.Thread(
            target=run_loop, daemon=True, name="KNX-Async"
        )
        self._async_thread.start()
        loop_ready.wait()
        return self._async_loop  # type: ignore

    def _run_async(self, coro: Coroutine[Any, Any, None]) -> None:
        loop = self._ensure_async_loop()
        asyncio.run_coroutine_threadsafe(coro, loop)

    def _load_saved_settings(self) -> None:
        data = load_settings(_SETTINGS)
        ip = data.get("controller_ip")
        if isinstance(ip, str) and ip:
            self._controller_ip = ip
        mcast = data.get("multicast_group")
        if isinstance(mcast, str) and mcast:
            self._multicast_group = mcast
        ctype = data.get("connection_type")
        if ctype is not None:
            with contextlib.suppress(ValueError):
                self._connection_type = ConnectionType(ctype)
        pref = data.get("preferred_gateway_ip")
        if isinstance(pref, str) and pref:
            self._preferred_gateway_ip = pref

    def _save_current_settings(self) -> None:
        save_settings(
            _SETTINGS,
            {
                "controller_ip": self._controller_ip,
                "multicast_group": self._multicast_group,
                "connection_type": self._connection_type.value,
                "preferred_gateway_ip": self._preferred_gateway_ip,
            },
        )

    def connect(self) -> None:
        """Manual IP connect (tunneling)."""
        if self._state in (ConnectionState.CONNECTING, ConnectionState.CONNECTED):
            return
        self._connection_type = ConnectionType.TUNNELING
        self._selected_gateway = None
        self._state = ConnectionState.CONNECTING
        self._error_message = None
        self._save_current_settings()
        self._run_async(self._connect_async())

    def connect_to_gateway(self, gateway: GatewayDescriptor) -> None:
        """Connect to a scanned gateway (tunneling preferred, routing fallback)."""
        if self._state in (ConnectionState.CONNECTING, ConnectionState.CONNECTED):
            return
        if gateway.supports_tunnelling:
            self._connection_type = ConnectionType.TUNNELING
            self._controller_ip = gateway.ip_addr
        else:
            self._connection_type = ConnectionType.ROUTING
            self._multicast_group = gateway.multicast_address or DEFAULT_MCAST_GRP
        self._selected_gateway = gateway
        self._preferred_gateway_ip = gateway.ip_addr
        self._state = ConnectionState.CONNECTING
        self._error_message = None
        self._save_current_settings()
        self._run_async(self._connect_async())

    @property
    def _connection_target(self) -> str:
        if self._connection_type == ConnectionType.ROUTING:
            return f"{self._multicast_group} (routing)"
        return self._controller_ip

    async def _connect_async(self) -> None:
        self._log.info(
            "connecting",
            target=self._connection_target,
            mode=self._connection_type.name.lower(),
        )
        try:
            self._xknx = XKNX()
            if self._connection_type == ConnectionType.ROUTING:
                config = ConnectionConfig(
                    connection_type=ConnectionType.ROUTING,
                    multicast_group=self._multicast_group,
                    threaded=True,
                )
            else:
                config = ConnectionConfig(
                    connection_type=ConnectionType.TUNNELING,
                    gateway_ip=self._controller_ip,
                    threaded=True,
                )
            self._interface = ObservableKNXIPInterfaceThreaded(
                xknx=self._xknx,
                connection_config=config,
                raw_cemi_callback=self._api.connection.dispatch_raw_cemi,
            )
            # Replace the inert default interface so all internal send paths use ours.
            self._xknx.knxip_interface = self._interface
            await self._interface.start()
            if self._selected_gateway is not None:
                self._gateway_info = self._selected_gateway
            elif self._connection_type == ConnectionType.TUNNELING:
                try:
                    self._gateway_info = await request_description(self._controller_ip)
                except Exception as desc_err:
                    self._gateway_info = None
                    self._log.debug(
                        "gateway description unavailable",
                        ip=self._controller_ip,
                        error=f"{type(desc_err).__name__}: {desc_err}",
                    )
            else:
                self._gateway_info = None
            self._state = ConnectionState.CONNECTED
            self._api.connection.set_connection(self._xknx, asyncio.get_running_loop())
            self._api.connection.dispatch_connected()
            self._log.info("connected", target=self._connection_target)
            if self._gateway_info:
                services = [
                    s
                    for s, enabled in [
                        ("tunneling", self._gateway_info.supports_tunnelling),
                        ("tunneling_tcp", self._gateway_info.supports_tunnelling_tcp),
                        ("routing", self._gateway_info.supports_routing),
                        ("secure", self._gateway_info.supports_secure),
                    ]
                    if enabled
                ]
                self._log.info(
                    "gateway info",
                    name=self._gateway_info.name,
                    knx_address=str(self._gateway_info.individual_address or ""),
                    core_version=str(self._gateway_info.core_version),
                    services=",".join(services),
                )
        except Exception as e:
            self._state = ConnectionState.ERROR
            self._error_message = str(e)
            self._interface = None
            self._gateway_info = None
            self._xknx = None
            self._log.error(
                "connection failed",
                target=self._connection_target,
                mode=self._connection_type.name.lower(),
                error=f"{type(e).__name__}: {e}",
            )

    def disconnect(self) -> None:
        if self._state in (ConnectionState.DISCONNECTED, ConnectionState.DISCONNECTING):
            return
        self._state = ConnectionState.DISCONNECTING
        self._run_async(self._disconnect_async())

    async def _disconnect_async(self) -> None:
        try:
            if self._interface is not None:
                await self._interface.stop()
        finally:
            self._interface = None
            self._gateway_info = None
            self._xknx = None
            self._state = ConnectionState.DISCONNECTED
            self._api.connection.set_connection(None, None)
            self._log.info("disconnected")

    def scan(self, auto_connect: bool = False) -> None:
        if self._scanning:
            return
        self._scanning = True
        self._run_async(self._scan_async(auto_connect))

    def autostart(self) -> None:
        """Discover gateways at startup and connect to the preferred (last-used) or first one."""
        if self._state != ConnectionState.DISCONNECTED:
            return
        self._log.info("auto-discovering gateways")
        self.scan(auto_connect=True)

    async def _scan_async(self, auto_connect: bool = False) -> None:
        try:
            xknx = XKNX()
            scanner = GatewayScanner(xknx, timeout_in_seconds=3.0)
            self._gateways = await scanner.scan()
            self._log.info("gateway scan complete", found=len(self._gateways))
            for g in self._gateways:
                self._log.debug(
                    "gateway found",
                    name=g.name,
                    ip=g.ip_addr,
                    knx_address=str(g.individual_address or ""),
                )
            if auto_connect and not self._gateways:
                self._log.warning("no gateways found on the network")
                if (
                    not self._autostart_retry_done
                    and self._state == ConnectionState.DISCONNECTED
                ):
                    # macOS: the first discovery only triggers the "Local Network" permission prompt
                    # and returns nothing. Retry once after a delay so a granted permission takes
                    # effect without restarting the app.
                    self._autostart_retry_done = True
                    self._run_async(self._delayed_rescan(_AUTOSTART_RETRY_SECONDS))
            if (
                auto_connect
                and self._gateways
                and self._state == ConnectionState.DISCONNECTED
            ):
                target = next(
                    (
                        g
                        for g in self._gateways
                        if g.ip_addr == self._preferred_gateway_ip
                    ),
                    self._gateways[0],
                )
                self._log.info(
                    "auto-connecting gateway",
                    name=target.name,
                    ip=target.ip_addr,
                    preferred=target.ip_addr == self._preferred_gateway_ip,
                )
                self.connect_to_gateway(target)
        except Exception as e:
            self._log.error("gateway scan failed", error=f"{type(e).__name__}: {e}")
        finally:
            self._scanning = False

    async def _delayed_rescan(self, delay: float) -> None:
        """Re-run autostart discovery once after ``delay`` seconds. Skips if the user connected or a
        scan is already running in the meantime. Runs on the async loop, so the wait never blocks the
        UI thread."""
        await asyncio.sleep(delay)
        if self._state != ConnectionState.DISCONNECTED or self._scanning:
            return
        self._log.info("retrying gateway discovery after delay", delay=delay)
        self._scanning = True
        await self._scan_async(auto_connect=True)

    def shutdown(self) -> None:
        if self._interface is not None:
            self._run_async(self._disconnect_async())
        if self._async_loop is not None:
            self._async_loop.call_soon_threadsafe(self._async_loop.stop)

    def render_status_indicator(self) -> None:
        draw_list = imgui.get_window_draw_list()
        cursor = imgui.get_cursor_screen_pos()
        text_height = imgui.get_text_line_height()
        center = imgui.ImVec2(cursor.x + 5, cursor.y + text_height / 2)

        if self._state == ConnectionState.CONNECTED:
            pulse = 0.5 + 0.5 * math.sin(imgui.get_time() * 3.0)
            alpha = 0.4 + 0.6 * pulse
            draw_list.add_circle_filled(center, 4, color_u32(0.2, 0.8, 0.3, alpha))
            draw_list.add_circle_filled(
                center, 4 + pulse * 3, color_u32(0.2, 0.8, 0.3, 0.15 * (1 - pulse))
            )
            imgui.dummy(imgui.ImVec2(12, 0))
            imgui.same_line()
            target = self._connection_target
            if self._gateway_info and self._gateway_info.name:
                name = "".join(
                    c for c in self._gateway_info.name if c.isprintable()
                ).strip()
                if name:
                    target = f"{name} @ {target}"
            imgui.text(S.STATUS_CONNECTED.format(ip=target))
        elif self._state == ConnectionState.CONNECTING:
            spin = (imgui.get_time() * 4) % 1.0
            draw_list.add_circle_filled(
                center, 4, color_u32(0.8, 0.7, 0.2, 0.5 + 0.5 * spin)
            )
            imgui.dummy(imgui.ImVec2(12, 0))
            imgui.same_line()
            imgui.text_disabled("Connecting...")
        elif self._state == ConnectionState.ERROR:
            draw_list.add_circle_filled(center, 4, color_u32(0.8, 0.2, 0.2, 1.0))
            imgui.dummy(imgui.ImVec2(12, 0))
            imgui.same_line()
            error_short = (
                self._error_message[:60] if self._error_message else "Unknown error"
            )
            imgui.text_colored(
                imgui.ImVec4(0.8, 0.2, 0.2, 1.0), f"Error: {error_short}"
            )
            if self._error_message and imgui.is_item_hovered():
                imgui.set_tooltip(self._error_message)
        else:
            draw_list.add_circle_filled(center, 4, color_u32(0.5, 0.5, 0.5, 1.0))
            imgui.dummy(imgui.ImVec2(12, 0))
            imgui.same_line()
            imgui.text_disabled(S.STATUS_DISCONNECTED)

    def _read_programming_mode_devices(self) -> None:
        """Diagnostics: read the individual addresses of devices currently in programming mode."""
        future = self._api.connection.read_programming_mode_devices()
        if future is None:
            return

        def _done(f: "Future[Any]") -> None:
            try:
                addresses = f.result()
            except Exception as e:  # bus timeout / not connected / xknx error
                self._log.error("programming-mode read failed", error=str(e))
                return
            self._log.info(
                "devices in programming mode",
                count=len(addresses),
                addresses=[str(a) for a in addresses],
            )

        future.add_done_callback(_done)

    def render_menu(self) -> None:
        if imgui.begin_menu(S.MENU_CONNECTION):
            if self._state == ConnectionState.CONNECTED:
                imgui.text(S.STATUS_CONNECTED_TO.format(ip=self._connection_target))
                if self._gateway_info:
                    imgui.separator()
                    imgui.text_disabled("Gateway")
                    imgui.text(f"  Name: {self._gateway_info.name}")
                    if self._gateway_info.individual_address:
                        imgui.text(
                            f"  KNX Address: {self._gateway_info.individual_address}"
                        )
                    imgui.text(f"  Core Version: {self._gateway_info.core_version}")
                    services = []
                    if self._gateway_info.supports_tunnelling:
                        services.append("Tunneling")
                    if self._gateway_info.supports_tunnelling_tcp:
                        services.append("TCP Tunneling")
                    if self._gateway_info.supports_routing:
                        services.append("Routing")
                    if self._gateway_info.supports_secure:
                        services.append("Secure")
                    if services:
                        imgui.text(f"  Services: {', '.join(services)}")
                imgui.separator()
                imgui.text_disabled(S.SECTION_DIAGNOSTICS)
                if imgui.menu_item(S.MENU_READ_PROGMODE, "", False)[0]:
                    self._read_programming_mode_devices()
                imgui.separator()
                if imgui.menu_item(S.MENU_DISCONNECT, "", False)[0]:
                    self.disconnect()
            elif self._state == ConnectionState.CONNECTING:
                imgui.text_disabled("Connecting...")
            elif self._state == ConnectionState.ERROR:
                imgui.text_colored(
                    imgui.ImVec4(0.8, 0.2, 0.2, 1.0), "Connection failed"
                )
                if self._error_message:
                    imgui.text_wrapped(self._error_message)
                imgui.separator()
                self._render_gateway_picker(retry_label="Retry")
            else:
                self._render_gateway_picker(retry_label=S.MENU_CONNECT)
            imgui.end_menu()

    def _render_gateway_picker(self, retry_label: str) -> None:
        if imgui.is_window_appearing() and not self._scanning:
            self.scan()

        imgui.text_disabled(S.SECTION_DISCOVERED)
        if self._scanning:
            imgui.same_line()
            imspinner.spinner_ang(
                "##scan-spinner",
                6,
                2,
                color=imgui.ImColor(
                    imgui.get_style_color_vec4(imgui.Col_.tab_selected)
                ),
            )
        if self._gateways:
            for gw in self._gateways:
                tags: list[str] = []
                if gw.supports_tunnelling:
                    tags.append("T")
                if gw.supports_routing:
                    tags.append("R")
                if gw.supports_secure:
                    tags.append("S")
                tag_str = "/".join(tags)
                label = f"{gw.name}  ({gw.ip_addr})" + (
                    f"  [{tag_str}]" if tag_str else ""
                )
                is_connected_to = (
                    self._state == ConnectionState.CONNECTED
                    and self._selected_gateway is not None
                    and self._selected_gateway.ip_addr == gw.ip_addr
                    and self._selected_gateway.port == gw.port
                )
                if imgui.menu_item(label, "", is_connected_to)[0]:
                    self.connect_to_gateway(gw)
        elif not self._scanning:
            imgui.text_disabled(S.NO_GATEWAYS_FOUND)

        imgui.separator()
        imgui.text_disabled(S.SECTION_MANUAL)
        imgui.set_next_item_width(180)
        _, self._controller_ip = imgui.input_text("IP##manual", self._controller_ip)
        if imgui.menu_item(retry_label, "", False)[0]:
            self.connect()

    @property
    def panels(self) -> list[PanelDefinition]:
        return self._panels

    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        self.shutdown()
