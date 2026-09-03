"""Import an ETS ``.knxproj`` archive into a fresh project SQLite document.

Parsing is delegated to the ``xknxproject`` library. A ``.knxproj`` bundles its application
program XMLs, so ``xknxproject`` resolves every device's com-object/parameter/module refs and its
group-address links straight from the archive — the toolkit catalog is *not* needed. That keeps this
importer inside ``xknx-project`` (which depends only on ``xknx-models``) without pulling in the
catalog/product layers.

The public ``parse()`` dict drops the ETS reference ids (``product_ref`` / ``hardware_program_ref``)
that a project :class:`~xknxmono.project.models.Device` requires, so we drive the internal
``XMLParser`` and read its populated ``devices`` / ``areas`` / ``group_ranges`` /
``group_addresses`` attributes instead.

The whole project is written directly through the ORM in one commit (like
:func:`~xknxmono.project.core.skeleton.seed_new_project`): an import is initial state, not a sequence
of undoable edits, so it produces a valid zero-event project — far faster than one event per row for
a large installation, and it preserves the ETS group-range names.
"""

from __future__ import annotations

import logging
import zlib
from pathlib import Path
from uuid import uuid4
from zipfile import BadZipFile

from sqlalchemy.orm import Session
from xknxproject.exceptions import InvalidPasswordException, UnexpectedFileContent
from xknxproject.models.knxproject import DPTType
from xknxproject.models.models import (
    ComObjectInstanceRef,
    DeviceInstance,
    XMLGroupRange,
    XMLSpace,
)
from xknxproject.xml import XMLParser
from xknxproject.zip.extractor import extract

from xknxmono.project.core.addressing import GroupAddressStyle
from xknxmono.project.db import make_engine, url_for
from xknxmono.project.models import (
    Area,
    ComObject,
    ComObjectLink,
    Device,
    Function,
    FunctionGroupAddress,
    GroupAddress,
    GroupRange,
    Installation,
    Line,
    ModuleInstance,
    Parameter,
    Project,
    Segment,
    Space,
)

logger = logging.getLogger(__name__)

_INSTALLATION_INDEX = 0


def import_knxproj(
    source: Path | str,
    dest: Path | str,
    *,
    password: str | None = None,
    language: str | None = None,
    project_id: str | None = None,
) -> str:
    """Parse ``source`` (a ``.knxproj``) and write it as a new project at ``dest``.

    ``password`` is the ETS project password (for encrypted ETS5/6 archives); ``language`` picks the
    translation (e.g. ``"de-DE"``), falling back to the project default. Returns the project id.

    Raises :class:`~xknxproject.exceptions.InvalidPasswordException` when the archive is protected
    and no/a wrong password was given (standard-zip encryption reports a wrong password only as a
    decompression error, so any parse failure with a password set is treated as a wrong password),
    and :class:`~xknxproject.exceptions.UnexpectedFileContent` when the file is not a readable
    ``.knxproj`` archive. An existing ``dest`` is overwritten (an import is a fresh project).
    """
    parser = _parse_checked(source, password, language)
    # ETS project IDs are "P-" + 4 hex digits (spec Project Scheme §4.2.3, e.g. "P-02D7"); a longer
    # id yields a non-conformant P-XXXXXXXX folder that ETS can refuse to import.
    pid = project_id or f"P-{uuid4().hex[:4].upper()}"
    logger.debug(
        "import_knxproj: source=%s dest=%s pid=%s language=%s encrypted=%s",
        source,
        dest,
        pid,
        language,
        password is not None,
    )
    # An import always produces a new project; start from a clean file so re-importing over an
    # existing target does not clash with its rows. Done only after a successful parse, so a failed
    # import (e.g. wrong password) never destroys an existing project.
    dest_path = Path(dest)
    dest_path.unlink(missing_ok=True)
    engine = make_engine(url_for(dest_path))
    try:
        with Session(engine) as session:
            _build(session, parser, pid)
            session.commit()
    finally:
        engine.dispose()
    logger.debug("import_knxproj done: pid=%s -> %s", pid, dest)
    return pid


def _parse_checked(
    source: Path | str, password: str | None, language: str | None
) -> XMLParser:
    """Parse, normalising the assorted low-level failure modes into a clear, typed error."""
    try:
        return _parse(source, password, language)
    except InvalidPasswordException:
        raise  # protected + no password (extractor reports this eagerly)
    except (BadZipFile, zlib.error, RuntimeError) as e:
        # Standard-zip (ETS4/5) encryption has only a one-byte password check: a wrong password may
        # fail the header check (RuntimeError) or slip through and fail decompression later
        # (zlib.error). With a password set, treat any such failure as a wrong password.
        if password is not None:
            raise InvalidPasswordException("Invalid password.") from e
        raise UnexpectedFileContent(f"Not a readable .knxproj archive: {e}") from e


