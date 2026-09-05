"""Cockpit plugin: a site-wide commissioning overview docked in the main area."""

from editor_gui.plugins.base import PanelDefinition, PluginAPI
from editor_gui.plugins.cockpit.service import CockpitService
from editor_gui.plugins.cockpit.strings import S
from editor_gui.plugins.cockpit.ui import CockpitPanel


class CockpitPlugin:
    name = "cockpit"

    def __init__(self, api: PluginAPI) -> None:
        self._api = api
        self._service = CockpitService(api.project)
        self._panel = CockpitPanel(
            service=self._service,
            on_select=self._select,
            is_open=lambda: api.project.is_open,
        )
        self._panels = [
            PanelDefinition(
                name="cockpit",
                label=S.PANEL_COCKPIT,
                dock="MainDockSpace",
                render=self._panel.render,
            ),
        ]

    def _select(self, node_id: int) -> None:
        device = self._api.project.find_device_by_node_id(node_id)
        if device is not None:
            self._api.project.selected_device = device
            self._api.project.focus_editor()

    @property
    def panels(self) -> list[PanelDefinition]:
        return self._panels

    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass
