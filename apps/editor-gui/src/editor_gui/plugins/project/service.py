"""The GUI project facade, backed by :class:`xknxmono.project.ProjectService`.

Persistence + undo/redo live in the project package (one open project). This adapter keeps the GUI
concerns: the rich in-memory ``Device`` view (resolved ``Application``, com-objects, parameter
visibility), the selection, and the pub/sub. Project state is read live from the service; only the
resolved ``Application`` is cached (the expensive part), and the device view is rebuilt lazily when
a version counter changes — so there is no reload-from-db: every edit (and undo/redo) just bumps the
version, and the next read rebuilds.
"""

import os
import shutil
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from editor_gui.concurrency import io_guarded
from editor_gui.device import Device
from editor_gui.plugins.project.ui.history import HistoryEntry
from xknxmono.models.intermediate import ComObjectInstanceRef
from xknxmono.models.intermediate.enable_t import Enable
from xknxmono.product import Application
from xknxmono.product.app_id import parse_app_id
from xknxmono.project import ProjectService as _ProjectService
from xknxmono.project import import_knxproj as _import_knxproj
from xknxmono.project.core.addressing import GroupAddressStyle, parse_ga

if TYPE_CHECKING:
    from editor_gui.plugins.base import Logger
    from editor_gui.plugins.catalog.service import CatalogService
    from xknxmono.catalog import ProductSummary
    from xknxmono.download.image import GroupCommunication
    from xknxmono.project.core.service import (
        DeviceInfo,
        GroupRangeInfo,
        SpaceDeviceInfo,
        SpaceInfo,
    )

_INSTALLATION = 0


@dataclass(frozen=True)
class UpdateApplicationResult:
    """Outcome of an ETS-style application update: the version updated to and how many parameter/
    com-object rows carried over vs were dropped as incompatible."""

    new_version: int
    kept: int
    dropped: int


# GUI flag name -> project ComObject column
_FLAG_COLUMNS: dict[str, str] = {
    "communication": "communication_flag",
    "read": "read_flag",
    "write": "write_flag",
    "transmit": "transmit_flag",
    "update": "update_flag",
    "read_on_init": "read_on_init_flag",
}


def _parse_individual_address(text: str) -> int | None:
    """Parse ``area.line.device`` into a raw 16-bit individual address."""
    parts = text.split(".")
    if len(parts) != 3:
        return None
    try:
        area, line, device = (int(p) for p in parts)
    except ValueError:
        return None
    if not (0 <= area <= 0xF and 0 <= line <= 0xF and 0 <= device <= 0xFF):
        return None
    return (area << 12) | (line << 8) | device


def _parse_group_address(text: str) -> int | None:
    """Parse a 3-level (``a/b/c``), 2-level (``a/b``) or free group address into a raw value."""
    parts = text.split("/")
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        return None
    if len(nums) == 3:
        return (nums[0] << 11) | (nums[1] << 8) | nums[2]
    if len(nums) == 2:
        return (nums[0] << 11) | nums[1]
    if len(nums) == 1:
        return nums[0]
    return None


def _co_instance_ref_from_row(row: Any) -> ComObjectInstanceRef | None:
    def _e(v: bool | None) -> Enable | None:
        return None if v is None else (Enable.ENABLED if v else Enable.DISABLED)

    if all(
        getattr(row, col) is None
        for col in (
            "communication_flag",
            "read_flag",
            "write_flag",
            "transmit_flag",
            "update_flag",
            "read_on_init_flag",
        )
    ):
        return None
    return ComObjectInstanceRef(
        ref_id=row.ref_id,
        communication_flag=_e(row.communication_flag),
        read_flag=_e(row.read_flag),
        write_flag=_e(row.write_flag),
        transmit_flag=_e(row.transmit_flag),
        update_flag=_e(row.update_flag),
        read_on_init_flag=_e(row.read_on_init_flag),
    )


def _history_device_id(data: dict[str, Any]) -> int | None:
    """The device id an undone/redone event touched — for a ``SyncDeviceComObjects`` (``device_id``)
    or a ``Composite`` (from the first sub-event that carries one), so only that device is rebuilt."""
    if "device_id" in data:
        try:
            return int(data["device_id"])
        except (TypeError, ValueError):
            return None
    for sub in data.get("events", []):
        node_id = _history_device_id(sub.get("data", {}))
        if node_id is not None:
            return node_id
    return None


def _history_label(event_type: str, data: dict[str, Any]) -> str:
    """Render a command's history label (presentation lives in the GUI, not the project package)."""
    if event_type == "AddDevice":
        return f"Add device {data.get('name', '')!r}"
    if event_type == "SetParameter":
        return f"Set {data.get('ref_id', '')} = {data.get('value', '')!r}"
    if event_type == "Composite":
        # A composite is a parameter change plus the com-object re-instantiation it triggered; label
        # it by its first sub-event (the SetParameter) so the history reads naturally.
        for sub in data.get("events", []):
            if sub.get("data"):
                return _history_label(str(sub.get("type", "")), sub["data"])
        return "Change"
    if event_type == "CreateArea":
        return f"Create area {data.get('address')}"
    if event_type == "CreateLine":
        return f"Create line {data.get('address')}"
    if event_type == "CreateSegment":
        return "Add segment"
    if event_type == "CreateGroupAddress":
        return f"Create group address {data.get('address')}"
    if event_type == "LinkComObject":
        return "Link com-object"
    if event_type == "UnlinkComObject":
        return "Unlink com-object"
    if event_type == "RenameArea":
        return f"Rename area to {data.get('name', '')!r}"
    if event_type == "RenameLine":
        return f"Rename line to {data.get('name', '')!r}"
    if event_type == "SetDeviceName":
        return f"Rename device to {data.get('name', '')!r}"
    if event_type == "MoveDevice":
        return "Move device"
    if event_type == "SetComObjectFlag":
        return "Set flag"
    if event_type == "SetComObjectSending":
        return "Set sending"
    if event_type == "SetGroupAddressDatapointType":
        return "Set datapoint type"
    if event_type.startswith("Remove"):
        return f"Remove {event_type[len('Remove') :].lower()}"
    if event_type == "AddInstallation":
        return "Add installation"
    return event_type


@dataclass
class _Area:
    id: int
    area_number: int
    name: str


@dataclass
class _Line:
    id: int
    area_id: int
    line_number: int
    name: str


@dataclass
class _GroupAddress:
    id: int
    address: str
    name: str
    datapoint_type: str | None = None
    description: str = ""
    comment: str = ""
    data_secure: bool = False
    raw: int = 0  # raw 16-bit group-address value (style-independent; matches xknx GroupAddress.raw)


@dataclass
class _ProjectInfo:
    id: str
    name: str
    group_address_style: str
    guid: str
    created_by: str
    last_modified: str
    schema_version: str
    tool_version: str
    # ETS protection artifacts carried over from the imported .knxproj (shown as presence/size,
    # not raw dumps): the source project id the certificate is bound to, the signed master data,
    # the ".validation" file and the "<pid>.certificate".
    original_project_id: str = ""
    master_data_size: int = 0
    validation_size: int = 0
    certificate_size: int = 0


@dataclass
class _Assignment:
    id: int
    com_object_id: int
    group_address_id: int
    is_sending: bool


class ProjectService:
    def __init__(self, catalog: "CatalogService") -> None:
        self._catalog = catalog
        # Share the catalog's re-entrant lock: a background import holds it while writing both stores.
        self._io_lock = catalog.io_lock
        self._svc = _ProjectService()
        self._pid: str | None = None
        self._path: Path | None = None
        self._log: Logger
        self._listeners: dict[str, list[Callable[..., Any]]] = {}
        self._app_cache: dict[str, Application] = {}
        self._program_to_app: dict[str, str] | None = None
        # Signature of the non-reverted events at open — the baseline the read-only pre-flight
        # compares against, so opening a previously-edited project is not itself "modified".
        self._history_baseline: frozenset[tuple[int, str, str]] = frozenset()
        # Optional (i_done, total) callback invoked while (re)building the device views — lets the
        # GUI show a determinate "opening project" progress bar sized to the project's device count.
        self.build_progress: Callable[[int, int, str], None] | None = None
        self._devices_cache: list[Device] | None = None
        self._areas_cache: list[_Area] | None = None
        self._lines_cache: dict[int, list[_Line]] | None = None
        self._ga_cache: list[_GroupAddress] | None = None
        # Each lazy cache tracks the project version it was built at, independently. A single shared
        # counter is wrong: after an edit only the first cache read would rebuild (and stamp the
        # shared version), leaving the others returning stale data until the next edit.
        self._devices_cache_version: int = -1
        self._topology_cache_version: int = -1
        self._ga_cache_version: int = -1
        self._version: int = 0
        self._selected_node_id: int | None = None
        # ETS-style multi-selection: the full set of selected device node ids (the primary above is
        # the last-clicked one, kept for all single-device consumers). Empty = single/none.
        self._selected_node_ids: set[int] = set()
        # Recently-viewed devices whose heavy DynamicUI we keep resident (MRU first), so toggling
        # between a few devices is instant instead of re-parsing each time. Older ones are released.
        self._dynui_lru: list[int] = []
        self._dynui_keep = 3
        # Cross-panel "please select this group address" request (consumed by the GA panel).
        self._requested_ga_id: int | None = None
        # Cross-panel "please bring the editor tab to front" request (consumed by the editor panel).
        self._focus_editor_requested = False
        # Re-instantiate a device's persisted com-objects on a function/mode parameter change, scoped
        # to exactly the objects that parameter controls (its ChooseWhenNode branches). Only the
        # objects the parameter governs are added/removed; channels and globals stay as configured.
        # (An earlier blanket before/after diff of the whole unpruned set was destructive — it
        # over-activated all channels and removed real objects; the scoped diff in
        # _reconcile_com_objects avoids that.)
        self._co_reconcile_enabled = True

    def set_logger(self, log: "Logger") -> None:
        self._log = log

    # --- pub/sub ----------------------------------------------------------

    def subscribe(self, event: str, handler: Callable[..., Any]) -> Callable[[], None]:
        self._listeners.setdefault(event, []).append(handler)
        return lambda: self._listeners[event].remove(handler)

    def _emit(self, event: str, *args: Any) -> None:
        for handler in list(self._listeners.get(event, [])):
            handler(*args)

    # --- lifecycle --------------------------------------------------------

    @property
    def is_open(self) -> bool:
        return self._pid is not None

    @property
    def path(self) -> Path | None:
        return self._path

    @staticmethod
    def _remove_project_file(path: Path) -> None:
        """Delete a project's SQLite file and its DELETE-mode ``-journal`` sidecar, so a fresh create
        never seeds into a leftover database (a stale sidecar over a new db also corrupts it)."""
        path.unlink(missing_ok=True)
        Path(f"{path}-journal").unlink(missing_ok=True)

    def new(self, path: Path) -> None:
        if self._pid is not None:
            self.close()
        if not path.suffix:
            path = path.with_suffix(".xknx")
        # New project = a fresh file. The save dialog lets the user pick an existing path to
        # overwrite; without clearing it, create()'s seed collides with the old project's rows
        # ("UNIQUE constraint failed: installations.index").
        self._remove_project_file(path)
        self._pid = self._svc.create(path)
        self._path = path
        self._reset()
        self._log.info("project created", path=str(path))

    def save_as(self, new_path: Path) -> Path | None:
        """Save the open project to ``new_path`` and continue there (ETS-style "Save as").

        The project persists to its .xknx file continuously (event-sourced), so this snapshots the
        current file to the chosen location and re-opens it there — how an auto-named "untitled"
        project (created when the Welcome screen is closed) gets a real, user-chosen home. Returns the
        final path (``.xknx`` suffix ensured), or ``None`` when no project is open."""
        if self._pid is None or self._path is None:
            return None
        if not new_path.suffix:
            new_path = new_path.with_suffix(".xknx")
        with self._io_lock:
            src = self._path
            # Close first to release the SQLite file (DELETE journal, no open txn), copy the fully
            # persisted document, then open the copy so edits continue against the new location.
            self._svc.close(self._pid)
            self._pid = None
            self._path = None
            self._reset()
            # Overwriting an existing target: drop its stale -journal so the copied db is not paired
            # with a foreign rollback journal.
            Path(f"{new_path}-journal").unlink(missing_ok=True)
            shutil.copyfile(src, new_path)
        self.open(new_path)
        self._log.info("project saved as", path=str(new_path))
        return new_path

    def open(self, path: Path) -> None:
        # Hold the shared lock for the whole open (incl. the device-view build) so per-frame UI reads
        # on other threads bail to empty placeholders instead of racing it — lets a background open
        # run behind a progress spinner. Re-entrant, so our own nested reads still work.
        with self._io_lock:
            # Open (and thereby validate) the target BEFORE closing the current project, so a
            # corrupt/invalid file leaves the existing project intact instead of stranding the user.
            self._log.debug("opening project", path=str(path))
            new_pid = self._svc.open(path)
            # Re-opening the same file yields the same pid; closing it then would drop the project we
            # just opened, so only close the previous one when it is a different project.
            if self._pid is not None and self._pid != new_pid:
                self._svc.close(self._pid)
            self._pid = new_pid
            self._path = path
            self._reset()
            self._history_baseline = self._history_key()
            self._log.info("project opened", path=str(path), devices=len(self.devices))

    def import_knxproj(
        self, source: Path, dest: Path, *, password: str | None = None
    ) -> None:
        """Import an ETS ``.knxproj`` into a new project at ``dest`` and open it.

        A ``.knxproj`` bundles the (unencrypted) manufacturer/application data for the products it
        uses, so we also ingest it into the catalog — without it the device view cannot resolve the
        applications and would skip every imported device.

        The parse-and-write goes into a sibling temp file the live service never references, so the
        whole schema build/DDL happens off to the side; only once it is complete do we close any
        engine on ``dest``, atomically ``os.replace`` the temp into place, and open it. This is what
        keeps a re-import safe: we never rewrite the file under an open SQLite connection, and the UI
        keeps reading the previous project (stable, no schema mutation) until the swap."""
        if not dest.suffix:
            dest = dest.with_suffix(".xknx")
        # Hold the shared lock for the whole import so per-frame UI reads on other threads bail to
        # empty placeholders (see editor_gui.concurrency) instead of racing these writes. This method is
        # meant to run on a worker thread; the lock is re-entrant, so our own nested reads still work.
        with self._io_lock:
            self._log.debug(
                "importing knxproj",
                source=str(source),
                dest=str(dest),
                encrypted=password is not None,
            )
            try:
                added = self._catalog.import_knxprod(source)
                self._log.info("catalog updated from knxproj", added=len(added))
            except Exception as e:
                # Best effort: catalog ingest is optional enrichment (it lets the device view resolve
                # applications). Any failure here — including product-parser bugs on odd archives —
                # must not block the project import; topology and group addresses still load.
                self._log.warning(
                    "could not populate catalog from knxproj",
                    source=str(source),
                    error=f"{type(e).__name__}: {e}",
                )
            tmp = dest.with_name(f"{dest.name}.import-{os.getpid()}.tmp")
            try:
                # Parse + write into the temp file. On a wrong password this raises before writing,
                # so the currently-open project is left untouched.
                _import_knxproj(source, tmp, password=password)
                # If we are overwriting the file the live service currently has open, close it first
                # so no engine holds dest's inode when we replace it (old-inode/new-file + pooled-
                # connection hazard). A different dest needs no early close — open() closes the old
                # project after the swap.
                if (
                    self._pid is not None
                    and self._path is not None
                    and self._path.resolve() == dest.resolve()
                ):
                    self._svc.close(self._pid)
                    self._pid = None
                    self._path = None
                    self._reset()
                os.replace(tmp, dest)
            finally:
                # Clean up the temp file if it survived a failure (a successful replace consumed it).
                Path(tmp).unlink(missing_ok=True)
            self.open(dest)
        self._log.info("project imported", source=str(source), path=str(dest))

    def close(self) -> None:
        if self._pid is not None:
            self._svc.close(self._pid)
            self._pid = None
            self._path = None
            self._reset()
            self._history_baseline = frozenset()
            self._log.info("project closed")

    def _reset(self) -> None:
        self._devices_cache = None
        self._areas_cache = None
        self._lines_cache = None
        self._ga_cache = None
        self._devices_cache_version = -1
        self._topology_cache_version = -1
        self._ga_cache_version = -1
        self._version = 0
        self._selected_node_id = None
        self._selected_node_ids = set()
        self._dynui_lru.clear()
        self._app_cache.clear()
        self._program_to_app = None

    def _bump(self, *, structural: bool = True) -> None:
        """Advance the revision so views refresh. ``structural=False`` for edits that don't change
        device structure (group-address/link changes): the expensive device cache — each device
        rebuild re-parses its application's dynamic UI — is kept valid instead of being discarded,
        so linking a group address stays instant on large projects."""
        self._version += 1
        if not structural and self._devices_cache is not None:
            self._devices_cache_version = self._version

    def _refresh_device(self, node_id: int) -> None:
        """Rebuild a single device's cached view in place (its com-objects changed), instead of
        discarding the whole device cache. A full structural rebuild re-evaluates every device's
        DynamicUI (``_build_device`` warms it per device), which is very slow on large projects; a
        function/mode change only affects the one edited device, so refresh just that entry. Caller
        bumps the revision."""
        if self._pid is None or self._devices_cache is None:
            return
        row = next((r for r in self._svc.devices(self._pid) if r.id == node_id), None)
        if row is None:
            return
        rebuilt = self._build_device(row)
        if rebuilt is None:
            return
        for i, d in enumerate(self._devices_cache):
            if d.node_id == node_id:
                self._devices_cache[i] = rebuilt
                return

    @property
    def revision(self) -> int:
        """Monotonic counter bumped on every edit/undo/redo — for cheap change detection."""
        return self._version

    # --- application resolution + device view -----------------------------

    def _resolve_app(self, program_ref: str | None) -> Application | None:
        if program_ref is None:
            return None
        cached = self._app_cache.get(program_ref)
        if cached is not None:
            return cached
        if self._program_to_app is None:
            self._program_to_app = {
                p.hardware2program_ref_id: p.application_id
                for p in self._catalog.get_products()
                if p.application_id is not None
            }
        app_id = self._program_to_app.get(program_ref)
        app = self._catalog.get_application(app_id) if app_id else None
        if app is not None:
            self._app_cache[program_ref] = app
        return app

    def _build_device(self, row: Any) -> Device | None:
        try:
            app = self._resolve_app(row.hardware2program_ref_id)
        except Exception as e:
            # A broken/unsupported .knxprod (bad application XML) must not abort loading the whole
            # project — report it in the log and skip just this device.
            self._log.error(
                "failed to load device application (broken product data?)",
                device_id=row.id,
                name=row.name,
                program=row.hardware2program_ref_id,
                error=f"{type(e).__name__}: {e}",
            )
            return None
        if app is None:
            self._log.warning(
                "skipping device: application not found",
                device_id=row.id,
                program=row.hardware2program_ref_id,
            )
            return None
        assert self._pid is not None
        from xknxmono.models.intermediate import ParameterInstanceRef as _PIR
        from xknxmono.models.intermediate.module_instance_t import ModuleInstance as _MI

        try:
            pirs = [_PIR(ref_id=p.ref_id, value=p.value) for p in row.parameters]
            mis = [
                _MI(id=mi.instance_id, ref_id=mi.ref_id) for mi in row.module_instances
            ]
            # Every persisted ComObject row is an instantiated object (that is what pins the device's
            # object set against the parser's channel over-activation). Seed one instance ref per row
            # — with its flag overrides where present, else a bare ref — so objects added by a
            # function/mode re-instantiation (default, i.e. all-None, flags) are also counted as
            # instantiated and thus shown/encoded rather than pruned away.
            coirs = [
                _co_instance_ref_from_row(co_row)
                or ComObjectInstanceRef(ref_id=co_row.ref_id)
                for co_row in row.com_objects
            ]
            ia = self._svc.individual_address(self._pid, row.id) or ""
            device = Device(
                node_id=row.id,
                name=row.name,
                app=app,
                individual_address=ia,
                parameter_instance_refs=pirs,
                module_instances=mis,
                com_object_instance_refs=coirs,
            )
            for co_row in row.com_objects:
                co = device.find_com_object(co_row.ref_id)
                if co is not None:
                    co.db_id = co_row.id
            # Warm the lightweight views the panels read for every device, then drop the heavy
            # per-device DynamicUI evaluator (~15 MB each) — it is rebuilt lazily only when a device
            # is inspected or edited. This keeps memory bounded to the active device.
            device.get_visible_com_objects()
            device.release_dynamic_ui()
            return device
        except Exception as e:
            # Building the device (evaluating its dynamic UI from the .knxprod) failed — log the
            # product/device and skip it rather than crashing the editor.
            self._log.error(
                "failed to build device from product data",
                device_id=row.id,
                name=row.name,
                program=row.hardware2program_ref_id,
                error=f"{type(e).__name__}: {e}",
            )
            return None

    @property
    @io_guarded(list)
    def devices(self) -> list[Device]:
        if self._devices_cache is None or self._devices_cache_version != self._version:
            devices: list[Device] = []
            if self._pid is not None:
                rows = list(self._svc.devices(self._pid))
                total = len(rows)
                report = self.build_progress
                for i, row in enumerate(rows, start=1):
                    device = self._build_device(row)
                    if device is not None:
                        devices.append(device)
                    if report is not None:
                        label = (
                            f"{device.individual_address}  {device.name}".strip()
                            if device is not None
                            else (row.name or "")
                        )
                        report(i, total, label)
            self._devices_cache = devices
            self._devices_cache_version = self._version
        return self._devices_cache

    def find_device_by_node_id(self, node_id: int) -> Device | None:
        return next((d for d in self.devices if d.node_id == node_id), None)

    def find_device_by_address(self, address: str) -> Device | None:
        return next((d for d in self.devices if d.individual_address == address), None)

    @property
    def selected_device(self) -> Device | None:
        if self._selected_node_id is None:
            return None
        return self.find_device_by_node_id(self._selected_node_id)

    @selected_device.setter
    def selected_device(self, device: Device | None) -> None:
        new_id = device.node_id if device is not None else None
        if new_id != self._selected_node_id:
            self._selected_node_id = new_id
            # Any single-device select (command palette, Health/Cockpit navigate) collapses the
            # multi-selection to just this device; set_multi_selection re-widens it afterwards.
            self._selected_node_ids = {new_id} if new_id is not None else set[int]()
            # Keep the few most-recently-viewed devices' DynamicUI resident (instant toggling);
            # release those that fall out of the small LRU (no-op if they have unsaved edits).
            if new_id is not None:
                if new_id in self._dynui_lru:
                    self._dynui_lru.remove(new_id)
                self._dynui_lru.insert(0, new_id)
                for evicted in self._dynui_lru[self._dynui_keep :]:
                    dev = self.find_device_by_node_id(evicted)
                    if dev is not None:
                        dev.release_dynamic_ui()
                del self._dynui_lru[self._dynui_keep :]
            self._emit("device_selected", device)

    @property
    def selected_node_ids(self) -> set[int]:
        """The full multi-selection (device node ids); empty when a single/no device is selected."""
        return set(self._selected_node_ids)

    def set_multi_selection(self, primary_id: int | None, node_ids: list[int]) -> None:
        """Set the selection set and its primary (the device the single-device panels track). The
        primary is forced into the set; an empty selection clears everything."""
        ids = set(node_ids)
        if primary_id is not None and primary_id not in ids:
            primary_id = None
        if primary_id is None and ids:
            primary_id = min(ids)
        # Assign the primary first (the setter collapses _selected_node_ids to {primary}), then
        # widen to the full multi-selection set.
        self.selected_device = (
            self.find_device_by_node_id(primary_id) if primary_id is not None else None
        )
        self._selected_node_ids = ids

    def request_group_address(self, ga_id: int) -> None:
        """Ask the Group Addresses panel to select ``ga_id`` (cross-panel navigation, e.g. Health)."""
        self._requested_ga_id = ga_id

    def take_requested_group_address(self) -> int | None:
        """One-shot: the pending externally-requested group-address selection, then cleared."""
        ga_id = self._requested_ga_id
        self._requested_ga_id = None
        return ga_id

    def focus_editor(self) -> None:
        """Ask the editor tab to come to the front (after selecting a device from another view)."""
        self._focus_editor_requested = True

    def take_focus_editor(self) -> bool:
        """One-shot: whether the editor tab was asked to focus, then cleared."""
        requested = self._focus_editor_requested
        self._focus_editor_requested = False
        return requested

    # --- topology reads ---------------------------------------------------

    def _installation(self) -> Any:
        assert self._pid is not None
        return self._svc.topology(self._pid, _INSTALLATION)

    def _ensure_topology_cache(self) -> None:
        if (
            self._areas_cache is not None
            and self._topology_cache_version == self._version
        ):
            return
        if self._pid is None:
            self._areas_cache = []
            self._lines_cache = {}
            return
        installation = self._svc.topology(self._pid, _INSTALLATION)
        self._areas_cache = [
            _Area(id=a.id, area_number=a.address, name=a.name)
            for a in installation.areas
        ]
        self._lines_cache = {
            a.id: [
                _Line(
                    id=ln.id, area_id=ln.area_id, line_number=ln.address, name=ln.name
                )
                for ln in a.lines
            ]
            for a in installation.areas
        }
        self._topology_cache_version = self._version

    @io_guarded(list)
    def get_areas(self) -> list[_Area]:
        if self._pid is None:
            return []
        self._ensure_topology_cache()
        return self._areas_cache or []

    @io_guarded(list)
    def get_lines(self, area_id: int) -> list[_Line]:
        if self._pid is None:
            return []
        self._ensure_topology_cache()
        return (self._lines_cache or {}).get(area_id, [])

    # --- group address reads ----------------------------------------------

    @property
    @io_guarded(list)
    def group_addresses(self) -> list[_GroupAddress]:
        if self._pid is None:
            return []
        if self._ga_cache is not None and self._ga_cache_version == self._version:
            return self._ga_cache
        self._ga_cache = [
            _GroupAddress(
                id=g.id,
                address=g.text,
                name=g.name,
                datapoint_type=g.datapoint_type,
                description=g.description,
                comment=g.comment,
                data_secure=g.data_secure,
                raw=g.address,
            )
            for g in self._svc.group_addresses(self._pid)
        ]
        self._ga_cache_version = self._version
        return self._ga_cache

    @io_guarded(lambda: None)
    def get_group_address(self, ga_id: int) -> _GroupAddress | None:
        if self._pid is None:
            return None
        try:
            g = self._svc.group_address(self._pid, ga_id)
        except KeyError:
            return None
        return _GroupAddress(
            id=g.id,
            address=g.text,
            name=g.name,
            datapoint_type=g.datapoint_type,
            description=g.description,
            comment=g.comment,
            data_secure=g.data_secure,
            raw=g.address,
        )

    @io_guarded(list)
    def get_assignments_for_ga(self, ga_id: int) -> list[_Assignment]:
        if self._pid is None:
            return []
        return [
            _Assignment(
                id=link.id,
                com_object_id=link.com_object_id,
                group_address_id=link.group_address_id,
                is_sending=link.is_sending,
            )
            for link in self._svc.group_address_links(self._pid, ga_id)
        ]

    @io_guarded(list)
    def get_links_for_com_object(self, com_object_db_id: int) -> list[_Assignment]:
        """A device com-object's group-address links (the per-com-object direction, for the editor's
        Group Objects view). ``com_object_db_id`` is ``ComObject.db_id``."""
        if self._pid is None:
            return []
        return [
            _Assignment(
                id=link.id,
                com_object_id=link.com_object_id,
                group_address_id=link.group_address_id,
                is_sending=link.is_sending,
            )
            for link in self._svc.com_object_links(self._pid, com_object_db_id)
        ]

    def group_communication_for(self, device: Device) -> "GroupCommunication | None":
        """Collect a device's group-address links into a :class:`GroupCommunication` for programming.

        Returns ``None`` when the device has no (parseable) individual address. Used by both the GUI
        download flow and the embedded MCP server so both program identical address/association data.
        """
        from xknxmono.download import GroupCommunication
        from xknxmono.download.project_data import GroupObjectLink

        device_address = _parse_individual_address(device.individual_address)
        if device_address is None:
            return None
        links: list[GroupObjectLink] = []
        for com_object in device.com_objects:
            if com_object.db_id is None:
                continue
            for assignment in self.get_links_for_com_object(com_object.db_id):
                ga = self.get_group_address(assignment.group_address_id)
                if ga is None:
                    continue
                address = _parse_group_address(ga.address)
                if address is None:
                    continue
                links.append(
                    GroupObjectLink(
                        com_object_ref_id=com_object.id,
                        group_address=address,
                        sending=assignment.is_sending,
                    )
                )
        # A line/backbone coupler (address x.y.0) also carries a group-address filter table computed
        # from the whole topology (which group addresses cross it). A non-coupler at .0 gets one too,
        # but its load procedure has no Router-object write, so the extra image segment is unused.
        from xknxmono.download.filter_table import (
            compute_coupler_filter_table,
            is_coupler_address,
        )

        filter_table = (
            compute_coupler_filter_table(
                device_address, self._all_device_group_addresses()
            )
            if is_coupler_address(device_address)
            else None
        )
        return GroupCommunication(
            device_address=device_address, links=links, filter_table=filter_table
        )

    def _all_device_group_addresses(self) -> dict[int, set[int]]:
        """Map every device's raw individual address to the raw group addresses it links (send or
        receive). The coupler filter-table computation uses this to decide which addresses cross a
        coupler (linked both behind it and in front of it)."""
        result: dict[int, set[int]] = {}
        for dev in self.devices:
            ia = _parse_individual_address(dev.individual_address)
            if ia is None:
                continue
            gas: set[int] = set()
            for co in dev.com_objects:
                if co.db_id is None:
                    continue
                for assignment in self.get_links_for_com_object(co.db_id):
                    ga = self.get_group_address(assignment.group_address_id)
                    if ga is None:
                        continue
                    raw = _parse_group_address(ga.address)
                    if raw is not None:
                        gas.add(raw)
            result[ia] = gas
        return result

    @io_guarded(list)
    def get_group_range_tree(self) -> list["GroupRangeInfo"]:
        """The named group-address range tree (roots → children → GAs) for the GA view."""
        if self._pid is None:
            return []
        return self._svc.group_ranges(self._pid, _INSTALLATION)

    @io_guarded(list)
    def get_space_tree(self) -> list["SpaceInfo"]:
        """The building/location tree (spaces → devices/functions) for the Buildings view."""
        if self._pid is None:
            return []
        return self._svc.space_tree(self._pid, _INSTALLATION)

    @io_guarded(lambda: None)
    def get_project_metadata(self) -> _ProjectInfo | None:
        """Project-level metadata (name, author, tool/schema version, …) from the imported project."""
        if self._pid is None:
            return None
        p = self._svc.project(self._pid)
        return _ProjectInfo(
            id=p.id,
            name=p.name,
            group_address_style=p.group_address_style,
            guid=p.guid,
            created_by=p.created_by,
            last_modified=p.last_modified,
            schema_version=p.schema_version,
            tool_version=p.tool_version,
            original_project_id=p.original_project_id,
            master_data_size=len(p.knx_master_xml) if p.knx_master_xml else 0,
            validation_size=len(p.knx_validation),
            certificate_size=len(p.knx_certificate),
        )

    def next_free_group_address(self) -> str | None:
        """The next unused group address, style-formatted (e.g. ``"0/0/2"``); None if no project."""
        if self._pid is None:
            return None
        from xknxmono.project.core.addressing import format_ga

        value = self._svc.next_free_group_address(self._pid, _INSTALLATION)
        return format_ga(value, self.group_address_style)

    @io_guarded(lambda: None)
    def get_device_info(self, node_id: int) -> "DeviceInfo | None":
        """Descriptive device metadata (manufacturer/order number/hardware/description) from the
        imported project, independent of catalog resolution."""
        if self._pid is None:
            return None
        try:
            return self._svc.device(self._pid, node_id)
        except KeyError:
            return None

    def set_device_commissioning(
        self,
        node_id: int,
        *,
        serial_number: str | None = None,
        last_download: str | None = None,
        individual_address_loaded: bool | None = None,
        application_program_loaded: bool | None = None,
        communication_part_loaded: bool | None = None,
        medium_config_loaded: bool | None = None,
        parameters_loaded: bool | None = None,
    ) -> None:
        """Record a device's commissioning state (loaded ticks / serial / last download).

        Called after programming a device. Non-structural: the device's parameter/com-object UI is
        unchanged, so the expensive device cache is preserved (only the revision bumps)."""
        if self._pid is None:
            return
        self._svc.set_device_commissioning(
            self._pid,
            node_id,
            serial_number=serial_number,
            last_download=last_download,
            individual_address_loaded=individual_address_loaded,
            application_program_loaded=application_program_loaded,
            communication_part_loaded=communication_part_loaded,
            medium_config_loaded=medium_config_loaded,
            parameters_loaded=parameters_loaded,
        )
        self._bump(structural=False)

    @io_guarded(set)
    def program_refs(self) -> set[str]:
        """Distinct hardware-program refs (fallback product refs) across all project devices.

        Used to collect the manufacturer archives a ``.knxproj`` export needs to bundle.
        """
        if self._pid is None:
            return set()
        refs: set[str] = set()
        for row in self._svc.devices(self._pid):
            ref = row.hardware2program_ref_id or row.product_ref_id
            if ref:
                refs.add(ref)
        return refs

    @io_guarded(list)
    def missing_program_refs(self) -> list[str]:
        """Hardware-program refs of devices whose application is NOT in the local catalog.

        These are the devices dropped from the view with "application not found"; the refs can be
        fetched from the online catalog (they are a prefix of the online catalog item id).
        Guarded because it is polled every frame and also read from the fetch worker."""
        if self._pid is None:
            return []
        missing: list[str] = []
        for row in self._svc.devices(self._pid):
            ref = row.hardware2program_ref_id
            if ref and self._resolve_app(ref) is None and ref not in missing:
                missing.append(ref)
        return missing

    def refresh_catalog_resolution(self, *, rebuild: bool = False) -> None:
        """Drop the cached catalog lookups and invalidate the device view — call after new .knxprod
        products were imported (so unresolved apps now resolve) or after a UI-language change (so
        device labels re-parse in the new language).

        With ``rebuild=True`` the device views are rebuilt *now*, while the lock is held — use this
        from a worker thread (behind the progress modal) so the slow re-parse doesn't freeze the UI
        thread on the next frame. Holds the shared lock across clear + rebuild so per-frame UI reads
        (which acquire it non-blocking and bail otherwise) never see a half-cleared cache or trigger
        the rebuild themselves. The lock is re-entrant, so the ``devices`` read below still works."""
        with self._io_lock:
            self._program_to_app = None
            self._app_cache.clear()
            self._bump()
            if rebuild:
                _ = (
                    self.devices
                )  # rebuild under the held lock instead of lazily on the UI thread

    # --- application update (ETS "Update Application Program") -------------

    def newer_application_version(self, device: Device) -> int | None:
        """The newest application version available online for this device that is newer than the
        one it currently runs, or ``None``. Read-only, from the cached online index (empty until the
        online catalog has been fetched)."""
        if self._pid is None:
            return None
        parsed = parse_app_id(device.app.id)
        if parsed is None:
            return None
        info = self._svc.device(self._pid, device.node_id)
        newer = [
            item.application_version
            for item in self._catalog.online_products_for_order(info.order_number)
            if item.application_version is not None
            and item.application_version > parsed.version
        ]
        return max(newer) if newer else None

    def update_application(self, device: Device) -> UpdateApplicationResult | None:
        """Update ``device`` to the newest available version of the *same* application program,
        keeping parameter values and group-address links. Imports the newer ``.knxprod`` from the
        online catalog when it is not already local, then repoints the device and re-maps its refs
        (see :class:`~xknxmono.project.core.events.UpdateDeviceApplication`). Returns the outcome, or
        ``None`` when no newer version is available or it cannot be resolved."""
        from xknxmono.product.parser_v2.application_indexer import ApplicationIndexer

        if self._pid is None:
            return None
        parsed = parse_app_id(device.app.id)
        if parsed is None:
            return None
        info = self._svc.device(self._pid, device.node_id)
        candidates = [
            item
            for item in self._catalog.online_products_for_order(info.order_number)
            if item.application_version is not None
            and item.application_version > parsed.version
        ]
        if not candidates:
            return None
        target = max(candidates, key=lambda item: item.application_version or 0)
        target_version = target.application_version
        assert target_version is not None

        product = self._resolve_product_for_version(
            parsed.manufacturer_id, parsed.application_number, target_version, target.id
        )
        if product is None or product.application_id is None:
            self._log.warning(
                "update application: target product not resolvable",
                device=device.node_id,
                order=info.order_number,
                version=target_version,
            )
            return None
        new_app = self._catalog.get_application(product.application_id)
        if new_app is None:
            return None
        indexer = ApplicationIndexer(new_app.program)
        valid = list(set(indexer.parameter_refs) | set(indexer.com_object_refs))
        kept, dropped = self._svc.update_device_application(
            self._pid,
            device.node_id,
            product_ref_id=product.product_ref_id,
            hardware2program_ref_id=product.hardware2program_ref_id,
            old_app_id=device.app.id,
            new_app_id=product.application_id,
            valid_ref_ids=valid,
            order_number=product.order_number,
            product_name=product.name,
            manufacturer_name=product.manufacturer_name,
        )
        self._program_to_app = None
        self._app_cache.clear()
        self._bump()
        self._log.info(
            "application updated",
            device=device.node_id,
            to_version=target_version,
            kept=kept,
            dropped=dropped,
        )
        return UpdateApplicationResult(
            new_version=target_version, kept=kept, dropped=dropped
        )

    def _resolve_product_for_version(
        self,
        manufacturer_id: str,
        application_number: int,
        version: int,
        catalog_item_id: str,
    ) -> "ProductSummary | None":
        """The catalog product for an exact application version, downloading+importing the online
        ``.knxprod`` first when it is not present locally."""
        products = self._catalog.find_products_for_application(
            manufacturer_id=manufacturer_id,
            application_number=application_number,
            application_version=version,
        )
        if not products:
            self._catalog.download_online_products([catalog_item_id])
            self._program_to_app = None
            self._app_cache.clear()
            products = self._catalog.find_products_for_application(
                manufacturer_id=manufacturer_id,
                application_number=application_number,
                application_version=version,
            )
        return products[0] if products else None

    # --- device edits -----------------------------------------------------

    def find_or_create_segment_for_address(self, individual_address: str) -> int | None:
        """Return the segment id for an address' area/line, creating them if absent.

        A fresh project only has area/line ``0.0``; recovering a device at e.g.
        ``1.1.5`` needs that area and line to exist first, otherwise setting the
        address silently fails. Parses ``area.line.device`` and ensures the area
        and line (which comes with a segment) exist, returning that segment's id."""
        if self._pid is None:
            return None
        try:
            area_num, line_num, _device = (
                int(part) for part in individual_address.split(".")
            )
        except ValueError:
            return None
        topo = self._svc.topology(self._pid, _INSTALLATION)
        area = next((a for a in topo.areas if a.address == area_num), None)
        if area is None:
            self._svc.create_area(self._pid, _INSTALLATION, area_num, "")
            topo = self._svc.topology(self._pid, _INSTALLATION)
            area = next((a for a in topo.areas if a.address == area_num), None)
        if area is None:
            return None
        line = next((line for line in area.lines if line.address == line_num), None)
        if line is None:
            self._svc.create_line(self._pid, area.id, line_num, "")
            topo = self._svc.topology(self._pid, _INSTALLATION)
            area = next((a for a in topo.areas if a.address == area_num), None)
            line = (
                next((line for line in area.lines if line.address == line_num), None)
                if area is not None
                else None
            )
        if line is None or not line.segments:
            return None
        self._bump()
        return line.segments[0].id

    def add_device(
        self,
        product_ref_id: str,
        hardware2program_ref_id: str | None,
        name: str,
        app: Application,
        *,
        segment_id: int | None = None,
        address: int | None = None,
        parameters: list[tuple[str, str]] | None = None,
    ) -> int | None:
        if self._pid is None:
            return None
        if segment_id is None:
            segment_id = self._installation().areas[0].lines[0].segments[0].id
        if address is None:
            # Assign the next free individual address on the target line (ETS behaviour), instead of
            # leaving the device address-less. Editable afterwards in Configure. If the line is full,
            # fall back to no address rather than failing the add.
            try:
                address = self._svc.next_free_individual_address_for_segment(
                    self._pid, segment_id
                )
            except ValueError:
                address = None
        init_device = Device(node_id=0, name=name, app=app, individual_address="")
        com_objects: list[tuple[str, str | None]] = [
            (co.id, None) for co in init_device.com_objects
        ]
        module_instances = init_device.get_module_instances()
        device_id = self._svc.add_device(
            self._pid,
            segment_id,
            product_ref_id,
            name=name,
            address=address,
            hardware2program_ref_id=hardware2program_ref_id,
            parameters=parameters or None,
            com_objects=com_objects,
            module_instances=module_instances if module_instances else None,
        )
        if hardware2program_ref_id is not None:
            self._app_cache[hardware2program_ref_id] = app
        self._bump()
        return device_id

    def set_param(self, device: Device, param_id: str, value: str) -> None:
        if self._pid is None:
            return
        old_value = device.get_param_value(param_id)
        self._log.debug(
            "param clicked",
            device=device.node_id,
            param=param_id,
            old=old_value,
            new=value,
        )
        # Parameter-driven active com-object set BEFORE the change; the reconcile diffs it against the
        # after-set so only objects whose activeness THIS edit changes are added/removed (see
        # _sync_param_and_com_objects). Captured before set_param_value updates the live dynamic UI.
        old_active = (
            device.active_parameter_driven_com_object_ref_ids()
            if self._co_reconcile_enabled
            else set[str]()
        )
        device.set_param_value(param_id, value)
        self._log_param_tree(device, param_id)
        if self._sync_param_and_com_objects(device, param_id, value, old_active):
            self._refresh_device(device.node_id)
        self._bump(structural=False)

    def _log_param_tree(self, device: Device, param_id: str) -> None:
        """Debug: dump the (pruned) parameter tree the device now renders — total parameter count and
        the top-level sections with their parameter counts — so a parameter edit's effect on the tree
        (e.g. a section appearing/disappearing) is visible in the log."""
        from xknxmono.product.parser_v2.ui import (
            UiComObject,
            UiParameter,
            UiParameterBlock,
            UiTab,
        )

        def count(nodes: list[Any]) -> tuple[int, int]:
            params = cos = 0
            stack: list[Any] = list(nodes)
            while stack:
                n = stack.pop()
                if isinstance(n, UiParameter):
                    params += 1
                elif isinstance(n, UiComObject):
                    cos += 1
                elif isinstance(n, (UiTab, UiParameterBlock)):
                    stack.extend(n.children)
            return params, cos

        ui = device.get_ui()
        total_params, total_cos = count(list(ui))
        sections: list[str] = []
        for node in ui:
            children: list[Any] = (
                list(node.children) if isinstance(node, UiTab) else [node]
            )
            for child in children:
                if isinstance(child, (UiTab, UiParameterBlock)):
                    # Match the renderer, which shows text first (parameter_widgets.py) — so the log
                    # reflects the actual section header the user sees.
                    name = getattr(child, "text", None) or getattr(child, "name", None)
                    if name:
                        p, _ = count([child])
                        sections.append(f"{name}({p})")
        self._log.debug(
            "param tree",
            device=device.node_id,
            param=param_id,
            params=total_params,
            com_objects=total_cos,
            sections=sections[:40],
        )

    def _sync_param_and_com_objects(
        self, device: Device, param_id: str, value: str, old_active: set[str]
    ) -> bool:
        """Persist a parameter change plus any com-object re-instantiation it causes; return whether
        the com-object set changed (i.e. the edited device must be rebuilt).

        Reconcile on the DELTA of the parameter-driven active set (chain-AND) across THIS edit — never
        the absolute set. ``old_active`` is that set before the change, ``new_active`` after:
        ADD objects that became active due to this edit (``(new_active - old_active) - current``) —
        surfaces channels a function activates, incl. via a cascade like an RGB function enabling the
        separate "Channel D"; REMOVE objects that became inactive (``(old_active - new_active) & current``).
        Using the delta (not ``new_active - current``) cancels any pre-existing mismatch between the
        configured set and the parser's derivation, so an unrelated edit — or an app the parser
        under-derives (empty active set, unchanged across the edit) — touches nothing. Change is stored
        as one composite (one undo step); survivors keep flags+links, removed rows are snapshotted."""
        if self._pid is None or not self._co_reconcile_enabled:
            self._svc.set_parameter(self._pid, device.node_id, param_id, value)  # type: ignore[arg-type]
            return False
        new_active = device.active_parameter_driven_com_object_ref_ids()
        current = {co.id for co in device.com_objects}
        add = (
            new_active - old_active
        ) - current  # became active due to this edit, not yet present
        remove = (old_active - new_active) & current  # became inactive due to this edit
        target = (current - remove) | add
        self._log.debug(
            "reconcile com-objects",
            device=device.node_id,
            param=param_id,
            current=len(current),
            active_before=len(old_active),
            active_after=len(new_active),
            add=len(add),
            remove=len(remove),
        )
        if target == current:
            self._svc.set_parameter(self._pid, device.node_id, param_id, value)
            return False
        self._log.info(
            "sync com-objects",
            device=device.node_id,
            param=param_id,
            added=sorted(add),
            removed=sorted(remove),
            target=len(target),
        )
        self._svc.set_parameter_and_sync_com_objects(
            self._pid,
            device.node_id,
            param_id,
            value,
            [(ref, None) for ref in sorted(target)],
        )
        return True

    def set_param_on_matching(self, device: Device, param_id: str, value: str) -> int:
        """Set a parameter on every device running the same application (ETS-style multi-fill).

        Same-application devices share parameter ref-ids (they come from the one application
        program), so the same ``param_id`` applies. Updates each live device in place; returns how
        many devices were changed."""
        if self._pid is None:
            return 0
        app_id = getattr(device.app, "id", None)
        count = 0
        for d in self.devices:
            if getattr(d.app, "id", None) != app_id:
                continue
            try:
                old_active = (
                    d.active_parameter_driven_com_object_ref_ids()
                    if self._co_reconcile_enabled
                    else set[str]()
                )
                d.set_param_value(param_id, value)
                if self._sync_param_and_com_objects(d, param_id, value, old_active):
                    self._refresh_device(d.node_id)
            except (KeyError, ValueError):
                continue
            count += 1
        if count:
            self._bump(structural=False)
        return count

    def set_param_on_selected(
        self, node_ids: list[int], param_id: str, value: str
    ) -> int:
        """Set a parameter on each of the given devices (ETS-style multi-device edit over a chosen
        subset). Same as :meth:`set_param` per device; returns how many were changed."""
        if self._pid is None:
            return 0
        by_id = {d.node_id: d for d in self.devices}
        count = 0
        for nid in node_ids:
            d = by_id.get(nid)
            if d is None:
                continue
            try:
                old_active = (
                    d.active_parameter_driven_com_object_ref_ids()
                    if self._co_reconcile_enabled
                    else set[str]()
                )
                d.set_param_value(param_id, value)
                if self._sync_param_and_com_objects(d, param_id, value, old_active):
                    self._refresh_device(d.node_id)
            except (KeyError, ValueError):
                continue
            count += 1
        if count:
            self._bump(structural=False)
        return count

    def set_device_name(self, node_id: int, old_name: str, new_name: str) -> None:
        if self._pid is None or old_name == new_name:
            return
        self._svc.set_device_name(self._pid, node_id, new_name)
        # In place: update the live device's name and bump non-structurally (a rename changes no
        # device structure/topology), instead of rebuilding every device's dynamic UI.
        dev = self.find_device_by_node_id(node_id)
        if dev is not None:
            dev.name = new_name
        self._bump(structural=False)

    def remove_device(self, node_id: int) -> None:
        """Delete a device (and its com-objects/links) from the project."""
        if self._pid is None:
            return
        self._svc.remove_device(self._pid, node_id)
        self._bump()

    def clone_device(self, node_id: int, count: int = 1) -> list[int]:
        """Create ``count`` copies of a device, carrying over all parameter values.

        Copies keep the source product/application and parameter values; the individual address is
        left unset (the copies land in the first segment) so the user assigns fresh addresses.
        Returns the new device node ids."""
        if self._pid is None:
            return []
        row = next((r for r in self._svc.devices(self._pid) if r.id == node_id), None)
        if row is None:
            return []
        app = self._resolve_app(row.hardware2program_ref_id)
        if app is None:
            self._log.warning("cannot clone: application not resolved", device=node_id)
            return []
        params = [(p.ref_id, p.value) for p in row.parameters]
        created: list[int] = []
        for i in range(max(1, count)):
            suffix = " (copy)" if count == 1 else f" (copy {i + 1})"
            new_id = self.add_device(
                row.product_ref_id,
                row.hardware2program_ref_id,
                f"{row.name}{suffix}",
                app,
                parameters=params,
            )
            if new_id is not None:
                created.append(new_id)
        self._log.info("device cloned", source=node_id, copies=len(created))
        return created

    def set_device_individual_address(
        self, node_id: int, old_address: str, new_address: str
    ) -> bool:
        """Persist a new individual address. Returns ``True`` on success, ``False`` when rejected
        (e.g. the address is already used) so the caller can avoid mutating its live device object
        with an address the project never accepted."""
        if self._pid is None or old_address == new_address:
            return False
        try:
            self._svc.set_individual_address(self._pid, node_id, new_address)
        except (KeyError, ValueError) as e:
            self._log.warning(
                "could not set individual address", address=new_address, error=str(e)
            )
            return False
        self._bump()
        return True

    def set_flag(self, device: Device, co_id: str, flag_name: str, value: bool) -> None:
        if self._pid is None:
            return
        co = device.find_com_object(co_id)
        column = _FLAG_COLUMNS.get(flag_name)
        if co is None or co.db_id is None or column is None:
            return
        self._svc.set_com_object_flag(self._pid, co.db_id, column, value)
        # In place instead of a full rebuild (which would reset the Configure panel's tree/edit
        # state): reflect on the live com-object and push the com-object's full override set into the
        # live dynamic UI — exactly what a rebuild reconstructs from the DB — then bump non-structurally
        # so revision-keyed panels (Health/Cockpit) refresh.
        setattr(co.flags, flag_name, value)
        row = self._find_com_object_row(co.db_id)
        if row is not None:
            coir = _co_instance_ref_from_row(row) or ComObjectInstanceRef(ref_id=co_id)
            device.set_com_obj_instance_ref(co_id, coir)
        self._bump(structural=False)

    def _find_com_object_row(self, co_db_id: int) -> Any | None:
        """The core ComObject ORM row for ``co_db_id`` (to rebuild its instance-ref overrides)."""
        if self._pid is None:
            return None
        for d in self._svc.devices(self._pid):
            for c in d.com_objects:
                if c.id == co_db_id:
                    return c
        return None

    # --- topology edits ---------------------------------------------------

    def create_area(self, area_number: int, name: str = "") -> int | None:
        if self._pid is None:
            return None
        area_id = self._svc.create_area(self._pid, _INSTALLATION, area_number, name)
        self._bump()
        return area_id

    def remove_area(self, area_id: int, area_number: int = 0, name: str = "") -> None:
        if self._pid is None:
            return
        self._svc.remove_area(self._pid, area_id)
        self._bump()

    def rename_area(self, area_id: int, old_name: str, new_name: str) -> None:
        if self._pid is None or old_name == new_name:
            return
        self._svc.rename_area(self._pid, area_id, new_name)
        self._bump()

    def create_line(self, area_id: int, line_number: int, name: str = "") -> int | None:
        if self._pid is None:
            return None
        line_id = self._svc.create_line(self._pid, area_id, line_number, name)
        self._bump()
        return line_id

    def remove_line(
        self, line_id: int, area_id: int = 0, line_number: int = 0, name: str = ""
    ) -> None:
        if self._pid is None:
            return
        self._svc.remove_line(self._pid, line_id)
        self._bump()

    def rename_line(self, line_id: int, old_name: str, new_name: str) -> None:
        if self._pid is None or old_name == new_name:
            return
        self._svc.rename_line(self._pid, line_id, new_name)
        self._bump()

    # --- group address edits ----------------------------------------------

    @property
    @io_guarded(lambda: GroupAddressStyle.THREE_LEVEL)
    def group_address_style(self) -> GroupAddressStyle:
        """The project's group-address style (three-level, two-level, free).

        Read every frame by several panels, so it is IO-guarded: during a background import (which
        rewrites the schema on a worker thread) it returns the default instead of querying the DB
        mid-DDL, which would raise "malformed database schema"."""
        if self._pid is None:
            return GroupAddressStyle.THREE_LEVEL
        return GroupAddressStyle(self._svc.project(self._pid).group_address_style)

    def create_group_address(
        self, address: str | None = None, name: str = ""
    ) -> int | None:
        """Create a group address. ``address`` is a style-formatted string (e.g. ``"1/2/3"``); when
        omitted, the next free address is allocated. Returns ``None`` on an invalid address."""
        if self._pid is None:
            return None
        if address:
            style = GroupAddressStyle(self._svc.project(self._pid).group_address_style)
            try:
                value = parse_ga(address, style)
            except (ValueError, IndexError):
                self._log.warning("invalid group address", address=address)
                return None
        else:
            value = self._svc.next_free_group_address(self._pid, _INSTALLATION)
        ga_id = self._svc.create_group_address(self._pid, _INSTALLATION, value, name)
        self._bump(structural=False)
        return ga_id

    def create_group_address_value(self, value: int, name: str = "") -> int | None:
        """Return the id of the group address with this raw value, creating it if absent.

        Idempotent by value so recovering into a project that already contains a
        group address does not create duplicate rows (as a plain create would)."""
        if self._pid is None:
            return None
        existing = next(
            (
                ga.id
                for ga in self._svc.group_addresses(self._pid, _INSTALLATION)
                if ga.address == value
            ),
            None,
        )
        if existing is not None:
            return existing
        ga_id = self._svc.create_group_address(self._pid, _INSTALLATION, value, name)
        self._bump(structural=False)
        return ga_id

    def rename_group_address(self, ga_id: int, name: str) -> None:
        if self._pid is None:
            return
        self._svc.rename_group_address(self._pid, ga_id, name)
        self._bump(structural=False)

    def set_group_address_dpt(self, ga_id: int, dpt: str | None) -> None:
        if self._pid is None:
            return
        self._svc.set_group_address_datapoint_type(self._pid, ga_id, dpt or None)
        self._bump(structural=False)

    def remove_group_address(
        self, ga_id: int, address: str = "", name: str = ""
    ) -> None:
        if self._pid is None:
            return
        self._svc.remove_group_address(self._pid, ga_id)
        self._bump(structural=False)

    def create_group_range(self, parent_id: int | None, name: str) -> int | None:
        """Create an empty group-range folder (main group when ``parent_id`` is ``None``, else a
        middle group under it). Returns ``None`` when the style has no such folder or it is full."""
        if self._pid is None:
            return None
        rid = self._svc.create_group_range(self._pid, _INSTALLATION, parent_id, name)
        self._bump(structural=False)
        return rid

    def rename_group_range(self, range_id: int, name: str) -> None:
        if self._pid is None:
            return
        self._svc.rename_group_range(self._pid, range_id, name)
        self._bump(structural=False)

    def remove_group_range(self, range_id: int) -> None:
        if self._pid is None:
            return
        self._svc.remove_group_range(self._pid, range_id)
        self._bump(structural=False)

    def link_com_object_to_ga(
        self, com_object_id: int, group_address_id: int, is_sending: bool = False
    ) -> int | None:
        if self._pid is None:
            return None
        link_id = self._svc.link_com_object(
            self._pid, com_object_id, group_address_id, sending=is_sending
        )
        self._bump(structural=False)
        return link_id

    def unlink_com_object_from_ga(
        self,
        assignment_id: int,
        com_object_id: int = 0,
        group_address_id: int = 0,
        is_sending: bool = False,
    ) -> None:
        if self._pid is None:
            return
        self._svc.unlink_com_object(self._pid, assignment_id)
        self._bump(structural=False)

    # --- building functions -----------------------------------------------

    def create_function(
        self, space_id: int, function_type: str, name: str
    ) -> int | None:
        if self._pid is None:
            return None
        fid = self._svc.create_function(self._pid, space_id, function_type, name)
        self._bump(structural=False)
        return fid

    def remove_function(self, function_id: int) -> None:
        if self._pid is None:
            return
        self._svc.remove_function(self._pid, function_id)
        self._bump(structural=False)

    def rename_function(self, function_id: int, name: str) -> None:
        if self._pid is None:
            return
        self._svc.rename_function(self._pid, function_id, name)
        self._bump(structural=False)

    def set_function_type(self, function_id: int, function_type: str) -> None:
        if self._pid is None:
            return
        self._svc.set_function_type(self._pid, function_id, function_type)
        self._bump(structural=False)

    def add_function_group_address(
        self, function_id: int, group_address_id: int, role: str = ""
    ) -> int | None:
        if self._pid is None:
            return None
        link_id = self._svc.add_function_group_address(
            self._pid, function_id, group_address_id, role
        )
        self._bump(structural=False)
        return link_id

    def remove_function_group_address(self, link_id: int) -> None:
        if self._pid is None:
            return
        self._svc.remove_function_group_address(self._pid, link_id)
        self._bump(structural=False)

    # --- building spaces (location tree) ----------------------------------

    @io_guarded(list)
    def get_unassigned_devices(self) -> "list[SpaceDeviceInfo]":
        # Per-frame read (Spaces panel "Without space" section): guard it like the other tree reads
        # so it bails to an empty list while a background import holds the IO lock and rewrites the
        # schema — an unguarded query races the DDL and SQLite raises "malformed database schema".
        if self._pid is None:
            return []
        return self._svc.unassigned_devices(self._pid, _INSTALLATION)

    def create_space(
        self, parent_id: int | None, space_type: str, name: str
    ) -> int | None:
        if self._pid is None:
            return None
        sid = self._svc.create_space(
            self._pid, _INSTALLATION, space_type, name, parent_id
        )
        self._bump(structural=False)
        return sid

    def rename_space(self, space_id: int, name: str) -> None:
        if self._pid is None:
            return
        self._svc.rename_space(self._pid, space_id, name)
        self._bump(structural=False)

    def set_space_type(self, space_id: int, space_type: str) -> None:
        if self._pid is None:
            return
        self._svc.set_space_type(self._pid, space_id, space_type)
        self._bump(structural=False)

    def move_space(self, space_id: int, new_parent_id: int | None) -> None:
        if self._pid is None:
            return
        self._svc.move_space(self._pid, space_id, new_parent_id)
        self._bump(structural=False)

    def remove_space(self, space_id: int) -> None:
        if self._pid is None:
            return
        self._svc.remove_space(self._pid, space_id)
        self._bump(structural=False)

    def set_device_space(self, device_id: int, space_id: int | None) -> None:
        if self._pid is None:
            return
        self._svc.set_device_space(self._pid, device_id, space_id)
        self._bump(structural=False)

    # --- undo / redo / history --------------------------------------------

    def undo(self) -> bool:
        if self._pid is None:
            return False
        peek = self._svc.peek_undo(self._pid)
        result = self._svc.undo(self._pid)
        if result:
            self._refresh_after_history(peek, undo=True)
        return result

    def redo(self) -> bool:
        if self._pid is None:
            return False
        peek = self._svc.peek_redo(self._pid)
        result = self._svc.redo(self._pid)
        if result:
            self._refresh_after_history(peek, undo=False)
        return result

    def _refresh_after_history(
        self, peek: "tuple[str, dict[str, Any]] | None", *, undo: bool
    ) -> None:
        """Refresh views after an undo/redo. A plain parameter change is applied *in place* on the
        affected device (like a live edit); a composite param+com-object change rebuilds only that one
        device (its com-object rows changed in the DB) — both instant, instead of discarding and
        re-parsing every device's dynamic UI. Anything else falls back to a full structural rebuild."""
        if peek is not None and self._devices_cache is not None:
            event_type, data = peek
            if event_type == "SetParameter":
                value = data.get("old_value") if undo else data.get("value")
                device = self.find_device_by_node_id(int(data["device_id"]))
                if device is not None and value is not None:
                    device.set_param_value(str(data["ref_id"]), str(value))
                    self._bump(structural=False)
                    return
            elif event_type in ("Composite", "SyncDeviceComObjects"):
                node_id = _history_device_id(data)
                if node_id is not None:
                    self._refresh_device(node_id)  # rebuild only this device (not all)
                    self._bump(structural=False)
                    return
        self._bump(structural=True)

    @io_guarded(lambda: False)
    def can_undo(self) -> bool:
        return self._pid is not None and self._svc.can_undo(self._pid)

    @io_guarded(lambda: False)
    def can_redo(self) -> bool:
        return self._pid is not None and self._svc.can_redo(self._pid)

    @property
    @io_guarded(lambda: 0)
    def cursor(self) -> int:
        return self._svc.cursor(self._pid) if self._pid is not None else 0

    def jump_to(self, event_id: int) -> None:
        if self._pid is None:
            return
        self._svc.jump_to(self._pid, event_id)
        self._bump()

    @io_guarded(list)
    def history(self) -> list[HistoryEntry]:
        if self._pid is None:
            return []
        return [
            HistoryEntry(
                id=entry.id,
                display_text=_history_label(entry.event_type, entry.data),
                reverted=entry.reverted,
            )
            for entry in self._svc.history(self._pid)
        ]

    def _history_key(self) -> frozenset[tuple[int, str, str]]:
        """Signature of the currently-effective (non-reverted) events.

        Includes the event type and a repr of its data, not just the id: a store that deletes
        events on branch (undo + new command) can reuse an id, which an id-only set would miss."""
        if self._pid is None:
            return frozenset()
        return frozenset(
            (entry.id, entry.event_type, repr(entry.data))
            for entry in self._svc.history(self._pid)
            if not entry.reverted
        )

    @io_guarded(lambda: False)
    def edited_since_open(self) -> bool:
        """Whether the effective edit set changed since the project was opened.

        Opening a previously-edited project is not "modified"; only edits (or undo/redo) made in
        this session since the open count. Used to gate the read-only pre-flight self-test."""
        return self._history_key() != self._history_baseline
