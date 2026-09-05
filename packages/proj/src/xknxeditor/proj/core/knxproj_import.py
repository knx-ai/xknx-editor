"""Import a ``.knxproj`` archive into a fresh project SQLite document.

Parsing is delegated to the ``xknxproject`` library. A ``.knxproj`` bundles its application
program XMLs, so ``xknxproject`` resolves every device's com-object/parameter/module refs and its
group-address links straight from the archive — the catalog is *not* needed. That keeps this
importer inside ``xknxeditor-proj`` (which depends only on ``xknxeditor-namespaces``) without pulling in the
catalog/product layers.

The public ``parse()`` dict drops the .knxproj reference ids (``product_ref`` / ``hardware_program_ref``)
that a project :class:`~xknxeditor.proj.models.Device` requires, so we drive the internal
``XMLParser`` and read its populated ``devices`` / ``areas`` / ``group_ranges`` /
``group_addresses`` attributes instead.

The whole project is written directly through the ORM in one commit (like
:func:`~xknxeditor.proj.core.skeleton.seed_new_project`): an import is initial state, not a sequence
of undoable edits, so it produces a valid zero-event project — far faster than one event per row for
a large installation, and it preserves the original group-range names.
"""

from __future__ import annotations

import base64
import logging
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Any, Protocol
from uuid import uuid4
from xml.etree import ElementTree as ET
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

from xknxeditor.proj.core.addressing import GroupAddressStyle
from xknxeditor.proj.db import make_engine, url_for
from xknxeditor.proj.models import (
    Area,
    ComObject,
    ComObjectLink,
    Device,
    DeviceBinaryData,
    Function,
    FunctionGroupAddress,
    GroupAddress,
    GroupRange,
    Installation,
    Line,
    ModuleInstance,
    Parameter,
    Project,
    ProjectTrace,
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

    ``password`` is the project password (for encrypted archives); ``language`` picks the
    translation (e.g. ``"de-DE"``), falling back to the project default. Returns the project id.

    Raises :class:`~xknxproject.exceptions.InvalidPasswordException` when the archive is protected
    and no/a wrong password was given (standard-zip encryption reports a wrong password only as a
    decompression error, so any parse failure with a password set is treated as a wrong password),
    and :class:`~xknxproject.exceptions.UnexpectedFileContent` when the file is not a readable
    ``.knxproj`` archive. An existing ``dest`` is overwritten (an import is a fresh project).
    """
    parser, extras = _parse_checked(source, password, language)
    # Project IDs are "P-" + 4 hex digits (spec Project Scheme §4.2.3, e.g. "P-02D7"); a longer
    # id yields a non-conformant P-XXXXXXXX folder that the importer can refuse to import.
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
            _build(session, parser, pid, extras)
            session.commit()
    finally:
        engine.dispose()
    logger.debug("import_knxproj done: pid=%s -> %s", pid, dest)
    return pid


def _parse_checked(
    source: Path | str, password: str | None, language: str | None
) -> tuple[XMLParser, _RawExtras]:
    """Parse, normalising the assorted low-level failure modes into a clear, typed error."""
    try:
        return _parse(source, password, language)
    except InvalidPasswordException:
        raise  # protected + no password (extractor reports this eagerly)
    except (BadZipFile, zlib.error, RuntimeError) as e:
        # Standard-zip encryption has only a one-byte password check: a wrong password may
        # fail the header check (RuntimeError) or slip through and fail decompression later
        # (zlib.error). With a password set, treat any such failure as a wrong password.
        if password is not None:
            raise InvalidPasswordException("Invalid password.") from e
        raise UnexpectedFileContent(f"Not a readable .knxproj archive: {e}") from e


@dataclass(frozen=True, slots=True)
class _BinaryEntry:
    """A DeviceInstance ``<BinaryData>``: metadata + the raw payload from its ``.dat`` file."""

    name: str
    data: bytes
    ref_id: str = ""
    do_not_copy: bool = False


@dataclass(frozen=True, slots=True)
class _TraceEntry:
    """A ``ProjectInformation/ProjectTraces/ProjectTrace`` entry, captured verbatim.

    ``comment`` is stored exactly as written by ETS (encrypted); we neither decrypt nor re-encrypt.
    """

    date: str
    user_name: str
    comment: str


# Per-device data read straight from the raw project XML because xknxproject drops it. Keyed by
# DeviceInstance @Id (== xknxproject's ``DeviceInstance.identifier``).
BinaryDataMap = dict[str, list[_BinaryEntry]]
# instance_id -> (RepeatIndex, [{"ref_id", "value"}]) for that ModuleInstance's <Arguments>.
ModuleArgs = dict[str, tuple[str, list[dict[str, str]]]]
ModuleArgsMap = dict[str, ModuleArgs]


class _ProjectContents(Protocol):
    """The slice of xknxproject's ``KNXProjContents`` that ``_read_device_extras`` needs."""

    def open_project_0(self) -> IO[bytes]: ...


class _RawExtras:
    """Per-device data captured from the raw project XML (not surfaced by xknxproject)."""

    def __init__(self) -> None:
        # DeviceInstance @Id -> [(BinaryData Name, decoded bytes)]
        self.binary_data: BinaryDataMap = {}
        # DeviceInstance @Id -> {ModuleInstance @Id -> (RepeatIndex, argument list)}
        self.module_args: ModuleArgsMap = {}
        # ETS project-log entries, in document order (captured verbatim; comment stays encrypted).
        self.traces: list[_TraceEntry] = []


def _parse(
    source: Path | str, password: str | None, language: str | None
) -> tuple[XMLParser, _RawExtras]:
    with extract(Path(source), password) as contents:
        parser = XMLParser(contents)
        parser.parse(
            language
        )  # populates parser.* ; the returned dict drops the ref ids we need
        # xknxproject exposes neither per-device <BinaryData> (where DCAs persist state, e.g. the MDT
        # DALI "DaliGC16-Backup-Store") nor the <ModuleInstances> Arguments/RepeatIndex needed to
        # re-emit module-based devices on export, so read both from the raw installation XML while the
        # archive is still open.
        extras = _read_device_extras(contents)
        extras.traces = _read_project_traces(contents)
    logger.debug(
        "parsed knxproj '%s': %d devices, %d group addresses, %d w/ binary data, %d w/ modules, %d traces",
        parser.project_info.name,
        len(parser.devices),
        len(parser.group_addresses),
        len(extras.binary_data),
        len(extras.module_args),
        len(extras.traces),
    )
    return parser, extras


def _read_device_extras(contents: _ProjectContents) -> _RawExtras:
    """Extract each DeviceInstance's ``<BinaryData>`` and ``<ModuleInstances>`` from the raw ``0.xml``.

    ``contents`` is xknxproject's ``KNXProjContents``; ``open_project_0`` yields the installation
    XML. Best-effort: any parse failure leaves the result empty rather than aborting the import.
    """
    extras = _RawExtras()
    try:
        with contents.open_project_0() as handle:
            root = ET.parse(handle).getroot()
    except Exception as e:  # these extras are optional; never fail the import for them
        logger.debug("could not read raw 0.xml for device extras: %s", e)
        return extras
    # Namespace-agnostic: match on the local tag name so we don't depend on the schema version.
    for device in root.iter():
        if _localname(device.tag) != "DeviceInstance":
            continue
        device_id = device.get("Id")
        if not device_id:
            continue
        binary = _read_binary_data(device, device_id, contents)
        if binary:
            extras.binary_data[device_id] = binary
        modules = _read_module_args(device)
        if modules:
            extras.module_args[device_id] = modules
    return extras


def _read_project_traces(contents: _ProjectContents) -> list[_TraceEntry]:
    """Every ``ProjectInformation/ProjectTraces/ProjectTrace`` from the raw ``project.xml``.

    xknxproject does not surface the project log, so read it from the raw project metadata while the
    archive is open. Best-effort: any failure yields an empty list rather than aborting the import.
    The ``Comment`` is kept verbatim (ETS encrypts it); order follows the document.
    """
    raw = _read_project_file(contents, "project.xml")
    if raw is None:
        return []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        logger.debug("could not parse project.xml for project traces: %s", e)
        return []
    traces: list[_TraceEntry] = []
    for elem in root.iter():
        if _localname(elem.tag) != "ProjectTrace":
            continue
        traces.append(
            _TraceEntry(
                date=elem.get("Date") or "",
                user_name=elem.get("UserName") or "",
                comment=elem.get("Comment") or "",
            )
        )
    return traces


def _read_binary_data(
    device: ET.Element, device_id: str, contents: _ProjectContents
) -> list[_BinaryEntry]:
    """Every ``<BinaryData>`` entry on ``device`` with its payload.

    ETS stores the payload in ``P-XXXX/BinaryData/{Id}.dat`` (raw bytes), with the ``0.xml`` element
    carrying only metadata. Older/other writers may inline it as ``<Data>`` base64 — read that too.
    """
    entries: list[_BinaryEntry] = []
    for elem in device.iter():
        if _localname(elem.tag) != "BinaryData":
            continue
        name = elem.get("Name")
        entry_id = elem.get("Id")
        if name is None and entry_id is None:
            continue  # the wrapper element carries neither; only the entries do
        data = _binary_payload(elem, entry_id, contents)
        entries.append(
            _BinaryEntry(
                name=name or "",
                data=data,
                ref_id=elem.get("RefId") or "",
                do_not_copy=(elem.get("DoNotCopy") or "").lower() == "true",
            )
        )
    return entries


def _binary_payload(
    elem: ET.Element, entry_id: str | None, contents: _ProjectContents
) -> bytes:
    """The raw bytes for a ``<BinaryData>``: its external ``.dat`` file, or an inline ``<Data>``."""
    data_elem = next((c for c in elem if _localname(c.tag) == "Data"), None)
    if data_elem is not None and data_elem.text:
        try:
            return base64.b64decode(data_elem.text)
        except (ValueError, TypeError):
            logger.debug("skipping malformed inline BinaryData Data on %s", entry_id)
            return b""
    if entry_id:
        raw = _read_project_file(contents, f"BinaryData/{entry_id}.dat")
        if raw is not None:
            return raw
    return b""  # a RefId-only entry (content borrowed from the application program) has no file


def _read_project_file(contents: _ProjectContents, relpath: str) -> bytes | None:
    """Read a file from the project folder of the (possibly encrypted) archive; None if absent.

    Uses xknxproject's already-opened project archive (private attrs) so encrypted projects work
    too. Best-effort: any failure returns None rather than aborting the import.
    """
    archive: Any = getattr(contents, "_project_archive", None)
    base: str = getattr(contents, "_project_relative_path", "") or ""
    if archive is None:
        return None
    try:
        with archive.open(f"{base}{relpath}") as handle:
            data: bytes = handle.read()
            return data
    except (KeyError, OSError, RuntimeError):
        return None


def _read_module_args(device: ET.Element) -> ModuleArgs:
    """The ``RepeatIndex`` + ``<Arguments>`` of every ``<ModuleInstance>``, keyed by its ``@Id``."""
    result: ModuleArgs = {}
    for mi in device.iter():
        if _localname(mi.tag) != "ModuleInstance":
            continue
        mi_id = mi.get("Id")
        if not mi_id:
            continue
        args = [
            {"ref_id": ref, "value": arg.get("Value", "")}
            for arg in mi.iter()
            if _localname(arg.tag) == "Argument" and (ref := arg.get("RefId"))
        ]
        result[mi_id] = (mi.get("RepeatIndex", ""), args)
    return result


def _localname(tag: str) -> str:
    """The local part of a possibly namespaced ElementTree tag (``{ns}Name`` -> ``Name``)."""
    return tag.rsplit("}", 1)[-1]


def _build(session: Session, parser: XMLParser, pid: str, extras: _RawExtras) -> None:
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
            traces=[
                ProjectTrace(
                    project_id=pid,
                    date=t.date,
                    user_name=t.user_name,
                    comment=t.comment,
                )
                for t in extras.traces
            ],
        )
    )

    installation = Installation(index=_INSTALLATION_INDEX, name="")
    session.add(installation)

    state = _ImportState(extras)
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
    module_args = state.extras.module_args.get(xdevice.identifier, {})
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
            _build_module_instance(mi, module_args) for mi in xdevice.module_instances
        ],
        # Per-device <BinaryData> captured from the raw XML (keyed by DeviceInstance @Id), e.g. a
        # DCA's persisted state. Preserved verbatim so import -> export does not drop it.
        binary_data=[
            DeviceBinaryData(
                name=e.name,
                data=e.data,
                ref_id=e.ref_id,
                do_not_copy=e.do_not_copy,
            )
            for e in state.extras.binary_data.get(xdevice.identifier, [])
        ],
    )
    state.register_device(xdevice.individual_address, device)
    return device


def _build_module_instance(mi: object, module_args: ModuleArgs) -> ModuleInstance:
    """Build a ModuleInstance row, enriching it with the raw ``RepeatIndex``/``<Arguments>``.

    ``xknxproject`` only gives ``identifier``/``module_def_id``; the allocator arguments and repeat
    index come from ``module_args`` (captured from the raw XML, keyed by the on-disk ``@Id`` which
    equals ``identifier``), so a module-based device survives export.
    """
    repeat_index, arguments = module_args.get(mi.identifier, ("", []))  # type: ignore[attr-defined]
    return ModuleInstance(
        instance_id=mi.identifier,  # type: ignore[attr-defined]
        ref_id=mi.module_def_id,  # type: ignore[attr-defined]
        repeat_index=repeat_index,
        arguments=arguments,
    )


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

    def __init__(self, extras: _RawExtras | None = None) -> None:
        self.com_objects: list[tuple[ComObjectInstanceRef, ComObject]] = []
        self.group_addresses: dict[str, GroupAddress] = {}
        self.device_by_ia: dict[str, Device] = {}
        # Per-device BinaryData / module Arguments captured from the raw project XML.
        self.extras: _RawExtras = extras or _RawExtras()

    def register_com_object(self, coir: ComObjectInstanceRef, row: ComObject) -> None:
        self.com_objects.append((coir, row))

    def register_group_address(self, identifier: str, row: GroupAddress) -> None:
        self.group_addresses[identifier] = row

    def register_device(self, individual_address: str, row: Device) -> None:
        self.device_by_ia[individual_address] = row
