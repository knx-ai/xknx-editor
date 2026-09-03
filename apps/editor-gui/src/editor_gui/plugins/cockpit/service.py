"""Commissioning cockpit data: one row per project device with catalog + health status.

Rows are built from the live project and cached by the project revision, so the per-frame table
render never hits the database. "Attention" is derived from the shared health checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from editor_gui.plugins.cockpit.strings import S
from editor_gui.plugins.health.service import HealthService

if TYPE_CHECKING:
    from editor_gui.plugins.project.service import ProjectService
    from xknxmono.project.core.service import DeviceInfo


@dataclass
class CockpitRow:
    node_id: int
    individual_address: str
    name: str
    product_name: str
    order_number: str
    commissioning: str = ""  # short "loaded" label for the Loaded column
    commissioning_tooltip: str = ""  # per-flag detail + serial / last download
    issues: list[str] = field(default_factory=list[str])

    @property
    def needs_attention(self) -> bool:
        return bool(self.issues)


def _commissioning(info: DeviceInfo | None) -> tuple[str, str]:
    """Return a short "loaded" label and a detailed tooltip for a device's commissioning state."""
    if info is None:
        return "", ""
    flags = [
        (S.COCKPIT_LOADED_TOOLTIP_IA, info.individual_address_loaded),
        (S.COCKPIT_LOADED_TOOLTIP_APP, info.application_program_loaded),
        (S.COCKPIT_LOADED_TOOLTIP_COMM, info.communication_part_loaded),
        (S.COCKPIT_LOADED_TOOLTIP_MEDIUM, info.medium_config_loaded),
        (S.COCKPIT_LOADED_TOOLTIP_PARAMS, info.parameters_loaded),
    ]
    done = sum(1 for _, v in flags if v)
    if done == 0:
        label = S.COCKPIT_LOADED_NONE
    elif done == len(flags):
        label = S.COCKPIT_LOADED_FULL
    else:
        label = S.COCKPIT_LOADED_PARTIAL.format(done=done, total=len(flags))
    lines = [f"{'✓' if v else '·'} {name}" for name, v in flags]
    if info.serial_number:
        lines.append(S.COCKPIT_LOADED_TOOLTIP_SERIAL.format(serial=info.serial_number))
    if info.last_download:
        lines.append(
            S.COCKPIT_LOADED_TOOLTIP_LAST_DOWNLOAD.format(when=info.last_download)
        )
    return label, "\n".join(lines)


class CockpitService:
    def __init__(self, project: ProjectService) -> None:
        self._project = project
        self._health = HealthService(project)
        self._cache: list[CockpitRow] | None = None
        self._cache_revision = -1

    def skipped_count(self) -> int:
        """Devices dropped from the view because their application is not in the catalog."""
        return len(self._project.missing_program_refs())

    def rows(self) -> list[CockpitRow]:
        rev = self._project.revision
        if self._cache is None or self._cache_revision != rev:
            self._cache = self._build()
            self._cache_revision = rev
        return self._cache

    def _build(self) -> list[CockpitRow]:
        if not self._project.is_open:
            return []
        by_device: dict[int, list[str]] = {}
        for f in self._health.findings():
            if f.device_node_id is not None:
                by_device.setdefault(f.device_node_id, []).append(f.message)
        rows: list[CockpitRow] = []
        for d in self._project.devices:
            info = self._project.get_device_info(d.node_id)
            label, tooltip = _commissioning(info)
            rows.append(
                CockpitRow(
                    node_id=d.node_id,
                    individual_address=d.individual_address or "",
                    name=d.name,
                    product_name=info.product_name if info else "",
                    order_number=info.order_number if info else "",
                    commissioning=label,
                    commissioning_tooltip=tooltip,
                    issues=by_device.get(d.node_id, []),
                )
            )
        return rows
