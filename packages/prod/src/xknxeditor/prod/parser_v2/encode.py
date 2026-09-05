from __future__ import annotations

import struct
from collections.abc import Mapping
from typing import NamedTuple

from xknxeditor.namespaces.intermediate import ApplicationProgram
from xknxeditor.namespaces.intermediate.application_program_static_t_parameters_parameter import (
    ApplicationProgramStaticParametersParameter,
)
from xknxeditor.namespaces.intermediate.application_program_static_t_parameters_union import (
    ApplicationProgramStaticParametersUnion,
)
from xknxeditor.namespaces.intermediate.memory_parameter_t import MemoryParameter
from xknxeditor.namespaces.intermediate.memory_union_t import MemoryUnion
from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_parameter import (
    ModuleDefStaticParametersParameter,
)
from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_parameter_memory import (
    ModuleDefStaticParametersParameterMemory,
)
from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_parameter_property import (
    ModuleDefStaticParametersParameterProperty,
)
from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_union import (
    ModuleDefStaticParametersUnion,
)
from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_union_memory import (
    ModuleDefStaticParametersUnionMemory,
)
from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_union_property import (
    ModuleDefStaticParametersUnionProperty,
)
from xknxeditor.namespaces.intermediate.module_t_numeric_arg import ModuleNumericArg
from xknxeditor.namespaces.intermediate.parameter_type_t_type_color import (
    ParameterTypeTypeColor,
)
from xknxeditor.namespaces.intermediate.parameter_type_t_type_color_space import (
    ParameterTypeTypeColorSpace,
)
from xknxeditor.namespaces.intermediate.parameter_type_t_type_date import (
    ParameterTypeTypeDate,
)
from xknxeditor.namespaces.intermediate.parameter_type_t_type_float import (
    ParameterTypeTypeFloat,
)
from xknxeditor.namespaces.intermediate.parameter_type_t_type_float_encoding import (
    ParameterTypeTypeFloatEncoding,
)
from xknxeditor.namespaces.intermediate.parameter_type_t_type_ipaddress import (
    ParameterTypeTypeIpaddress,
)
from xknxeditor.namespaces.intermediate.parameter_type_t_type_number import (
    ParameterTypeTypeNumber,
)
from xknxeditor.namespaces.intermediate.parameter_type_t_type_raw_data import (
    ParameterTypeTypeRawData,
)
from xknxeditor.namespaces.intermediate.parameter_type_t_type_restriction import (
    ParameterTypeTypeRestriction,
)
from xknxeditor.namespaces.intermediate.parameter_type_t_type_text import (
    ParameterTypeTypeText,
)
from xknxeditor.namespaces.intermediate.parameter_type_t_type_time import (
    ParameterTypeTypeTime,
)
from xknxeditor.namespaces.intermediate.property_parameter_t import PropertyParameter
from xknxeditor.namespaces.intermediate.property_union_t import PropertyUnion
from xknxeditor.namespaces.intermediate.union_parameter_t import UnionParameter

from .application_indexer import ApplicationIndexer
from .state import GlobalState, ModuleState


class MemWrite(NamedTuple):
    seg_id: str
    offset: int
    bit_offset: int
    param_id: str
    parameter_type: str
    value: str


class PropWrite(NamedTuple):
    object_index: int | None
    property_id: int
    occurrence: int
    offset: int
    bit_offset: int
    param_id: str
    parameter_type: str
    value: str


class Writes:
    __slots__ = ("mem", "prop")

    def __init__(self) -> None:
        self.mem: list[MemWrite] = []
        self.prop: list[PropWrite] = []


PropertyKey = tuple[int | None, int, int]  # keys: object_index, property_id, occurrence


def _program_little_endian(app: ApplicationProgram) -> bool:
    """Whether the application program encodes parameter values little-endian.

    Read from the static options' ``ParameterByteOrder`` (default big-endian).
    """
    options = getattr(app.static, "options", None)
    order = getattr(options, "parameter_byte_order", None)
    return order is not None and order.value == "LittleEndian"


def _write_bits(
    buf: bytearray, offset: int, bit_offset: int, size_in_bit: int, value: int
) -> None:
    """Pack value big-endian into buf at offset+bit_offset (bit 0 = byte MSB)."""
    start = offset * 8 + bit_offset
    for i in range(size_in_bit):
        pos = start + i
        bit_mask = 1 << (7 - pos % 8)
        if (value >> (size_in_bit - 1 - i)) & 1:
            buf[pos // 8] |= bit_mask
        else:
            buf[pos // 8] &= ~bit_mask


def _encode_value(
    str_value: str, size_in_bit: int, tc: object, *, little_endian: bool = False
) -> int | None:
    """Encode a parameter value string into the integer that ``_write_bits`` packs.

    Values are packed MSB-first. The default byte order is big-endian; when the
    application program selects little-endian (``ParameterByteOrder`` in its static
    options), the byte order of a multi-octet numeric value is reversed, matching
    the reference engine (which reverses the octets of integer and float values for
    a little-endian program). Ports the reference engine's per-type value encoders.
    """
    if isinstance(tc, (ParameterTypeTypeNumber, ParameterTypeTypeTime)):
        # A time value is stored as a plain integer in the type's unit.
        return _apply_byte_order(
            _encode_number(str_value, size_in_bit), size_in_bit, little_endian
        )

    if isinstance(tc, ParameterTypeTypeRestriction):
        return _encode_restriction(str_value, size_in_bit, tc, little_endian)

    if isinstance(tc, ParameterTypeTypeFloat):
        return _apply_byte_order(
            _encode_float(str_value, size_in_bit, tc), size_in_bit, little_endian
        )

    if isinstance(tc, ParameterTypeTypeText):
        return _encode_text(str_value, size_in_bit)

    if isinstance(tc, ParameterTypeTypeDate):
        return _encode_date(str_value, tc)

    if isinstance(tc, ParameterTypeTypeIpaddress):
        return _encode_ipaddress(str_value)

    if isinstance(tc, ParameterTypeTypeColor):
        return _encode_color(str_value, size_in_bit, tc)

    if isinstance(tc, ParameterTypeTypeRawData):
        return _encode_raw_data(str_value, size_in_bit, little_endian)

    return None


def _apply_byte_order(
    value: int | None, size_in_bit: int, little_endian: bool
) -> int | None:
    """Reverse the octet order of a byte-aligned multi-octet numeric ``value``.

    Only applies for a little-endian program and a whole-octet field (at least two
    octets); single-octet and sub-octet fields are unaffected.
    """
    if value is None or not little_endian or size_in_bit < 16 or size_in_bit % 8 != 0:
        return value
    n = size_in_bit // 8
    return int.from_bytes(value.to_bytes(n, "big")[::-1], "big")


def _encode_restriction(
    str_value: str,
    size_in_bit: int,
    tc: ParameterTypeTypeRestriction,
    little_endian: bool,
) -> int | None:
    """Encode an enumeration value of a restricted parameter type.

    An enumeration entry may carry an explicit ``BinaryValue`` (the exact octets to
    store, e.g. a priority ordering); that is written verbatim, big-endian, and is
    not subject to the program byte order. Entries without a binary value fall back
    to encoding the enumeration value as an integer (honouring the byte order).
    """
    for enumeration in tc.enumeration:
        if str(enumeration.value) == str_value:
            if enumeration.binary_value:
                return int.from_bytes(enumeration.binary_value, "big")
            break
    return _apply_byte_order(
        _encode_number(str_value, size_in_bit), size_in_bit, little_endian
    )


def _encode_number(str_value: str, size_in_bit: int) -> int | None:
    """Signed/unsigned integer, masked to ``size_in_bit`` (two's complement)."""
    try:
        v = int(str_value, 0) if str_value[:2].lower() == "0x" else int(str_value)
    except (ValueError, TypeError):
        return None
    return v & ((1 << size_in_bit) - 1)


def _encode_float(
    str_value: str, size_in_bit: int, tc: ParameterTypeTypeFloat
) -> int | None:
    try:
        f = float(str_value)
    except (ValueError, TypeError):
        return None
    if tc.encoding == ParameterTypeTypeFloatEncoding.DPT_9:
        # KNX DPT 9 (2 octet float): value = 0.01 * m * 2^exp, m = 11 bit signed
        # two's complement, sign in bit 15, exponent in bits 14..11.
        mantissa = round(f * 100)
        exp = 0
        while mantissa < -2048 or mantissa > 2047:
            mantissa >>= 1
            exp += 1
        if exp > 15:
            return None
        sign = 1 if mantissa < 0 else 0
        return (sign << 15) | (exp << 11) | (mantissa & 0x7FF)
    if tc.encoding == ParameterTypeTypeFloatEncoding.IEEE_754_SINGLE:
        return struct.unpack(">I", struct.pack(">f", f))[0]
    if tc.encoding == ParameterTypeTypeFloatEncoding.IEEE_754_DOUBLE:
        return struct.unpack(">Q", struct.pack(">d", f))[0]
    return None


def _encode_text(str_value: str, size_in_bit: int) -> int:
    """Code-page (Latin-1) text, truncated and zero-padded to the field width.

    Zero padding also provides the null terminator implicitly (the reference
    engine relies on the zero-initialised buffer for termination).
    """
    encoded = str_value.encode("latin-1", errors="replace")
    n_bytes = size_in_bit // 8
    padded = encoded[:n_bytes].ljust(n_bytes, b"\x00")
    return int.from_bytes(padded, "big")


def _encode_date(str_value: str, tc: ParameterTypeTypeDate) -> int | None:
    """KNX date: 3 octets day, month, year mod 100 (value ``YYYY-MM-DD``).

    When the type does not display the year, the year octet stays zero (the
    reference engine writes only day and month for that formatting).
    """
    parts = str_value.split("-")
    if len(parts) != 3:
        return None
    try:
        year, month, day = (int(p) for p in parts)
    except ValueError:
        return None
    year_octet = 0 if tc.display_the_year is False else year % 100
    return (day << 16) | (month << 8) | year_octet


def _encode_ipaddress(str_value: str) -> int | None:
    """IPv4 dotted-quad to 4 octets in network (big-endian) order."""
    parts = str_value.split(".")
    if len(parts) != 4:
        return None
    try:
        octets = [int(p) for p in parts]
    except ValueError:
        return None
    if any(o < 0 or o > 255 for o in octets):
        return None
    return int.from_bytes(bytes(octets), "big")


def _encode_color(
    str_value: str, size_in_bit: int, tc: ParameterTypeTypeColor
) -> int | None:
    """Colour from a ``#RRGGBB``/``#RRGGBBWW`` hex string, per the type's space.

    - RGB: three octets ``[R, G, B]``.
    - RGBW: four octets ``[R, G, B, W]``.
    - HSV: three octets ``[H, S, V]`` converted from the RGB value (H scaled to a
      single octet), matching the reference engine's RGB-to-HSV conversion.
    """
    try:
        raw = bytes.fromhex(str_value.lstrip("#"))
    except ValueError:
        return None
    if tc.space == ParameterTypeTypeColorSpace.RGBW:
        raw = raw[:4].ljust(4, b"\x00")
        return int.from_bytes(raw, "big")
    if len(raw) < 3:
        return None
    r, g, b = raw[0], raw[1], raw[2]
    if tc.space == ParameterTypeTypeColorSpace.HSV:
        h, s, v = _rgb_to_hsv(r, g, b)
        return (h << 16) | (s << 8) | v
    return (r << 16) | (g << 8) | b


def _rgb_to_hsv(r: int, g: int, b: int) -> tuple[int, int, int]:
    """Convert an RGB triple to the KNX HSV octet triple (H scaled to 0..255)."""
    low = min(r, g, b)
    high = max(r, g, b)
    if low == high:
        hue = 0.0
    elif high == r:
        hue = 60.0 * (g - b) / (high - low)
    elif high == g:
        hue = 60.0 * (2.0 + (b - r) / (high - low))
    else:
        hue = 60.0 * (4.0 + (r - g) / (high - low))
    if hue < 0.0:
        hue += 360.0
    elif hue > 360.0:
        hue -= 360.0
    saturation = 0 if high == 0 else int(255.0 * (high - low) / high)
    return int(255.0 * hue / 360.0), saturation, high


def _encode_raw_data(
    str_value: str, size_in_bit: int, little_endian: bool = False
) -> int | None:
    """Raw octets from a hex string, truncated/zero-padded to the field width.

    For a little-endian program the octets are preceded by the data length as a
    four octet little-endian prefix (matching the reference engine), then the whole
    is padded to the field width.
    """
    try:
        data = bytes.fromhex(str_value)
    except ValueError:
        return None
    if little_endian:
        data = len(data).to_bytes(4, "little") + data
    n_bytes = size_in_bit // 8
    padded = data[:n_bytes].ljust(n_bytes, b"\x00")
    return int.from_bytes(padded, "big") if padded else 0


def resolve_param_values(idx: ApplicationIndexer, state: GlobalState) -> dict[str, str]:
    """Build {referenced_id: effective_value} for the ACTIVE ParameterRefs.

    The encoder writes each memory/property cell from the ParameterRef that is active in
    the resolved UI, taking its instance value, else its ref default, else the base
    Parameter default (``state.get`` resolves that whole chain). Parameters whose
    ref is not active are not encoded at all - their cells stay at the segment seed.

    Keys are the referenced ``Parameter``/``UnionParameter`` id (``pr.ref_id``),
    matching ``item.id`` in :func:`_collect_param` and ``up.id`` in a union pick.
    Module-qualified active refs are not in ``idx.parameter_refs``; the module
    collection path resolves those from its own instance state instead.
    """
    # When several active refs target the same parameter cell (the evaluator can
    # reach more than one in overlapping conditional branches), the reference
    # engine keeps the first one in definition order. Iterate parameter_refs in
    # their (XML/insertion) order and take the first active ref per parameter.
    active = state.active_param_refs()
    overrides: dict[str, str] = {}
    for ref_id, pr in idx.parameter_refs.items():
        if ref_id not in active or pr.ref_id in overrides:
            continue
        value = state.get(ref_id)
        if value is not None:
            overrides[pr.ref_id] = value
    # Explicitly configured union alternatives drive the union selection even if
    # the evaluator did not mark their ref active; carry them too.
    for ref_id, _ in state.relative_param_values():
        pr = idx.parameter_refs.get(ref_id)
        if pr is None or not isinstance(idx.parameters.get(pr.ref_id), UnionParameter):
            continue
        value = state.get(ref_id)
        if value is not None:
            overrides[pr.ref_id] = value
    return overrides


def _resolve_base(base_id: str | None, ms: ModuleState) -> int | None:
    if base_id is None:
        return 0
    arg = ms.arguments.get(base_id)
    if not isinstance(arg, ModuleNumericArg) or arg.value is None:
        return None
    return arg.value


def _build_instance_overrides(
    ms: ModuleState, idx: ApplicationIndexer
) -> dict[str, str]:
    overrides: dict[str, str] = {}
    for pr_id, value in ms.param_ref_id_to_value.items():
        pr = idx.parameter_refs.get(pr_id)
        if pr is not None:
            param = idx.parameters.get(pr.ref_id)
            if param is not None:
                overrides[param.id] = value
    return overrides


def _union_params_to_write(
    parameters: list[UnionParameter],
    overrides: dict[str, str],
    gated: bool = False,
) -> list[tuple[UnionParameter, str]]:
    """Return the union alternatives to write, each with its value.

    Union alternatives can sit at different bit offsets within the shared cell, so
    more than one may be active at once; each active alternative is written (their
    bits accumulate), matching the reference engine. When nothing is active: in a
    resolved UI (gated) the cell keeps its seed; a bare caller falls back to the
    union's default alternative so ``collect_writes`` still yields a value.
    """
    active = [up for up in parameters if up.id in overrides]
    if active:
        return [(up, overrides[up.id]) for up in active]
    if gated:
        return []
    default_up = next((up for up in parameters if up.default_union_parameter), None)
    return [(default_up, default_up.value)] if default_up is not None else []


def _collect_param(
    item: ApplicationProgramStaticParametersParameter
    | ModuleDefStaticParametersParameter,
    overrides: dict[str, str],
    ms: ModuleState | None,
    out: Writes,
    active_ids: set[str] | None = None,
) -> None:
    # When an active-ref set is given (resolved UI), encode only active parameters;
    # inactive cells are left at the segment seed, as the reference engine does.
    if active_ids is not None and item.id not in active_ids:
        return
    choice = item.choice
    value = overrides.get(item.id) or item.value
    # A module parameter's base_value offsets the encoded value by an arg-resolved amount.
    if (
        isinstance(item, ModuleDefStaticParametersParameter)
        and item.base_value is not None
        and ms is not None
    ):
        bv = _resolve_base(item.base_value, ms)
        if bv is not None and bv != 0:
            value = str(int(value) + bv)
    # Test subclasses first: module types derive from the top-level ones
    if isinstance(choice, ModuleDefStaticParametersParameterMemory):
        assert ms is not None
        base = _resolve_base(choice.base_offset, ms)
        if base is not None:
            out.mem.append(
                MemWrite(
                    choice.code_segment,
                    base + choice.offset,
                    choice.bit_offset,
                    item.id,
                    item.parameter_type,
                    value,
                )
            )
    elif isinstance(choice, MemoryParameter):
        out.mem.append(
            MemWrite(
                choice.code_segment,
                choice.offset,
                choice.bit_offset,
                item.id,
                item.parameter_type,
                value,
            )
        )
    elif isinstance(choice, ModuleDefStaticParametersParameterProperty):
        assert ms is not None
        bo = _resolve_base(choice.base_offset, ms)
        bi = _resolve_base(choice.base_index, ms)
        boc = _resolve_base(choice.base_occurrence, ms)
        if bo is not None and bi is not None and boc is not None:
            obj_idx = (choice.object_index or 0) + bi if bi else choice.object_index
            out.prop.append(
                PropWrite(
                    obj_idx,
                    choice.property_id,
                    choice.occurrence + boc,
                    bo + choice.offset,
                    choice.bit_offset,
                    item.id,
                    item.parameter_type,
                    value,
                )
            )
    elif isinstance(choice, PropertyParameter):
        out.prop.append(
            PropWrite(
                choice.object_index,
                choice.property_id,
                choice.occurrence,
                choice.offset,
                choice.bit_offset,
                item.id,
                item.parameter_type,
                value,
            )
        )
    # skip IoPointParameter and None


def _collect_union(
    item: ApplicationProgramStaticParametersUnion | ModuleDefStaticParametersUnion,
    overrides: dict[str, str],
    ms: ModuleState | None,
    out: Writes,
    gated: bool = False,
) -> None:
    choice = item.choice
    if choice is None:
        return
    selected = _union_params_to_write(item.parameter, overrides, gated)
    # Test subclasses first: module types derive from the top-level ones
    if isinstance(choice, ModuleDefStaticParametersUnionMemory):
        assert ms is not None
        base = _resolve_base(choice.base_offset, ms)
        if base is not None:
            for up, value in selected:
                out.mem.append(
                    MemWrite(
                        choice.code_segment,
                        base + choice.offset + up.offset,
                        choice.bit_offset + up.bit_offset,
                        up.id,
                        up.parameter_type,
                        value,
                    )
                )
    elif isinstance(choice, MemoryUnion):
        for up, value in selected:
            out.mem.append(
                MemWrite(
                    choice.code_segment,
                    choice.offset + up.offset,
                    choice.bit_offset + up.bit_offset,
                    up.id,
                    up.parameter_type,
                    value,
                )
            )
    elif isinstance(choice, ModuleDefStaticParametersUnionProperty):
        assert ms is not None
        bo = _resolve_base(choice.base_offset, ms)
        bi = _resolve_base(choice.base_index, ms)
        boc = _resolve_base(choice.base_occurrence, ms)
        if bo is not None and bi is not None and boc is not None:
            obj_idx = (choice.object_index or 0) + bi if bi else choice.object_index
            for up, value in selected:
                out.prop.append(
                    PropWrite(
                        obj_idx,
                        choice.property_id,
                        choice.occurrence + boc,
                        bo + choice.offset + up.offset,
                        choice.bit_offset + up.bit_offset,
                        up.id,
                        up.parameter_type,
                        value,
                    )
                )
    else:
        assert isinstance(choice, PropertyUnion)
        for up, value in selected:
            out.prop.append(
                PropWrite(
                    choice.object_index,
                    choice.property_id,
                    choice.occurrence,
                    choice.offset + up.offset,
                    choice.bit_offset + up.bit_offset,
                    up.id,
                    up.parameter_type,
                    value,
                )
            )


def _collect_scope_writes(
    ms: ModuleState, idx: ApplicationIndexer, out: Writes
) -> None:
    """Collect one module instance scope's writes (not its children), resolved to
    that instance's offsets."""
    if ms.ref_id is None:
        return
    md = idx.module_defs.get(ms.ref_id)
    if md is None or md.static.parameters is None:
        return
    instance_overrides = _build_instance_overrides(ms, idx)
    for item in md.static.parameters.choice:
        if isinstance(item, ModuleDefStaticParametersParameter):
            _collect_param(item, instance_overrides, ms, out)
        else:
            assert isinstance(item, ModuleDefStaticParametersUnion)
            _collect_union(item, instance_overrides, ms, out)


def _collect_module_writes(
    ms: ModuleState, idx: ApplicationIndexer, out: Writes
) -> None:
    _collect_scope_writes(ms, idx, out)
    for child in ms.module_children():
        _collect_module_writes(child, idx, out)


def collect_writes(
    app: ApplicationProgram,
    idx: ApplicationIndexer,
    overrides: dict[str, str],
    state: GlobalState | None = None,
) -> Writes:
    """Gather every parameter write into a Writes bundle, split into mem and prop."""
    out = Writes()
    s = app.static
    # With a resolved state, gate top-level parameters to the active set (regular
    # parameters present in overrides); inactive cells stay at the segment seed.
    # Without a state (direct callers), no gating: every static parameter encodes
    # as before. Unions keep their explicit-selection behaviour either way.
    active_ids = (
        {k for k in overrides if not isinstance(idx.parameters.get(k), UnionParameter)}
        if state is not None
        else None
    )
    if s.parameters is not None:
        for item in s.parameters.choice:
            if isinstance(item, ApplicationProgramStaticParametersParameter):
                _collect_param(item, overrides, None, out, active_ids)
            else:
                assert isinstance(item, ApplicationProgramStaticParametersUnion)
                _collect_union(item, overrides, None, out, gated=active_ids is not None)
    if state is not None:
        for ms in state.module_children():
            _collect_module_writes(ms, idx, out)
    return out


def encode_to_memory(
    app: ApplicationProgram,
    idx: ApplicationIndexer,
    overrides: dict[str, str],
    state: GlobalState | None = None,
) -> dict[str, bytes]:
    """Pack parameter values into per-segment byte buffers.

    Yields {segment_id: bytes} for each segment, seeded from seg.data when set.
    Layout: bit_offset 0 is a byte's MSB; values are big-endian.
    """
    writes = collect_writes(app, idx, overrides, state)
    little_endian = _program_little_endian(app)
    bufs: dict[str, bytearray] = {
        seg_id: bytearray(seg.data) if seg.data else bytearray(seg.size)
        for seg_id, seg in idx.code_segments.items()
    }
    for w in writes.mem:
        buf = bufs.get(w.seg_id)
        if buf is None:
            continue
        pt = idx.parameter_types.get(w.parameter_type)
        if pt is None:
            continue
        tc = pt.choice
        size_in_bit = getattr(tc, "size_in_bit", None)
        if size_in_bit is None:
            continue
        encoded = _encode_value(w.value, size_in_bit, tc, little_endian=little_endian)
        if encoded is None:
            continue
        _write_bits(buf, w.offset, w.bit_offset, size_in_bit, encoded)
    return {seg_id: bytes(buf) for seg_id, buf in bufs.items()}


def encode_to_memory_masked(
    app: ApplicationProgram,
    idx: ApplicationIndexer,
    overrides: dict[str, str],
    state: GlobalState | None = None,
) -> dict[str, tuple[bytes, bytes]]:
    """Like :func:`encode_to_memory` but also return a write mask per segment.

    Returns ``{segment_id: (data, mask)}`` where ``mask`` has one byte per data
    byte: ``0xFF`` for bytes an encoded parameter actually wrote, ``0x00`` for
    bytes left at the segment seed. A downloader writes only masked bytes, so it
    never overwrites regions this encoder does not produce (e.g. the com object
    table or RAM) - mirroring the reference engine, which loads only touched
    bytes on a partial download.
    """
    writes = collect_writes(app, idx, overrides, state)
    little_endian = _program_little_endian(app)
    bufs: dict[str, bytearray] = {
        seg_id: bytearray(seg.data) if seg.data else bytearray(seg.size)
        for seg_id, seg in idx.code_segments.items()
    }
    masks: dict[str, bytearray] = {
        seg_id: bytearray(len(buf)) for seg_id, buf in bufs.items()
    }
    for w in writes.mem:
        buf = bufs.get(w.seg_id)
        if buf is None:
            continue
        pt = idx.parameter_types.get(w.parameter_type)
        if pt is None:
            continue
        tc = pt.choice
        size_in_bit = getattr(tc, "size_in_bit", None)
        if size_in_bit is None:
            continue
        encoded = _encode_value(w.value, size_in_bit, tc, little_endian=little_endian)
        if encoded is None:
            continue
        _write_bits(buf, w.offset, w.bit_offset, size_in_bit, encoded)
        start_bit = w.offset * 8 + w.bit_offset
        end_bit = start_bit + size_in_bit - 1
        mask = masks[w.seg_id]
        for b in range(start_bit // 8, end_bit // 8 + 1):
            if b < len(mask):
                mask[b] = 0xFF
    return {seg_id: (bytes(buf), bytes(masks[seg_id])) for seg_id, buf in bufs.items()}


def build_memory_param_map(
    app: ApplicationProgram,
    idx: ApplicationIndexer,
    overrides: dict[str, str],
    state: GlobalState | None = None,
) -> dict[str, dict[int, tuple[str, str]]]:
    """Map {seg_id: {byte_offset: (param_id, value)}} for hex-viewer hovers."""
    writes = collect_writes(app, idx, overrides, state)
    maps: dict[str, dict[int, tuple[str, str]]] = {
        seg_id: {} for seg_id in idx.code_segments
    }
    for w in writes.mem:
        seg_map = maps.get(w.seg_id)
        if seg_map is None:
            continue
        pt = idx.parameter_types.get(w.parameter_type)
        if pt is None:
            continue
        size = getattr(pt.choice, "size_in_bit", None)
        if not size:
            continue
        start_bit = w.offset * 8 + w.bit_offset
        end_bit = start_bit + size - 1
        for b in range(start_bit // 8, end_bit // 8 + 1):
            seg_map[b] = (w.param_id, w.value)
    return maps


def written_bit_mask(
    app: ApplicationProgram,
    idx: ApplicationIndexer,
    overrides: dict[str, str],
    state: GlobalState | None = None,
) -> dict[str, bytes]:
    """Return ``{seg_id: bit_mask}`` marking which bits an active parameter writes.

    Unlike :func:`encode_to_memory_masked`, whose mask is byte granular (a byte is
    marked as soon as any parameter touches it), this marks the individual **bits**
    a parameter actually drives. Each mask byte holds, MSB first, a ``1`` for every
    bit position covered by a collected write (``1 << (7 - pos % 8)``); every other
    bit stays ``0``.

    A pre-flight uses this to tell apart, within one written byte, the bits that
    carry a real parameter value from the bits it only rewrites to the segment seed
    (the application default) because a neighbouring parameter shares the byte.
    """
    writes = collect_writes(app, idx, overrides, state)
    masks: dict[str, bytearray] = {
        seg_id: bytearray(seg.size if not seg.data else len(seg.data))
        for seg_id, seg in idx.code_segments.items()
    }
    for w in writes.mem:
        mask = masks.get(w.seg_id)
        if mask is None:
            continue
        pt = idx.parameter_types.get(w.parameter_type)
        size_in_bit = getattr(getattr(pt, "choice", None), "size_in_bit", None)
        if not size_in_bit:
            continue
        start_bit = w.offset * 8 + w.bit_offset
        for pos in range(start_bit, start_bit + size_in_bit):
            byte_index = pos // 8
            if byte_index < len(mask):
                mask[byte_index] |= 1 << (7 - pos % 8)
    return {seg_id: bytes(mask) for seg_id, mask in masks.items()}


def _read_bits(data: bytes, offset: int, bit_offset: int, size_in_bit: int) -> int:
    """Read ``size_in_bit`` bits MSB-first from ``data`` - the inverse of ``_write_bits``."""
    start = offset * 8 + bit_offset
    value = 0
    for i in range(size_in_bit):
        pos = start + i
        byte_index = pos // 8
        bit = (data[byte_index] >> (7 - pos % 8)) & 1 if byte_index < len(data) else 0
        value = (value << 1) | bit
    return value


def _is_signed_number(tc: ParameterTypeTypeNumber) -> bool:
    """Whether a number type encodes signed values (a negative lower bound)."""
    try:
        return int(tc.min_inclusive) < 0
    except (TypeError, ValueError):
        return False


def _field_bytes(raw: int, size_in_bit: int) -> bytes | None:
    """The big-endian octets of a byte-aligned field, or ``None`` if sub-octet."""
    if size_in_bit <= 0 or size_in_bit % 8:
        return None
    return raw.to_bytes(size_in_bit // 8, "big")


def _decode_float(raw: int, size_in_bit: int, tc: ParameterTypeTypeFloat) -> str | None:
    """Inverse of :func:`_encode_float` (DPT9 two-octet float and IEEE single/double)."""
    if tc.encoding == ParameterTypeTypeFloatEncoding.DPT_9 and size_in_bit == 16:
        exponent = (raw >> 11) & 0xF
        mantissa = raw & 0x7FF
        if raw & 0x8000:
            mantissa -= 0x800  # 11-bit two's complement
        return str(0.01 * mantissa * (1 << exponent))
    data = _field_bytes(raw, size_in_bit)
    if data is None:
        return None
    if tc.encoding == ParameterTypeTypeFloatEncoding.IEEE_754_SINGLE and len(data) == 4:
        return str(struct.unpack(">f", data)[0])
    if tc.encoding == ParameterTypeTypeFloatEncoding.IEEE_754_DOUBLE and len(data) == 8:
        return str(struct.unpack(">d", data)[0])
    return None


def _decode_value(
    raw: int, size_in_bit: int, tc: object, *, little_endian: bool
) -> str | None:
    """Best-effort inverse of :func:`_encode_value`; ``None`` when not recoverable.

    Enumerations are matched by re-encoding each candidate (so an explicit
    ``BinaryValue`` or byte order is handled by the same forward path). Integer,
    time, float, text, date, IPv4, RGB/RGBW colour and raw-data types are decoded
    directly. The result is a canonical string (e.g. a normalised number/float),
    not necessarily the exact original text. Non-injective encodings (HSV colour,
    a date whose year the type does not display, sub-octet byte types) return
    ``None`` - the original cannot be reconstructed from the bytes alone.
    """
    if isinstance(tc, ParameterTypeTypeRestriction):
        for enumeration in tc.enumeration:
            encoded = _encode_value(
                str(enumeration.value), size_in_bit, tc, little_endian=little_endian
            )
            if encoded is not None and encoded == raw:
                return str(enumeration.value)
        return None
    if isinstance(tc, ParameterTypeTypeNumber):
        logical = _apply_byte_order(raw, size_in_bit, little_endian) or 0
        if _is_signed_number(tc) and logical >= (1 << (size_in_bit - 1)):
            logical -= 1 << size_in_bit
        return str(logical)
    if isinstance(tc, ParameterTypeTypeTime):
        return str(_apply_byte_order(raw, size_in_bit, little_endian) or 0)
    if isinstance(tc, ParameterTypeTypeFloat):
        return _decode_float(raw, size_in_bit, tc)
    if isinstance(tc, ParameterTypeTypeText):
        data = _field_bytes(raw, size_in_bit)
        return None if data is None else data.rstrip(b"\x00").decode("latin-1")
    if isinstance(tc, ParameterTypeTypeIpaddress):
        data = _field_bytes(raw, size_in_bit)
        return (
            None if data is None or len(data) != 4 else ".".join(str(o) for o in data)
        )
    if isinstance(tc, ParameterTypeTypeDate):
        if tc.display_the_year is False:  # year not stored -> not reconstructable
            return None
        day, month, year = (raw >> 16) & 0xFF, (raw >> 8) & 0xFF, raw & 0xFF
        if not (1 <= month <= 12 and 1 <= day <= 31):
            return None
        return f"{2000 + year:04d}-{month:02d}-{day:02d}"
    if isinstance(tc, ParameterTypeTypeColor):
        data = _field_bytes(raw, size_in_bit)
        if data is None or tc.space == ParameterTypeTypeColorSpace.HSV:
            return None  # HSV<-RGB is lossy; not inverted
        if tc.space == ParameterTypeTypeColorSpace.RGBW and len(data) >= 4:
            return "#" + data[:4].hex().upper()
        if len(data) >= 3:
            return "#" + data[:3].hex().upper()
        return None
    if isinstance(tc, ParameterTypeTypeRawData):
        data = _field_bytes(raw, size_in_bit)
        if data is None:
            return None
        if little_endian and len(data) >= 4:
            length = int.from_bytes(data[:4], "little")
            return data[4 : 4 + length].hex().upper()
        return data.rstrip(b"\x00").hex().upper()
    return None


def decode_memory_parameters(
    app: ApplicationProgram,
    idx: ApplicationIndexer,
    segments: Mapping[str, bytes],
    state: GlobalState | None = None,
) -> dict[str, str | None]:
    """Best-effort inverse of :func:`encode_to_memory` for recovering parameter values.

    Given the current bytes of each code segment (read off a device), decodes each
    top-level static memory-backed parameter's value using the application's field
    layout. Returns ``{parameter_id: value}`` where ``value`` is ``None`` for a
    parameter whose type cannot be reconstructed from bytes (see
    :func:`_decode_value`).

    Only top-level static memory parameters are handled. Module-instanced
    parameters are deliberately skipped: a module definition's parameter id repeats
    across every instance at different offsets, so decoding it would collapse the
    instances and the values could not be mapped back to instance-qualified project
    references. Recovering those correctly needs the resolved per-instance layout
    and is left to a caller that has it. Property-backed parameters are omitted too.
    """
    little_endian = _program_little_endian(app)
    result: dict[str, str | None] = {}
    # Resolving against the evaluated state (not empty overrides) is what makes union
    # members appear in the write set: a union only contributes its active alternative
    # once the parameter values are resolved. Only the field layout (segment/offset/
    # size) is used for decoding; the resolved values themselves are irrelevant here.
    overrides = resolve_param_values(idx, state) if state is not None else {}
    for w in collect_writes(app, idx, overrides, state).mem:
        data = segments.get(w.seg_id)
        if data is None:
            continue
        pt = idx.parameter_types.get(w.parameter_type)
        if pt is None:
            continue
        size_in_bit = getattr(pt.choice, "size_in_bit", None)
        if not size_in_bit:
            continue
        raw = _read_bits(data, w.offset, w.bit_offset, size_in_bit)
        result[w.param_id] = _decode_value(
            raw, size_in_bit, pt.choice, little_endian=little_endian
        )
    return result


def decode_property_parameters(
    app: ApplicationProgram,
    idx: ApplicationIndexer,
    properties: Mapping[PropertyKey, bytes],
    state: GlobalState | None = None,
) -> dict[str, str | None]:
    """Best-effort inverse of :func:`encode_to_properties` for property parameters.

    ``properties`` maps ``(object_index, property_id, occurrence)`` to the property
    value bytes read off the device. Decodes each top-level static property-backed
    parameter's field from those bytes. Falls back to any occurrence of the same
    ``(object_index, property_id)`` when the exact occurrence is absent. Fields that
    do not fit the read bytes are skipped. Module-instanced parameters are omitted
    for the same reason as :func:`decode_memory_parameters`.
    """
    little_endian = _program_little_endian(app)
    result: dict[str, str | None] = {}
    overrides = resolve_param_values(idx, state) if state is not None else {}
    for w in collect_writes(app, idx, overrides, state).prop:
        data = properties.get((w.object_index, w.property_id, w.occurrence))
        if data is None:
            data = next(
                (
                    value
                    for (obj, pid, _occ), value in properties.items()
                    if obj == w.object_index and pid == w.property_id
                ),
                None,
            )
        if data is None:
            continue
        pt = idx.parameter_types.get(w.parameter_type)
        if pt is None:
            continue
        size_in_bit = getattr(pt.choice, "size_in_bit", None)
        if not size_in_bit:
            continue
        if w.offset * 8 + w.bit_offset + size_in_bit > len(data) * 8:
            continue  # field does not fit the bytes we read
        raw = _read_bits(data, w.offset, w.bit_offset, size_in_bit)
        result[w.param_id] = _decode_value(
            raw, size_in_bit, pt.choice, little_endian=little_endian
        )
    return result


def _decode_field(
    w: MemWrite | PropWrite,
    data: bytes,
    idx: ApplicationIndexer,
    *,
    little_endian: bool,
) -> str | None:
    """Decode one write's field from ``data`` (its segment/property bytes)."""
    pt = idx.parameter_types.get(w.parameter_type)
    if pt is None:
        return None
    size_in_bit = getattr(pt.choice, "size_in_bit", None)
    if not size_in_bit:
        return None
    if w.offset * 8 + w.bit_offset + size_in_bit > len(data) * 8:
        return None
    raw = _read_bits(data, w.offset, w.bit_offset, size_in_bit)
    return _decode_value(raw, size_in_bit, pt.choice, little_endian=little_endian)


def decode_module_parameters(
    app: ApplicationProgram,
    idx: ApplicationIndexer,
    state: GlobalState,
    segments: Mapping[str, bytes],
    properties: Mapping[PropertyKey, bytes],
) -> dict[str, str | None]:
    """Decode module-instance parameter values from device memory and properties.

    ``state`` must be an evaluated state whose module instances match the device
    (seed it from the recovered top-level parameters first). For every module
    instance scope this resolves that instance's field offsets, decodes each field,
    and returns ``{qualified_parameter_ref_id: value}`` - the same instance-qualified
    reference ids a project stores - with ``None`` for unreconstructable types.
    """
    little_endian = _program_little_endian(app)
    param_to_refs: dict[str, list[str]] = {}
    for ref_id, ref in idx.parameter_refs.items():
        param_to_refs.setdefault(ref.ref_id, []).append(ref_id)

    result: dict[str, str | None] = {}

    def visit(scope: ModuleState) -> None:
        writes = Writes()
        _collect_scope_writes(scope, idx, writes)
        for w in writes.mem:
            data = segments.get(w.seg_id)
            if data is not None:
                value = _decode_field(w, data, idx, little_endian=little_endian)
                for ref_id in param_to_refs.get(w.param_id, []):
                    result[scope.qualify(ref_id)] = value
        for w in writes.prop:
            data = properties.get((w.object_index, w.property_id, w.occurrence))
            if data is None:
                data = next(
                    (
                        value
                        for (obj, pid, _occ), value in properties.items()
                        if obj == w.object_index and pid == w.property_id
                    ),
                    None,
                )
            if data is not None:
                value = _decode_field(w, data, idx, little_endian=little_endian)
                for ref_id in param_to_refs.get(w.param_id, []):
                    result[scope.qualify(ref_id)] = value
        for child in scope.module_children():
            visit(child)

    for child in state.module_children():
        visit(child)
    return result


def encode_to_properties(
    app: ApplicationProgram,
    idx: ApplicationIndexer,
    overrides: dict[str, str],
    state: GlobalState | None = None,
) -> dict[PropertyKey, bytes]:
    """Pack PropertyParameter-backed values into interface-object property data.

    Yields {(object_index, property_id, occurrence): bytes}.
    Layout: bit_offset 0 is a byte's MSB; values are big-endian. Buffers grow to fit.
    """
    writes = collect_writes(app, idx, overrides, state)
    little_endian = _program_little_endian(app)
    bufs: dict[PropertyKey, bytearray] = {}
    for w in writes.prop:
        pt = idx.parameter_types.get(w.parameter_type)
        if pt is None:
            continue
        tc = pt.choice
        size_in_bit = getattr(tc, "size_in_bit", None)
        if not size_in_bit:
            continue
        encoded = _encode_value(w.value, size_in_bit, tc, little_endian=little_endian)
        if encoded is None:
            continue
        key: PropertyKey = (w.object_index, w.property_id, w.occurrence)
        needed = w.offset + (w.bit_offset + size_in_bit + 7) // 8
        buf = bufs.get(key)
        if buf is None:
            bufs[key] = buf = bytearray(needed)
        elif len(buf) < needed:
            buf.extend(bytearray(needed - len(buf)))
        _write_bits(buf, w.offset, w.bit_offset, size_in_bit, encoded)
    return {key: bytes(buf) for key, buf in bufs.items()}


def build_property_param_map(
    app: ApplicationProgram,
    idx: ApplicationIndexer,
    overrides: dict[str, str],
    state: GlobalState | None = None,
) -> dict[PropertyKey, dict[int, tuple[str, str]]]:
    """Map {(object_index, property_id, occurrence): {byte_offset: (param_id, value)}}."""
    writes = collect_writes(app, idx, overrides, state)
    maps: dict[PropertyKey, dict[int, tuple[str, str]]] = {}
    for w in writes.prop:
        pt = idx.parameter_types.get(w.parameter_type)
        if pt is None:
            continue
        size = getattr(pt.choice, "size_in_bit", None)
        if not size:
            continue
        key: PropertyKey = (w.object_index, w.property_id, w.occurrence)
        byte_map = maps.setdefault(key, {})
        start_bit = w.offset * 8 + w.bit_offset
        end_bit = start_bit + size - 1
        for b in range(start_bit // 8, end_bit // 8 + 1):
            byte_map[b] = (w.param_id, w.value)
    return maps
