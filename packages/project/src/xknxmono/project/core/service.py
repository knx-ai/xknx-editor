"""`ProjectService` — owns N open projects (one SQLite document each), keyed by project id.

Every edit funnels through an :class:`~xknxmono.project.core.event_store.EventStore`, which applies
the event, persists it to the ``events`` history, and manages the undo/redo cursor. The live state
is the relational tables; reads return ORM rows. Installation-scoped calls take the installation's
0-based ``index``; other graph references use internal row ids.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from xknxmono.project.core.addressing import (
    GroupAddressStyle,
    format_ga,
    format_ia,
    parse_ia,
    ranges_for,
)
from xknxmono.project.core.event_store import EventStore, HistoryEntry
from xknxmono.project.core.events import (
    COM_OBJECT_FLAGS,
    AddDevice,
    AddFunctionGroupAddress,
    AddInstallation,
    CompositeEvent,
    CreateArea,
    CreateFunction,
    CreateGroupAddress,
    CreateGroupRange,
    CreateLine,
    CreateSegment,
    CreateSpace,
    LinkComObject,
    MoveDevice,
    MoveSpace,
    RemoveArea,
    RemoveDevice,
    RemoveFunction,
    RemoveFunctionGroupAddress,
    RemoveGroupAddress,
    RemoveGroupRange,
    RemoveLine,
    RemoveSegment,
    RemoveSpace,
    RenameArea,
    RenameFunction,
    RenameGroupAddress,
    RenameGroupRange,
    RenameLine,
    RenameSpace,
    SetComObjectFlag,
    SetComObjectSending,
    SetDeviceCommissioning,
    SetDeviceName,
    SetDeviceSpace,
    SetFunctionType,
    SetGroupAddressDatapointType,
    SetParameter,
    SetSpaceType,
    SyncDeviceComObjects,
    UnlinkComObject,
    UpdateDeviceApplication,
)
from xknxmono.project.core.skeleton import MEDIUM_TP, seed_new_project
from xknxmono.project.db import make_engine, url_for
from xknxmono.project.models import (
    Area,
    ComObjectLink,
    Device,
    Function,
    GroupAddress,
    GroupRange,
    Installation,
    Line,
    Project,
    Segment,
    Space,
)


@dataclass
class _Open:
    engine: Engine
    session: Session
    store: EventStore


@dataclass(frozen=True)
class GroupAddressInfo:
    """A group address resolved for display: its value, the style-formatted string, and its links."""

    id: int
    address: int
    text: str
    name: str
    datapoint_type: str | None
    links: list[int]
    description: str
    comment: str
    data_secure: bool


@dataclass(frozen=True)
class GroupRangeInfo:
    """A node in the group-address range tree, resolved for display (recursive)."""

    id: int
    name: str
    range_start: int
    range_end: int
    children: list[GroupRangeInfo]
    group_addresses: list[GroupAddressInfo]


@dataclass(frozen=True)
class SpaceDeviceInfo:
    """A device as referenced from a space (building tree leaf), with display metadata."""

    id: int
    name: str
    individual_address: str | None
    description: str
    product_name: str
    hardware_name: str
    manufacturer_name: str


@dataclass(frozen=True)
class FunctionGroupAddressInfo:
    """A group address referenced by a function, with its role."""

    id: int  # FunctionGroupAddress link id (for removal)
    group_address_id: int
    text: str
    role: str


@dataclass(frozen=True)
class FunctionInfo:
    """A function assigned to a space, resolved for display."""

    id: int
    name: str
    function_type: str
    usage_text: str
    group_addresses: list[FunctionGroupAddressInfo]


@dataclass(frozen=True)
class SpaceInfo:
    """A node in the building/location tree, resolved for display (recursive)."""

    id: int
    name: str
    space_type: str
    number: str
    usage_text: str
    description: str
    children: list[SpaceInfo]
    devices: list[SpaceDeviceInfo]
    functions: list[FunctionInfo]


@dataclass(frozen=True)
class DeviceInfo:
    """A device resolved for display. The refs identify the catalog product and the loaded program;
    callers resolve the application from them (the project package itself is ref-only)."""

    id: int
    name: str
    individual_address: str | None
    product_ref_id: str
    hardware2program_ref_id: str | None
    description: str
    order_number: str
    hardware_name: str
    product_name: str
    manufacturer_name: str
    # Commissioning state (ETS's "loaded" ticks + serial / last download).
    serial_number: str
    last_download: str | None
    individual_address_loaded: bool
    application_program_loaded: bool
    communication_part_loaded: bool
    medium_config_loaded: bool
    parameters_loaded: bool


@dataclass(frozen=True)
class LinkInfo:
    """A link between a com-object and a group address; ``is_sending`` marks a transmitting link."""

    id: int
    com_object_id: int
    group_address_id: int
    is_sending: bool


class ProjectService:
    def __init__(self) -> None:
        self._projects: dict[str, _Open] = {}

    # --- lifecycle --------------------------------------------------------

    def create(
        self,
        path: Path | str,
        project_id: str | None = None,
        *,
        group_address_style: GroupAddressStyle = GroupAddressStyle.THREE_LEVEL,
    ) -> str:
        # ETS project IDs are "P-" + 4 hex digits (spec Project Scheme §4.2.3, e.g. "P-02D7").
        pid = project_id or f"P-{uuid4().hex[:4].upper()}"
        engine = make_engine(url_for(Path(path)))
        session = Session(engine)
        seed_new_project(session, pid, "New project", group_address_style)
        self._register(pid, engine, session)
        return pid

    def open(self, path: Path | str) -> str:
        engine = make_engine(url_for(Path(path)))
        session = Session(engine)
        project = session.query(Project).first()
        if project is None:
            raise ValueError(f"{path} is not a project (no project row)")
        self._register(project.id, engine, session)
        return project.id

    def close(self, project_id: str) -> None:
        state = self._projects.pop(project_id)
        state.session.close()
        state.engine.dispose()

    def list(self) -> list[str]:
        return list(self._projects)

    # --- commands (one public method each) --------------------------------

    def add_installation(self, project_id: str, name: str) -> int:
        state = self._state(project_id)
        highest = state.session.query(func.max(Installation.index)).scalar()
        index = highest + 1 if highest is not None else 0
        state.store.append(AddInstallation(index=index, name=name))
        return index

    def create_area(
        self, project_id: str, installation: int, address: int, name: str
    ) -> int:
        state = self._state(project_id)
        event = CreateArea(
            installation_id=self._installation(state, installation).id,
            address=address,
            name=name,
        )
        state.store.append(event)
        assert event.area_id is not None
        return event.area_id

    def create_line(
        self, project_id: str, area_id: int, address: int, name: str
    ) -> int:
        state = self._state(project_id)
        event = CreateLine(
            area_id=area_id, address=address, name=name, medium_type=MEDIUM_TP
        )
        state.store.append(event)
        assert event.line_id is not None
        return event.line_id

    def add_segment(
        self,
        project_id: str,
        line_id: int,
        *,
        medium_type: str = MEDIUM_TP,
        name: str = "",
    ) -> int:
        """Add a media segment to a line (its number continues the line's existing segments)."""
        state = self._state(project_id)
        highest = (
            state.session.query(func.max(Segment.number))
            .filter_by(line_id=line_id)
            .scalar()
        )
        number = highest + 1 if highest is not None else 0
        event = CreateSegment(
            line_id=line_id, number=number, medium_type=medium_type, name=name
        )
        state.store.append(event)
        assert event.segment_id is not None
        return event.segment_id

    def add_device(
        self,
        project_id: str,
        segment_id: int,
        product_ref_id: str,
        *,
        address: int | None = None,
        name: str = "",
        hardware2program_ref_id: str | None = None,
        parameters: list[tuple[str, str]] | None = None,
        com_objects: list[tuple[str, str | None]] | None = None,
        module_instances: list[tuple[str, str]] | None = None,
    ) -> int:
        """Add a device. ``product_ref_id`` is the catalog product; ``hardware2program_ref_id`` is
        the loaded program through which the application resolves. The project package is ref-only —
        it never reads the catalog, so the caller expands the application and passes its
        ``parameters`` (``(ref_id, value)``), ``com_objects`` (``(ref_id, channel_id)``), and
        ``module_instances`` (``(instance_id, ref_id)``) in."""
        state = self._state(project_id)
        if address is not None:
            self._check_unique_address(state, segment_id, address)
        event = AddDevice(
            segment_id=segment_id,
            address=address,
            name=name,
            product_ref_id=product_ref_id,
            hardware2program_ref_id=hardware2program_ref_id,
            parameters=[[ref, value] for ref, value in (parameters or [])],
            com_objects=[[ref, channel] for ref, channel in (com_objects or [])],
            module_instances=[[iid, rid] for iid, rid in (module_instances or [])],
        )
        state.store.append(event)
        assert event.device_id is not None
        return event.device_id

    def set_parameter(
        self, project_id: str, device_id: int, ref_id: str, value: str
    ) -> None:
        self._state(project_id).store.append(
            SetParameter(device_id=device_id, ref_id=ref_id, value=value)
        )

    def create_group_address(
        self, project_id: str, installation: int, address: int, name: str
    ) -> int:
        state = self._state(project_id)
        levels = ranges_for(address, self._style(state))
        event = CreateGroupAddress(
            installation_id=self._installation(state, installation).id,
            address=address,
            name=name,
            levels=[[start, end, range_name] for start, end, range_name in levels],
        )
        state.store.append(event)
        assert event.ga_id is not None
        return event.ga_id

    def create_group_range(
        self, project_id: str, installation: int, parent_id: int | None, name: str
    ) -> int | None:
        """Create an empty group-range folder (a main or middle group) and return its id.

        ``parent_id`` ``None`` adds a main group (the next free main number); a main group's id adds
        a middle group under it (the next free middle, ThreeLevel only). Returns ``None`` when the
        style has no such folders (Free, or a middle group in TwoLevel) or the level is full."""
        state = self._state(project_id)
        style = self._style(state)
        if style is GroupAddressStyle.FREE:
            return None
        inst = self._installation(state, installation)
        if parent_id is None:
            # Main group: lowest unused main number (0-31), range = main << 11 .. + 0x7FF.
            used = {
                rs >> 11
                for (rs,) in state.session.query(GroupRange.range_start).filter(
                    GroupRange.installation_id == inst.id,
                    GroupRange.parent_id.is_(None),
                )
            }
            number = next((n for n in range(32) if n not in used), None)
            if number is None:
                return None
            base = number << 11
            start, end = max(1, base), base + 0x7FF
        else:
            # Middle group under a main (ThreeLevel only): lowest unused middle (0-7).
            if style is not GroupAddressStyle.THREE_LEVEL:
                return None
            parent = state.session.get(GroupRange, parent_id)
            if parent is None:
                return None
            main = parent.range_start >> 11
            used = {
                (rs >> 8) & 0x7
                for (rs,) in state.session.query(GroupRange.range_start).filter(
                    GroupRange.installation_id == inst.id,
                    GroupRange.parent_id == parent_id,
                )
            }
            number = next((m for m in range(8) if m not in used), None)
            if number is None:
                return None
            base = (main << 11) + (number << 8)
            start, end = max(1, base), base + 0xFF
        event = CreateGroupRange(
            installation_id=inst.id,
            parent_id=parent_id,
            range_start=start,
            range_end=end,
            name=name,
        )
        state.store.append(event)
        return event.range_id

    def rename_group_range(self, project_id: str, range_id: int, name: str) -> None:
        self._state(project_id).store.append(
            RenameGroupRange(range_id=range_id, name=name)
        )

    def remove_group_range(self, project_id: str, range_id: int) -> None:
        self._state(project_id).store.append(RemoveGroupRange(target_id=range_id))

    def link_com_object(
        self,
        project_id: str,
        com_object_id: int,
        group_address_id: int,
        *,
        sending: bool = False,
    ) -> int:
        """Link a com-object to a group address; ``sending`` marks it as the transmitting link.
        Use :meth:`set_com_object_sending` to reassign the sender across a com-object's links."""
        state = self._state(project_id)
        event = LinkComObject(
            com_object_id=com_object_id,
            group_address_id=group_address_id,
            is_sending=sending,
        )
        state.store.append(event)
        assert event.link_id is not None
        return event.link_id

    def set_com_object_sending(self, project_id: str, link_id: int) -> None:
        """Make this link the com-object's sending link, clearing the bit on its sibling links."""
        self._state(project_id).store.append(SetComObjectSending(link_id=link_id))

    def set_com_object_flag(
        self, project_id: str, com_object_id: int, flag: str, value: bool | None
    ) -> None:
        """Override a com-object flag (``value`` forces it; ``None`` reverts to the product default).

        ``flag`` is one of :data:`~xknxmono.project.core.events.COM_OBJECT_FLAGS`."""
        if flag not in COM_OBJECT_FLAGS:
            raise ValueError(f"Unknown com-object flag {flag!r}")
        self._state(project_id).store.append(
            SetComObjectFlag(com_object_id=com_object_id, flag=flag, value=value)
        )

    def set_group_address_datapoint_type(
        self, project_id: str, group_address_id: int, datapoint_type: str | None
    ) -> None:
        self._state(project_id).store.append(
            SetGroupAddressDatapointType(
                group_address_id=group_address_id, datapoint_type=datapoint_type
            )
        )

    # --- building functions -----------------------------------------------

    def create_function(
        self, project_id: str, space_id: int, function_type: str, name: str
    ) -> int:
        """Create a building function in a space; returns the new function id."""
        state = self._state(project_id)
        event = CreateFunction(
            space_id=space_id, function_type=function_type, name=name
        )
        state.store.append(event)
        assert event.function_id is not None
        return event.function_id

    def remove_function(self, project_id: str, function_id: int) -> None:
        self._state(project_id).store.append(RemoveFunction(target_id=function_id))

    def rename_function(self, project_id: str, function_id: int, name: str) -> None:
        self._state(project_id).store.append(
            RenameFunction(function_id=function_id, name=name)
        )

    def set_function_type(
        self, project_id: str, function_id: int, function_type: str
    ) -> None:
        self._state(project_id).store.append(
            SetFunctionType(function_id=function_id, function_type=function_type)
        )

    def add_function_group_address(
        self, project_id: str, function_id: int, group_address_id: int, role: str = ""
    ) -> int:
        """Assign a group address to a function under ``role``; returns the new link id."""
        state = self._state(project_id)
        event = AddFunctionGroupAddress(
            function_id=function_id, group_address_id=group_address_id, role=role
        )
        state.store.append(event)
        assert event.link_id is not None
        return event.link_id

    def remove_function_group_address(self, project_id: str, link_id: int) -> None:
        self._state(project_id).store.append(
            RemoveFunctionGroupAddress(target_id=link_id)
        )

    # --- building spaces (location tree) ----------------------------------

    def create_space(
        self,
        project_id: str,
        installation: int,
        space_type: str,
        name: str,
        parent_id: int | None = None,
    ) -> int:
        """Create a building space (building/floor/room/…) under ``parent_id`` (or at the top level
        when ``None``). New siblings are appended after the existing ones; returns the new id."""
        state = self._state(project_id)
        inst = self._installation(state, installation)
        highest = (
            state.session.query(func.max(Space.order))
            .filter(Space.installation_id == inst.id, Space.parent_id == parent_id)
            .scalar()
        )
        order = highest + 1 if highest is not None else 0
        event = CreateSpace(
            installation_id=inst.id,
            space_type=space_type,
            name=name,
            parent_id=parent_id,
            order=order,
        )
        state.store.append(event)
        assert event.space_id is not None
        return event.space_id

    def rename_space(self, project_id: str, space_id: int, name: str) -> None:
        self._state(project_id).store.append(RenameSpace(space_id=space_id, name=name))

    def set_space_type(self, project_id: str, space_id: int, space_type: str) -> None:
        self._state(project_id).store.append(
            SetSpaceType(space_id=space_id, space_type=space_type)
        )

    def move_space(
        self, project_id: str, space_id: int, new_parent_id: int | None
    ) -> None:
        """Re-parent a space. Rejects a move that would create a cycle (making a space its own
        ancestor). ``new_parent_id`` ``None`` moves the space to the top level."""
        state = self._state(project_id)
        if new_parent_id is not None:
            if new_parent_id == space_id:
                raise ValueError("cannot move a space into itself")
            ancestor = state.session.get(Space, new_parent_id)
            while ancestor is not None:
                if ancestor.id == space_id:
                    raise ValueError("cannot move a space into its own descendant")
                ancestor = (
                    state.session.get(Space, ancestor.parent_id)
                    if ancestor.parent_id is not None
                    else None
                )
        state.store.append(MoveSpace(space_id=space_id, new_parent_id=new_parent_id))

    def remove_space(self, project_id: str, space_id: int) -> None:
        self._state(project_id).store.append(RemoveSpace(target_id=space_id))

    def set_device_space(
        self, project_id: str, device_id: int, space_id: int | None
    ) -> None:
        """Assign a device to a space (room), or unassign it (``space_id`` ``None``)."""
        self._state(project_id).store.append(
            SetDeviceSpace(device_id=device_id, space_id=space_id)
        )

    def set_device_commissioning(
        self,
        project_id: str,
        device_id: int,
        *,
        serial_number: str | None = None,
        last_download: str | None = None,
        individual_address_loaded: bool | None = None,
        application_program_loaded: bool | None = None,
        communication_part_loaded: bool | None = None,
        medium_config_loaded: bool | None = None,
        parameters_loaded: bool | None = None,
    ) -> None:
        """Update a device's commissioning state (loaded ticks, serial, last download).

        Each field is optional; ``None`` leaves it unchanged. Typically called after programming to
        record what was loaded, and by the importer's round-trip (the ``.knxproj`` carries it)."""
        self._state(project_id).store.append(
            SetDeviceCommissioning(
                device_id=device_id,
                serial_number=serial_number,
                last_download=last_download,
                individual_address_loaded=individual_address_loaded,
                application_program_loaded=application_program_loaded,
                communication_part_loaded=communication_part_loaded,
                medium_config_loaded=medium_config_loaded,
                parameters_loaded=parameters_loaded,
            )
        )

    # --- remove / rename / move -------------------------------------------

    def remove_device(self, project_id: str, device_id: int) -> None:
        self._state(project_id).store.append(RemoveDevice(target_id=device_id))

    def remove_area(self, project_id: str, area_id: int) -> None:
        self._state(project_id).store.append(RemoveArea(target_id=area_id))

    def remove_line(self, project_id: str, line_id: int) -> None:
        self._state(project_id).store.append(RemoveLine(target_id=line_id))

    def remove_segment(self, project_id: str, segment_id: int) -> None:
        self._state(project_id).store.append(RemoveSegment(target_id=segment_id))

    def remove_group_address(self, project_id: str, group_address_id: int) -> None:
        self._state(project_id).store.append(
            RemoveGroupAddress(target_id=group_address_id)
        )

    def unlink_com_object(self, project_id: str, link_id: int) -> None:
        self._state(project_id).store.append(UnlinkComObject(target_id=link_id))

    def rename_area(self, project_id: str, area_id: int, name: str) -> None:
        self._state(project_id).store.append(RenameArea(area_id=area_id, name=name))

    def rename_line(self, project_id: str, line_id: int, name: str) -> None:
        self._state(project_id).store.append(RenameLine(line_id=line_id, name=name))

    def rename_group_address(
        self, project_id: str, group_address_id: int, name: str
    ) -> None:
        self._state(project_id).store.append(
            RenameGroupAddress(group_address_id=group_address_id, name=name)
        )

    def set_device_name(self, project_id: str, device_id: int, name: str) -> None:
        self._state(project_id).store.append(
            SetDeviceName(device_id=device_id, name=name)
        )

    def sync_device_com_objects(
        self,
        project_id: str,
        device_id: int,
        target: list[tuple[str, str | None]],
    ) -> None:
        """Reconcile a device's com-object rows to ``target`` (the parameter-driven should-exist set
        of ``(ref_id, channel_id)``): add missing refs, remove obsolete ones (with links), keep
        survivors. Undoable. The caller computes ``target`` (the project package is ref-only)."""
        self._state(project_id).store.append(
            SyncDeviceComObjects(
                device_id=device_id,
                target=[[ref_id, channel_id] for ref_id, channel_id in target],
            )
        )

    def set_parameter_and_sync_com_objects(
        self,
        project_id: str,
        device_id: int,
        ref_id: str,
        value: str,
        target: list[tuple[str, str | None]],
    ) -> None:
        """Set a parameter and reconcile the device's com-objects to ``target`` as ONE undo step (a
        function/mode change and the objects it activates/deactivates must revert together)."""
        self._state(project_id).store.append(
            CompositeEvent(
                events=[
                    SetParameter(device_id=device_id, ref_id=ref_id, value=value),
                    SyncDeviceComObjects(
                        device_id=device_id,
                        target=[[r, c] for r, c in target],
                    ),
                ]
            )
        )

    def update_device_application(
        self,
        project_id: str,
        device_id: int,
        *,
        product_ref_id: str,
        hardware2program_ref_id: str | None,
        old_app_id: str,
        new_app_id: str,
        valid_ref_ids: list[str],
        order_number: str | None = None,
        hardware_name: str | None = None,
        product_name: str | None = None,
        manufacturer_name: str | None = None,
        description: str | None = None,
    ) -> tuple[int, int]:
        """Update a device to a newer version of the same application, keeping parameter values and
        group-address links (see :class:`UpdateDeviceApplication`). Returns ``(kept, dropped)``: how
        many parameter/com-object rows carried over and how many were dropped as incompatible."""
        state = self._state(project_id)
        event = state.store.append(
            UpdateDeviceApplication(
                device_id=device_id,
                new_product_ref_id=product_ref_id,
                new_hardware2program_ref_id=hardware2program_ref_id,
                old_app_id=old_app_id,
                new_app_id=new_app_id,
                valid_ref_ids=valid_ref_ids,
                new_order_number=order_number,
                new_hardware_name=hardware_name,
                new_product_name=product_name,
                new_manufacturer_name=manufacturer_name,
                new_description=description,
            )
        )
        assert isinstance(event, UpdateDeviceApplication)
        dropped = len(event.deleted_params) + len(event.deleted_com_objects)
        device = state.session.get(Device, device_id)
        kept = (len(device.parameters) + len(device.com_objects)) if device else 0
        return kept, dropped

    def move_device(
        self, project_id: str, device_id: int, segment_id: int, address: int | None
    ) -> None:
        state = self._state(project_id)
        if address is not None:
            self._check_unique_address(state, segment_id, address, exclude=device_id)
        state.store.append(
            MoveDevice(device_id=device_id, segment_id=segment_id, address=address)
        )

    # --- undo / redo / history --------------------------------------------

    def undo(self, project_id: str) -> bool:
        return self._state(project_id).store.undo()

    def redo(self, project_id: str) -> bool:
        return self._state(project_id).store.redo()

    def peek_undo(self, project_id: str) -> tuple[str, dict[str, Any]] | None:
        """(type, data) of the event ``undo`` would revert next — lets a caller pick a cheaper
        refresh (e.g. an in-place parameter update) instead of a full rebuild."""
        return self._state(project_id).store.peek_undo()

    def peek_redo(self, project_id: str) -> tuple[str, dict[str, Any]] | None:
        return self._state(project_id).store.peek_redo()

    def can_undo(self, project_id: str) -> bool:
        return self._state(project_id).store.can_undo()

    def can_redo(self, project_id: str) -> bool:
        return self._state(project_id).store.can_redo()

    def cursor(self, project_id: str) -> int:
        return self._state(project_id).store.cursor

    def jump_to(self, project_id: str, event_id: int) -> None:
        self._state(project_id).store.jump_to(event_id)

    def history(self, project_id: str) -> list[HistoryEntry]:
        return self._state(project_id).store.history()

    # --- reads ------------------------------------------------------------

    def project(self, project_id: str) -> Project:
        project = self._state(project_id).session.get(Project, project_id)
        assert project is not None
        return project

    def installations(self, project_id: str) -> list[Installation]:
        return (
            self._state(project_id)
            .session.query(Installation)
            .order_by(Installation.index)
            .all()
        )

    def topology(self, project_id: str, installation: int) -> Installation:
        return self._installation(self._state(project_id), installation)

    def devices(self, project_id: str) -> list[Device]:
        return self._state(project_id).session.query(Device).order_by(Device.id).all()

    def device(self, project_id: str, device_id: int) -> DeviceInfo:
        """A device resolved for display (composed individual address + catalog/program refs)."""
        state = self._state(project_id)
        device = state.session.get(Device, device_id)
        if device is None:
            raise KeyError(f"No device with id {device_id}")
        return DeviceInfo(
            id=device.id,
            name=device.name,
            individual_address=self._compose_ia(device),
            product_ref_id=device.product_ref_id,
            hardware2program_ref_id=device.hardware2program_ref_id,
            description=device.description,
            order_number=device.order_number,
            hardware_name=device.hardware_name,
            product_name=device.product_name,
            manufacturer_name=device.manufacturer_name,
            serial_number=device.serial_number,
            last_download=device.last_download,
            individual_address_loaded=device.individual_address_loaded,
            application_program_loaded=device.application_program_loaded,
            communication_part_loaded=device.communication_part_loaded,
            medium_config_loaded=device.medium_config_loaded,
            parameters_loaded=device.parameters_loaded,
        )

    def com_object_links(self, project_id: str, com_object_id: int) -> list[LinkInfo]:
        """A com-object's links (to group addresses), with the sending one flagged."""
        return self._links(
            self._state(project_id)
            .session.query(ComObjectLink)
            .filter_by(com_object_id=com_object_id)
            .order_by(ComObjectLink.id)
            .all()
        )

    def group_address_links(
        self, project_id: str, group_address_id: int
    ) -> list[LinkInfo]:
        """Every com-object linked to a group address (its assignments), sending flagged."""
        return self._links(
            self._state(project_id)
            .session.query(ComObjectLink)
            .filter_by(group_address_id=group_address_id)
            .order_by(ComObjectLink.id)
            .all()
        )

    def group_addresses(self, project_id: str) -> list[GroupAddressInfo]:
        state = self._state(project_id)
        style = self._style(state)
        rows = state.session.query(GroupAddress).order_by(GroupAddress.id).all()
        return [self._ga_info(row, style) for row in rows]

    def group_ranges(self, project_id: str, installation: int) -> list[GroupRangeInfo]:
        """The installation's group-address range tree (roots → children), resolved for display."""
        state = self._state(project_id)
        style = self._style(state)
        inst = self._installation(state, installation)
        roots = (
            state.session.query(GroupRange)
            .filter(
                GroupRange.installation_id == inst.id,
                GroupRange.parent_id.is_(None),
            )
            .order_by(GroupRange.range_start)
            .all()
        )
        return [self._range_info(r, style) for r in roots]

    def space_tree(self, project_id: str, installation: int) -> list[SpaceInfo]:
        """The installation's building/location tree (roots → children), with devices and functions
        resolved for display."""
        state = self._state(project_id)
        style = self._style(state)
        inst = self._installation(state, installation)
        roots = (
            state.session.query(Space)
            .filter(Space.installation_id == inst.id, Space.parent_id.is_(None))
            .order_by(Space.order, Space.id)
            .all()
        )
        return [self._space_info(s, style) for s in roots]

    def unassigned_devices(
        self, project_id: str, installation: int
    ) -> list[SpaceDeviceInfo]:
        """Devices in the installation that are not placed in any space (``space_id IS NULL``)."""
        state = self._state(project_id)
        inst = self._installation(state, installation)
        devices = (
            state.session.query(Device)
            .join(Segment, Device.segment_id == Segment.id)
            .join(Line, Segment.line_id == Line.id)
            .join(Area, Line.area_id == Area.id)
            .filter(Area.installation_id == inst.id, Device.space_id.is_(None))
            .order_by(Device.name, Device.id)
            .all()
        )
        return [self._space_device_info(d) for d in devices]

    def group_address(self, project_id: str, group_address_id: int) -> GroupAddressInfo:
        state = self._state(project_id)
        ga = state.session.get(GroupAddress, group_address_id)
        if ga is None:
            raise KeyError(f"No group address with id {group_address_id}")
        return self._ga_info(ga, self._style(state))

    def next_free_group_address(
        self, project_id: str, installation: int, *, start: int = 1
    ) -> int:
        """The lowest unused group-address value (>= ``start``) in the installation. Address 0 is
        reserved, so allocation begins at 1."""
        state = self._state(project_id)
        inst = self._installation(state, installation)
        used = {
            address
            for (address,) in state.session.query(GroupAddress.address)
            .join(GroupRange, GroupAddress.group_range_id == GroupRange.id)
            .filter(GroupRange.installation_id == inst.id)
        }
        address = max(1, start)
        while address in used:
            address += 1
        if address > 0xFFFF:
            raise ValueError("no free group address available")
        return address

    # --- individual-address helpers ---------------------------------------

    def individual_address(self, project_id: str, device_id: int) -> str | None:
        """The device's ``area.line.device`` string, or ``None`` if its octet is unassigned."""
        state = self._state(project_id)
        device = state.session.get(Device, device_id)
        if device is None:
            raise KeyError(f"No device with id {device_id}")
        return self._compose_ia(device)

    def next_free_individual_address(self, project_id: str, line_id: int) -> int:
        """The lowest unused device octet (1-255) across all segments of the line."""
        state = self._state(project_id)
        if state.session.get(Line, line_id) is None:
            raise KeyError(f"No line with id {line_id}")
        used = {
            octet
            for (octet,) in state.session.query(Device.address)
            .join(Segment, Device.segment_id == Segment.id)
            .filter(Segment.line_id == line_id, Device.address.is_not(None))
        }
        octet = 1
        while octet in used:
            octet += 1
        if octet > 255:
            raise ValueError("no free individual address on this line")
        return octet

    def next_free_individual_address_for_segment(
        self, project_id: str, segment_id: int
    ) -> int:
        """The lowest unused device octet (1-255) on the line the segment belongs to."""
        state = self._state(project_id)
        segment = state.session.get(Segment, segment_id)
        if segment is None:
            raise KeyError(f"No segment with id {segment_id}")
        return self.next_free_individual_address(project_id, segment.line_id)

    def set_individual_address(
        self, project_id: str, device_id: int, address: str
    ) -> None:
        """Place a device at an ``area.line.device`` address within its installation.

        Resolves the target line by its area/line numbers and uses that line's first segment (the
        segment is a media grouping, not part of the address). Raises if no such line exists."""
        state = self._state(project_id)
        device = state.session.get(Device, device_id)
        if device is None:
            raise KeyError(f"No device with id {device_id}")
        area_no, line_no, octet = parse_ia(address)
        installation_id = device.segment.line.area.installation_id
        line = (
            state.session.query(Line)
            .join(Area, Line.area_id == Area.id)
            .filter(
                Area.installation_id == installation_id,
                Area.address == area_no,
                Line.address == line_no,
            )
            .first()
        )
        if line is None:
            raise KeyError(f"No line {area_no}.{line_no} in this installation")
        self.move_device(
            project_id, device_id, self._first_segment(state, line).id, octet
        )

    # --- internals --------------------------------------------------------

    def _links(self, rows: list[ComObjectLink]) -> list[LinkInfo]:
        return [
            LinkInfo(
                id=r.id,
                com_object_id=r.com_object_id,
                group_address_id=r.group_address_id,
                is_sending=r.is_sending,
            )
            for r in rows
        ]

    def _ga_info(self, ga: GroupAddress, style: GroupAddressStyle) -> GroupAddressInfo:
        return GroupAddressInfo(
            id=ga.id,
            address=ga.address,
            text=format_ga(ga.address, style),
            name=ga.name,
            datapoint_type=ga.datapoint_type,
            links=[link.com_object_id for link in ga.links],
            description=ga.description,
            comment=ga.comment,
            data_secure=ga.data_secure,
        )

    def _range_info(
        self, group_range: GroupRange, style: GroupAddressStyle
    ) -> GroupRangeInfo:
        return GroupRangeInfo(
            id=group_range.id,
            name=group_range.name,
            range_start=group_range.range_start,
            range_end=group_range.range_end,
            children=[
                self._range_info(child, style)
                for child in sorted(group_range.children, key=lambda c: c.range_start)
            ],
            group_addresses=[
                self._ga_info(ga, style)
                for ga in sorted(group_range.group_addresses, key=lambda g: g.address)
            ],
        )

    def _space_info(self, space: Space, style: GroupAddressStyle) -> SpaceInfo:
        return SpaceInfo(
            id=space.id,
            name=space.name,
            space_type=space.space_type,
            number=space.number,
            usage_text=space.usage_text,
            description=space.description,
            children=[
                self._space_info(child, style)
                for child in sorted(space.children, key=lambda c: (c.order, c.id))
            ],
            devices=[self._space_device_info(device) for device in space.devices],
            functions=[
                self._function_info(fn, style)
                for fn in sorted(space.functions, key=lambda f: (f.order, f.id))
            ],
        )

    def _space_device_info(self, device: Device) -> SpaceDeviceInfo:
        return SpaceDeviceInfo(
            id=device.id,
            name=device.name,
            individual_address=self._compose_ia(device),
            description=device.description,
            product_name=device.product_name,
            hardware_name=device.hardware_name,
            manufacturer_name=device.manufacturer_name,
        )

    def _function_info(
        self, function: Function, style: GroupAddressStyle
    ) -> FunctionInfo:
        return FunctionInfo(
            id=function.id,
            name=function.name,
            function_type=function.function_type,
            usage_text=function.usage_text,
            group_addresses=[
                FunctionGroupAddressInfo(
                    id=link.id,
                    group_address_id=link.group_address_id,
                    text=format_ga(link.group_address.address, style),
                    role=link.role,
                )
                for link in function.group_addresses
            ],
        )

    def _register(self, project_id: str, engine: Engine, session: Session) -> None:
        self._projects[project_id] = _Open(engine, session, EventStore(session))

    def _state(self, project_id: str) -> _Open:
        return self._projects[project_id]

    def _installation(self, state: _Open, index: int) -> Installation:
        inst = state.session.query(Installation).filter_by(index=index).first()
        if inst is None:
            raise KeyError(f"No installation with index {index}")
        return inst

    def _style(self, state: _Open) -> GroupAddressStyle:
        project = state.session.query(Project).first()
        assert project is not None
        return GroupAddressStyle(project.group_address_style)

    def _compose_ia(self, device: Device) -> str | None:
        if device.address is None:
            return None
        line = device.segment.line
        return format_ia(line.area.address, line.address, device.address)

    def _first_segment(self, state: _Open, line: Line) -> Segment:
        segment = (
            state.session.query(Segment)
            .filter_by(line_id=line.id)
            .order_by(Segment.id)
            .first()
        )
        if segment is None:
            raise KeyError(f"Line {line.id} has no segment")
        return segment

    def _check_unique_address(
        self,
        state: _Open,
        segment_id: int,
        address: int,
        exclude: int | None = None,
    ) -> None:
        segment = state.session.get(Segment, segment_id)
        if segment is None:
            raise KeyError(f"No segment with id {segment_id}")
        query = (
            state.session.query(Device)
            .join(Segment, Device.segment_id == Segment.id)
            .filter(Segment.line_id == segment.line_id, Device.address == address)
        )
        if exclude is not None:
            query = query.filter(Device.id != exclude)
        clash = query.first()
        if clash is not None:
            raise ValueError(
                f"Individual address {address} already used on this line by device {clash.id}"
            )
