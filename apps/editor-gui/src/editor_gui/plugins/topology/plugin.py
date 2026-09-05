"""Topology plugin: a layered Area -> Line -> Device map docked in the main area."""

from editor_gui.plugins.base import PanelDefinition, PluginAPI
from editor_gui.plugins.topology.strings import S
from editor_gui.plugins.topology.ui import TopologyPanel


class TopologyPlugin:
    name = "topology"

    def __init__(self, api: PluginAPI) -> None:
        self._api = api
        self._panel = TopologyPanel(
            get_devices=lambda: api.project.devices,
            get_space_tree=api.project.get_space_tree,
            on_select=self._select,
            is_open=lambda: api.project.is_open,
        )
        self._panels = [
            PanelDefinition(
                name="topology",
                label=S.PANEL_TOPOLOGY,
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
