"""Recover plugin: reconstruct a project by reading devices off the bus.

The recover view is a dockable panel that opens next to the Topology view (the
``MainDockSpace`` dock). A menu-bar entry next to Help (and the welcome card's
Recover button) focus it. It scans an address range, identifies each device
against the catalog, reads it back, and adds the recovered devices to a project."""

from imgui_bundle import imgui

from editor_gui.plugins.base import Logger, PanelDefinition, PluginAPI
from editor_gui.plugins.recover.service import RecoverService
from editor_gui.plugins.recover.strings import S
from editor_gui.plugins.recover.ui import RecoverPanel


class RecoverPlugin:
    name = "recover"

    def __init__(self, api: PluginAPI) -> None:
        self._api = api
        self._service = RecoverService(api)
        self._service.set_logger(Logger(api.log, "recover"))
        self._panel = RecoverPanel(self._service)

    @property
    def panels(self) -> list[PanelDefinition]:
        # Docked next to the topology/devices tree, not a floating window.
        return [
            PanelDefinition(
                name="recover",
                label=S.WINDOW_TITLE,
                dock="MainDockSpace",
                render=self._panel.render,
            )
        ]

    def render_menu(self) -> None:
        """The 'Recover' menu-bar entry (next to Help) focuses the docked panel."""
        if imgui.begin_menu(S.MENU_RECOVER):
            if imgui.menu_item(S.MENU_OPEN_WINDOW, "", False)[0]:
                self._panel.request_focus()
            imgui.end_menu()

    def open_window(self) -> None:
        """Focus the recover panel (used by the welcome screen's Recover button)."""
        self._panel.request_focus()

    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass
