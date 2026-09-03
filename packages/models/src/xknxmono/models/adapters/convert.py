"""Convert per-version `files.vXX` model instances into the unified `intermediate` model.

The engine is a reflective field-copy: for each target field it copies the same-named source
field, recursing into nested dataclasses and lists. xsdata names fields identically across
versions, so this handles the bulk automatically. Genuine divergences — captured from analysing
the schemas — are handled by per-type override functions registered in OVERRIDES, plus a
universal rule that synthesises a PUID where the unified model requires one but the source
version predates it.

Nothing here changes the intermediate model; every version-specific quirk lives in an override.
"""

# This is the reflective field-copy engine: it walks arbitrary per-version `files.vXX` dataclasses
# via getattr, so `src` is intentionally `Any` and the unknown-type rules don't apply here. The
# @override-decorated handlers are registered into OVERRIDES by the decorator and only invoked
# through that table, so their module-level names also read as unused.
# pyright: reportUnusedFunction=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportUnknownMemberType=false
from __future__ import annotations

import types
import typing
from collections.abc import Callable
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, get_args, get_origin

if TYPE_CHECKING:
    import structlog


class ConversionError(Exception):
    """Raised when a source value cannot be honestly mapped into the unified model."""


class _NullLogger:
    """No-op stand-in so the converter has zero runtime logging dependency. Callers that want the
    conversion trace inject a real structlog logger via `Context(logger=...)`; the apps that do so
    already depend on structlog. The structlog-style API (`bind` + level methods taking an event
    string and arbitrary kwargs) is mirrored here so injected and default loggers are interchangeable."""

    def bind(self, **_kw: Any) -> _NullLogger:
        return self

    def debug(self, *_a: Any, **_kw: Any) -> None: ...
    def info(self, *_a: Any, **_kw: Any) -> None: ...
    def warning(self, *_a: Any, **_kw: Any) -> None: ...
    def error(self, *_a: Any, **_kw: Any) -> None: ...


@dataclass(slots=True)
class PuidAllocator:
    """Hands out synthetic PUIDs for pre-v12 projects, which have no PUID of their own.

    Values are sequential per conversion. They are fabricated — a v10/v11 file carries no real
    PUIDs, so within one converted project every PUID here is synthetic and internally unique.
    """

    _next: int = 1

    def allocate(self) -> int:
        value = self._next
        self._next += 1
        return value


@dataclass(slots=True)
class Context:
    version: str
    puid: PuidAllocator = field(default_factory=PuidAllocator)
    # A structlog logger when the caller injects one; a no-op otherwise (logging is opt-in).
    logger: structlog.typing.FilteringBoundLogger = field(default_factory=_NullLogger)  # type: ignore[assignment]

    def __post_init__(self) -> None:
        # Every event from this conversion carries the source version automatically.
        self.logger = self.logger.bind(version=self.version)


# type key (Meta.name, else class name) -> override producing {field_name: value}. Overrides run
# BEFORE the generic copy and OWN the fields they return (the generic pass skips those fields).
OverrideFn = Callable[[Context, Any], dict[str, Any]]
OVERRIDES: dict[str, OverrideFn] = {}


def override(type_key: str) -> Callable[[OverrideFn], OverrideFn]:
    def register(fn: OverrideFn) -> OverrideFn:
        OVERRIDES[type_key] = fn
        return fn

    return register


def type_key(cls: type) -> str:
    meta = getattr(cls, "Meta", None)
    return (getattr(meta, "name", None) if meta else None) or cls.__name__


# Field renames between the version models and the unified model: target_type_key ->
# {target_field: source_field}. The generic copy consults this when a same-named source field is
# absent, then converts the value with the correct target type — so renames of both scalars and
# nested dataclasses are handled uniformly. (Old versions used capital-'In' casing: AddInData,
# AddInId; the unified model uses the v12+ lowercase forms.)
ALIASES: dict[str, dict[str, str]] = {
    "Project_t": {"addin_data": "add_in_data"},
    "ProjectAddinData": {"addin_data": "add_in_data"},
    "AddinData_t": {"addin_id": "add_in_id"},
    # v13→v14 renames (old versions used the left-hand source names):
    "ProjectInstallationsInstallation": {
        "locations": "buildings"
    },  # Buildings → Locations
    "Locations_t": {"space": "building_part"},  # BuildingPart → Space
    "Space_t": {"space": "building_part"},  # recursive Space child
    # v14→v20 rename:
    "DeviceInstance_t": {
        "is_activity_calculated": "is_communication_object_visibility_calculated"
    },
}