def _parse(source: Path | str, password: str | None, language: str | None) -> XMLParser:
    with extract(Path(source), password) as contents:
        parser = XMLParser(contents)
        parser.parse(
            language
        )  # populates parser.* ; the returned dict drops the ref ids we need
    logger.debug(
        "parsed knxproj '%s': %d devices, %d group addresses",
        parser.project_info.name,
        len(parser.devices),
        len(parser.group_addresses),
    )
    return parser


def _build(session: Session, parser: XMLParser, pid: str) -> None:
    info = parser.project_info
    session.add(
        Project(
            id=pid,
            name=info.name,
            group_address_style=_style(info.group_address_style.value),
            guid=info.guid,
            created_by=info.created_by,
            last_modified=info.last_modified or "",
            schema_version=info.schema_version,
            tool_version=info.tool_version,
        )
    )

    installation = Installation(index=_INSTALLATION_INDEX, name="")
    session.add(installation)

    state = _ImportState()
    _build_topology(installation, parser, state)
    _build_group_addresses(installation, parser, state)
    _build_links(state)
    _build_spaces(installation, parser, state)


def _style(value: str) -> GroupAddressStyle:
    try:
        return GroupAddressStyle(value)
    except ValueError:
        return GroupAddressStyle.THREE_LEVEL


# --- topology + devices ---------------------------------------------------


def _build_topology(
    installation: Installation, parser: XMLParser, state: _ImportState
) -> None:
    for xarea in parser.areas:
        area = Area(address=xarea.address, name=xarea.name)
        installation.areas.append(area)
        for xline in xarea.lines:
            line = Line(
                address=xline.address,
                name=xline.name,
                # getattr: newer xknxproject (KNX PR #651) exposes coupler pass-through addresses as
                # a list of ints; store comma-separated. Default empty on older versions.
                additional_group_addresses=",".join(
                    str(a) for a in getattr(xline, "additional_group_addresses", [])
                ),
            )
            area.lines.append(line)
            segment = Segment(number=0, medium_type=xline.medium_type)
            line.segments.append(segment)
            for xdevice in xline.devices:
                try:
                    segment.devices.append(_build_device(xdevice, state))
                except Exception as e:
                    # Partial load: a single malformed device must not abort the whole import.
                    logger.warning(
                        "skipping malformed device on import",
                        extra={"address": getattr(xdevice, "individual_address", "?")},
                    )
                    logger.debug("device import error: %s: %s", type(e).__name__, e)


def _build_device(xdevice: DeviceInstance, state: _ImportState) -> Device:
    com_objects: list[ComObject] = []
    for coir in xdevice.com_object_instance_refs:
        row = _build_com_object(coir)
        com_objects.append(row)
        state.register_com_object(coir, row)
    device = Device(
        address=xdevice.address,
        name=xdevice.name,
        product_ref_id=xdevice.product_ref,
        hardware2program_ref_id=xdevice.hardware_program_ref,
        description=xdevice.description,
        order_number=xdevice.order_number,
        hardware_name=xdevice.hardware_name,
        product_name=xdevice.product_name,
        manufacturer_name=xdevice.manufacturer_name,
        # Commissioning state (getattr with defaults: optional, and only present on newer
        # xknxproject; a missing attribute must not fail the whole device import).
        serial_number=getattr(xdevice, "serial_number", "") or "",
        last_download=getattr(xdevice, "last_download", None),
        individual_address_loaded=getattr(xdevice, "individual_address_loaded", False),
        application_program_loaded=getattr(
            xdevice, "application_program_loaded", False
        ),
        communication_part_loaded=getattr(xdevice, "communication_part_loaded", False),
        medium_config_loaded=getattr(xdevice, "medium_config_loaded", False),
        parameters_loaded=getattr(xdevice, "parameters_loaded", False),
        com_objects=com_objects,
        parameters=[
            Parameter(ref_id=ref, value=p.value or "")
            for ref, p in xdevice.parameter_instance_refs.items()
        ],
        module_instances=[
            ModuleInstance(instance_id=mi.identifier, ref_id=mi.module_def_id)
            for mi in xdevice.module_instances
        ],
    )
    state.register_device(xdevice.individual_address, device)
    return device


def _build_com_object(coir: ComObjectInstanceRef) -> ComObject:
    return ComObject(
        ref_id=coir.com_object_ref_id or coir.ref_id,
        channel_id=coir.channel,
        read_flag=coir.read_flag,
        write_flag=coir.write_flag,
        communication_flag=coir.communication_flag,
        transmit_flag=coir.transmit_flag,
        update_flag=coir.update_flag,
        read_on_init_flag=coir.read_on_init_flag,
    )


# --- group ranges + addresses + links -------------------------------------


def _build_group_addresses(
    installation: Installation, parser: XMLParser, state: _ImportState
) -> None:
    ranges: list[GroupRange] = []
    _build_ranges(installation, parser.group_ranges, None, ranges)

    for xga in parser.group_addresses:
        group_range = _range_for(ranges, xga.raw_address)
        if group_range is None:
            continue  # a group address outside every range would violate the schema; skip it
        ga = GroupAddress(
            address=xga.raw_address,
            name=xga.name,
            datapoint_type=_dpt(xga.dpt),
            description=xga.description,
            comment=xga.comment,
            data_secure=bool(xga.data_secure_key),
            # getattr: only present on newer xknxproject (KNX PR #651); default False otherwise.
            unfiltered=getattr(xga, "unfiltered", False),
        )
        group_range.group_addresses.append(ga)
        state.register_group_address(xga.identifier, ga)


def _build_ranges(
    installation: Installation,
    xranges: list[XMLGroupRange],
    parent: GroupRange | None,
    collected: list[GroupRange],
) -> None:
    for xr in xranges:
        gr = GroupRange(
            range_start=xr.range_start,
            range_end=xr.range_end,
            name=xr.name,
            parent=parent,
            unfiltered=getattr(xr, "unfiltered", False),
        )
        installation.group_ranges.append(gr)
        collected.append(gr)
        _build_ranges(installation, xr.group_ranges, gr, collected)


def _range_for(ranges: list[GroupRange], address: int) -> GroupRange | None:
    """The smallest (leaf) range that contains ``address``."""
    best: GroupRange | None = None
    for gr in ranges:
        if gr.range_start <= address <= gr.range_end and (
            best is None
            or (gr.range_end - gr.range_start) < (best.range_end - best.range_start)
        ):
            best = gr
    return best


def _build_links(state: _ImportState) -> None:
    for coir, com_object in state.com_objects:
        for i, link in enumerate(coir.links or []):
            ga = state.group_addresses.get(link)
            if ga is None:
                continue  # link to a group address not present in the project; drop it
            com_object.links.append(
                ComObjectLink(group_address=ga, is_sending=(i == 0))
            )


# --- spaces (buildings/rooms) + functions ---------------------------------


def _build_spaces(
    installation: Installation, parser: XMLParser, state: _ImportState
) -> None:
    space_by_identifier: dict[str, Space] = {}
    for order, xspace in enumerate(parser.spaces):
        _build_space(installation, xspace, None, order, state, space_by_identifier)

    for order, func in enumerate(parser.functions):
        space = space_by_identifier.get(func.space_id)
        if space is None:
            continue  # function references a space that was not present
        function = Function(
            function_type=func.function_type,
            name=func.name,
            usage_text=func.usage_text,
            order=order,
        )
        for ref in func.group_addresses:
            ga = state.group_addresses.get(ref.ref_id)
            if ga is not None:
                function.group_addresses.append(
                    FunctionGroupAddress(group_address=ga, role=ref.role)
                )
        space.functions.append(function)


def _build_space(
    installation: Installation,
    xspace: XMLSpace,
    parent: Space | None,
    order: int,
    state: _ImportState,
    space_by_identifier: dict[str, Space],
) -> None:
    space = Space(
        space_type=xspace.space_type.value,
        name=xspace.name,
        number=xspace.number,
        usage_text=xspace.usage_text,
        description=xspace.description,
        order=order,
        parent=parent,
    )
    installation.spaces.append(space)
    space_by_identifier[xspace.identifier] = space
    for ia in xspace.devices:
        device = state.device_by_ia.get(ia)
        if device is not None:
            device.space = space
    for child_order, child in enumerate(xspace.spaces):
        _build_space(
            installation, child, space, child_order, state, space_by_identifier
        )


def _dpt(dpt: DPTType | None) -> str | None:
    if dpt is None:
        return None
    main = dpt["main"]
    sub = dpt["sub"]
    return f"DPST-{main}-{sub}" if sub is not None else f"DPT-{main}"


class _ImportState:
    """Cross-references built while walking devices, used to wire links once addresses exist."""

    def __init__(self) -> None:
        self.com_objects: list[tuple[ComObjectInstanceRef, ComObject]] = []
        self.group_addresses: dict[str, GroupAddress] = {}
        self.device_by_ia: dict[str, Device] = {}

    def register_com_object(self, coir: ComObjectInstanceRef, row: ComObject) -> None:
        self.com_objects.append((coir, row))

    def register_group_address(self, identifier: str, row: GroupAddress) -> None:
        self.group_addresses[identifier] = row

    def register_device(self, individual_address: str, row: Device) -> None:
        self.device_by_ia[individual_address] = row