# --- type-hint resolution -------------------------------------------------

_hints_cache: dict[type, dict[str, Any]] = {}


def _hints(cls: type) -> dict[str, Any]:
    if cls not in _hints_cache:
        _hints_cache[cls] = typing.get_type_hints(cls)
    return _hints_cache[cls]


def _unwrap(hint: Any) -> tuple[bool, Any]:
    """Return (is_list, base_type) with Optional/Union[..., None] stripped."""

    def strip_optional(h: Any) -> Any:
        if get_origin(h) in (typing.Union, types.UnionType):
            args = [a for a in get_args(h) if a is not type(None)]
            if len(args) == 1:
                return args[0]
        return h

    hint = strip_optional(hint)
    if get_origin(hint) is list:
        (arg,) = get_args(hint)
        return True, strip_optional(arg)
    return False, hint


# --- core converter -------------------------------------------------------


def _union_dataclass_members(hint: Any) -> list[type]:
    """The dataclass members of a Union hint (xs:choice), or [] if it isn't such a union."""
    if get_origin(hint) in (typing.Union, types.UnionType):
        return [a for a in get_args(hint) if isinstance(a, type) and is_dataclass(a)]
    return []


def _convert_choice(
    ctx: Context, value: Any, members: list[type], is_list: bool
) -> Any:
    """Convert xs:choice content: match each source item to the IR union member with the same
    type key (Meta.name) and convert it. Items with no IR counterpart are passed through."""
    by_key = {type_key(m): m for m in members}

    def one(item: Any) -> Any:
        target = by_key.get(type_key(type(item)))
        return convert(ctx, item, target) if target is not None else item

    return [one(v) for v in value] if is_list else one(value)


def convert(ctx: Context, src: Any, target_cls: type) -> Any:
    """Build a `target_cls` instance from `src`: overrides first, then copy same-named fields."""
    hints = _hints(target_cls)
    key = type_key(target_cls)
    ctx.logger.debug("convert", src=type(src).__name__, target=key)
    ov = OVERRIDES.get(key)
    produced = ov(ctx, src) if ov is not None else {}
    if produced:
        ctx.logger.debug("convert.override", target=key, owned=sorted(produced))
    kwargs: dict[str, Any] = dict(produced)
    aliases = ALIASES.get(key, {})

    for f in fields(target_cls):
        if f.name in kwargs:  # owned by an override
            continue
        src_name = f.name if hasattr(src, f.name) else aliases.get(f.name)
        if src_name is None or not hasattr(
            src, src_name
        ):  # target-only; default / puid rule
            continue
        src_val = getattr(src, src_name)
        if src_val is None:
            continue
        is_list, base = _unwrap(hints.get(f.name, f.type))
        members = _union_dataclass_members(base)
        if members:  # xs:choice — convert each member to its matching IR union type
            kwargs[f.name] = _convert_choice(ctx, src_val, members, is_list)
        elif isinstance(base, type) and is_dataclass(base):
            kwargs[f.name] = (
                [convert(ctx, v, base) for v in src_val]
                if is_list
                else convert(ctx, src_val, base)
            )
        elif isinstance(base, type) and issubclass(base, Enum):
            if is_list:
                kwargs[f.name] = [
                    base(v.value) if isinstance(v, Enum) and type(v) is not base else v
                    for v in src_val
                ]
            else:
                kwargs[f.name] = (
                    base(src_val.value)
                    if isinstance(src_val, Enum) and type(src_val) is not base
                    else src_val
                )
        else:
            kwargs[f.name] = src_val

    # Universal: synthesise a PUID where the unified model requires one but the source lacked it.
    if any(f.name == "puid" for f in fields(target_cls)) and kwargs.get("puid") is None:
        kwargs["puid"] = ctx.puid.allocate()
        ctx.logger.debug("convert.puid_synth", target=key, puid=kwargs["puid"])

    return target_cls(**kwargs)


# --- captured overrides (one per real divergence found while analysing the schemas) ---


@override("MasterData_t")
def _master_data(ctx: Context, src: Any) -> dict[str, Any]:
    """Pre-v12 master data (project/10, /11) carries no ``Id`` attribute, but the unified model
    requires one. Synthesise the canonical ``MD-1`` id ETS uses; the value is not referenced
    downstream (the master is consumed for its datapoint/medium/manufacturer tables, not its id)."""
    if getattr(src, "id", None) is None:
        ctx.logger.debug("convert.master_data.id_synth", version=ctx.version)
        return {"id": "MD-1"}
    return {}


@override("GroupAddress_t")
def _group_address(ctx: Context, src: Any) -> dict[str, Any]:
    """v10-v12 stored DatapointType as a list (IDREFS); the unified model is a single ref.
    Accept 0/1 entries; reject genuine multi-DPT records rather than silently dropping data."""
    dpt = getattr(src, "datapoint_type", None)
    if isinstance(dpt, list):
        if len(dpt) > 1:
            ctx.logger.error(
                "convert.group_address.multi_dpt",
                id=getattr(src, "id", "?"),
                count=len(dpt),
                refs=dpt,
            )
            raise ConversionError(
                f"GroupAddress {getattr(src, 'id', '?')}: {len(dpt)} DatapointType refs {dpt}; "
                "unified model allows one"
            )
        return {"datapoint_type": dpt[0] if dpt else None}
    return {}


@override("DeviceInstanceAdditionalAddresses")
def _additional_addresses(ctx: Context, src: Any) -> dict[str, Any]:
    """v10/v11 stored each additional address as element text (list[int]); v12+ wrap it in an
    <Address> element with an 'Address' attribute. Wrap the raw ints into the unified objects."""
    from xknxmono.models.intermediate.device_instance_t_additional_addresses_address import (
        DeviceInstanceAdditionalAddressesAddress as Addr,
    )

    vals = getattr(src, "address", None) or []
    if vals and all(isinstance(v, int) for v in vals):
        ctx.logger.info("convert.additional_addresses.wrapped_ints", count=len(vals))
        return {"address": [Addr(address=v) for v in vals]}
    return {}  # already in object form (v12+) — let the generic pass handle it


@override("DeviceInstanceBinaryDataBinaryData")
def _binary_data(ctx: Context, src: Any) -> dict[str, Any]:
    """v20 had AutoCopy (default false); v21+ renamed it to DoNotCopy with inverted polarity.
    Map the old flag across: DoNotCopy = not AutoCopy."""
    if hasattr(src, "auto_copy"):
        do_not_copy = not bool(src.auto_copy)
        ctx.logger.debug(
            "convert.binary_data.auto_copy_inverted", do_not_copy=do_not_copy
        )
        return {"do_not_copy": do_not_copy}
    return {}


@override("Hardware_t")
def _hardware(ctx: Context, src: Any) -> dict[str, Any]:
    """RF capability moved twice across versions, and the IR keeps it only per-Hardware2Program:
      - ≤v14 described it with RuntimeUnidirectional (transmit-only) + RFDeviceMode;
      - v20 split it into RFRxCapabilities + RFTxCapabilities attributes on Hardware_t;
      - v21 moved that pair down onto each Hardware2Program.
    Determine the pair from the source (derive it from RuntimeUnidirectional for ≤v14 — a
    transmitting device always has Tx, and Rx unless unidirectional; baseline value 'Ready', with
    RFDeviceMode preserved separately for finer detail) and push it onto every Hardware2Program
    that lacks its own. v21+ already carry it per-Hardware2Program — the generic copy handles those."""
    from xknxmono.models.intermediate.rfrx_capabilities_t import RfrxCapabilities
    from xknxmono.models.intermediate.rftx_capabilities_t import RftxCapabilities

    rftx = getattr(src, "rftx_capabilities", None)
    rfrx = getattr(src, "rfrx_capabilities", None)
    uni = getattr(src, "runtime_unidirectional", None)
    if (
        rftx is None and rfrx is None and uni is not None
    ):  # ≤v14: derive from RuntimeUnidirectional
        rftx = RftxCapabilities.READY
        rfrx = None if uni else RfrxCapabilities.READY

    if rftx is None and rfrx is None:
        return {}  # v21+ (already per-Hardware2Program) — generic copy handles it

    source = "runtime_unidirectional" if uni is not None else "hardware_attrs"
    h2ps = getattr(src, "hardware2_programs", None)
    if h2ps is None:
        ctx.logger.warning(
            "convert.hardware.rf_caps_dropped",
            reason="no Hardware2Program to host the capability",
            source=source,
        )
        return {}  # no program association to host the capability — nothing to carry it onto
    from xknxmono.models.intermediate.hardware_t_hardware2_programs import (
        HardwareHardware2Programs,
    )

    h2ps_out = convert(
        ctx, h2ps, HardwareHardware2Programs
    )  # own it so we can fill its children
    filled = 0
    for prog in getattr(h2ps_out, "hardware2_program", None) or []:
        if getattr(prog, "rftx_capabilities", None) is None:
            prog.rftx_capabilities = rftx
        if getattr(prog, "rfrx_capabilities", None) is None:
            prog.rfrx_capabilities = rfrx
        filled += 1
    ctx.logger.info(
        "convert.hardware.rf_caps_pushed_down",
        source=source,
        rftx=rftx,
        rfrx=rfrx,
        programs=filled,
    )
    return {"hardware2_programs": h2ps_out}


@override("ComObjectInstanceRef_t")
def _com_object_instance_ref(ctx: Context, src: Any) -> dict[str, Any]:
    """v14 had a Connectors element (a Send + zero-or-more Receive, each a GroupAddressRefId with an
    Acknowledge flag); v20 flattened it to the Links/Acknowledges RELIDREFS attributes. Rebuild
    them: Links = every linked group-address ref, Acknowledges = those flagged Acknowledge."""
    conn = getattr(src, "connectors", None)
    if conn is None:
        return {}  # v20+ already carry Links/Acknowledges
    entries = []
    send = getattr(conn, "send", None)
    if send is not None:
        entries.append(send)
    entries += list(getattr(conn, "receive", None) or [])
    links = [
        r for r in (getattr(e, "group_address_ref_id", None) for e in entries) if r
    ]
    acks = [
        getattr(e, "group_address_ref_id", None)
        for e in entries
        if getattr(e, "acknowledge", False) and getattr(e, "group_address_ref_id", None)
    ]
    out: dict[str, Any] = {}
    if links:
        out["links"] = links
    if acks:
        out["acknowledges"] = acks
    ctx.logger.info(
        "convert.com_object_ref.connectors_flattened",
        links=len(links),
        acknowledges=len(acks),
    )
    return out


def fake_hash(value: Any) -> bytes:
    """Placeholder for the KNX loaded-credential hashing algorithm, which we haven't identified.
    Raises so conversions that would need it fail loudly rather than fabricate a wrong hash."""
    raise NotImplementedError(
        f"loaded-credential hashing algorithm unknown; cannot hash {value!r}"
    )


@override("ParameterSeparator_t")
def _parameter_separator(ctx: Context, src: Any) -> dict[str, Any]:
    """≤v13 had a boolean HorizontalRuler; v14+ replaced it with the richer UIHint enum (which has
    a 'HorizontalRuler' value). Map a set ruler flag onto the enum."""
    if getattr(src, "horizontal_ruler", None) and getattr(src, "uihint", None) is None:
        from xknxmono.models.intermediate.parameter_separator_t_uihint import (
            ParameterSeparatorUihint,
        )

        ctx.logger.info("convert.parameter_separator.ruler_to_uihint")
        return {"uihint": ParameterSeparatorUihint.HORIZONTAL_RULER}
    return {}


@override("Security_t")
def _security(ctx: Context, src: Any) -> dict[str, Any]:
    """v14 replaced the plaintext Loaded* credentials with hashed forms. We keep both in the IR;
    when only the plaintext is present (≤v13), derive the hash. The algorithm is unknown, so this
    raises until it's identified rather than storing a bogus hash. The plaintext itself is kept
    (copied by the generic pass)."""
    out: dict[str, Any] = {}
    for plain, hashed in (
        ("loaded_device_authentication_code", "loaded_device_authentication_code_hash"),
        ("loaded_device_management_password", "loaded_device_management_password_hash"),
    ):
        pv = getattr(src, plain, None)
        if pv is not None and getattr(src, hashed, None) is None:
            out[hashed] = fake_hash(pv)
    return out


@override("TopologyAreaLine")
def _line(ctx: Context, src: Any) -> dict[str, Any]:
    """v21 introduced a Segment layer: devices + medium attrs moved from the flat line onto a
    Segment child. For pre-v21 flat lines, wrap that content into a single synthesized Segment so
    it lands at the modern location. (Line-level attrs stay on the line via the generic copy.)"""
    if getattr(src, "segment", None):
        return {}  # v21+ already segmented — generic copy handles it
    from xknxmono.models.intermediate.topology_t_area_line_segment import (
        TopologyAreaLineSegment as Seg,
    )

    hints = _hints(Seg)
    seg_kwargs: dict[str, Any] = {}
    for fname in (
        "device_instance",
        "bus_access",
        "additional_group_addresses",
        "medium_type_ref_id",
        "domain_address",
    ):
        val = getattr(src, fname, None)
        if val is None or val == []:
            continue
        is_list, base = _unwrap(hints[fname])
        if isinstance(base, type) and is_dataclass(base):
            seg_kwargs[fname] = (
                [convert(ctx, v, base) for v in val]
                if is_list
                else convert(ctx, val, base)
            )
        else:
            seg_kwargs[fname] = val
    # Synthesize the segment's own identity (distinct from the line's Id)
    seg_kwargs["id"] = f"{getattr(src, 'id', 'L')}-S1"
    seg_kwargs["number"] = 1
    seg_kwargs["puid"] = ctx.puid.allocate()
    ctx.logger.info(
        "convert.line.wrapped_into_segment",
        line=getattr(src, "id", "?"),
        segment=seg_kwargs["id"],
    )
    return {"segment": [Seg(**seg_kwargs)]}


@override("ProjectInstallationsInstallation")
def _installation(ctx: Context, src: Any) -> dict[str, Any]:
    """Two source→IR relocations for the Installation:
    - MulticastTTL moved from per-Line (v10/v11: Topology>Area>Line) to per-Installation (v14+).
      When the source lacks the installation-level value, lift it from the first line that has one.
    - BusAccess was an installation-wide default element (≤v14) that v20 removed; bus access is now
      configured per-Segment under Topology. Push the installation value down onto every Segment
      that doesn't already define its own (the per-line BusAccess, copied onto its Segment by
      `_line`, wins)."""
    out: dict[str, Any] = {}
    topo = getattr(src, "topology", None)

    # MulticastTTL lift (v10/v11 flat lines)
    if getattr(src, "multicast_ttl", None) is None:
        for area in getattr(topo, "area", None) or []:
            for line in getattr(area, "line", None) or []:
                ttl = getattr(line, "multicast_ttl", None)
                if ttl is not None:
                    out["multicast_ttl"] = ttl
                    ctx.logger.info(
                        "convert.installation.multicast_ttl_lifted", ttl=ttl
                    )
                    break
            if "multicast_ttl" in out:
                break

    # BusAccess push-down (≤v14 installation-level default → per-Segment fallback)
    src_ba = getattr(src, "bus_access", None)
    if src_ba is not None and topo is not None:
        from xknxmono.models.intermediate.bus_access_t import BusAccess
        from xknxmono.models.intermediate.topology_t import Topology

        topo_out = convert(
            ctx, topo, Topology
        )  # own topology so we can fill its segments
        for area in getattr(topo_out, "area", None) or []:
            for line in getattr(area, "line", None) or []:
                for seg in getattr(line, "segment", None) or []:
                    if getattr(seg, "bus_access", None) is None:
                        seg.bus_access = convert(ctx, src_ba, BusAccess)
                        ctx.logger.info(
                            "convert.installation.busaccess_pushed_down",
                            segment=getattr(seg, "id", "?"),
                        )
        out["topology"] = topo_out

    return out
