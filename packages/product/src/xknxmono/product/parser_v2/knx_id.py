from __future__ import annotations

from dataclasses import dataclass

# ── App-level schema definition leaves ────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Parameter:
    """Bare P-N parameter definition (no ParameterRef accessor)."""

    id: int

    def to_parts(self) -> list[str]:
        return [f"P-{self.id:X}"]


@dataclass(frozen=True, slots=True)
class ParameterBlock:
    id: int

    def to_parts(self) -> list[str]:
        return [f"PB-{self.id:X}"]


@dataclass(frozen=True, slots=True)
class ParameterBlockRef:
    id: int
    ref: int

    def to_parts(self) -> list[str]:
        return [f"PB-{self.id:X}", f"R-{self.ref:X}"]


@dataclass(frozen=True, slots=True)
class ParameterBlockCell:
    id: int
    cell: int

    def to_parts(self) -> list[str]:
        return [f"PB-{self.id:X}", f"C-{self.cell:X}"]


@dataclass(frozen=True, slots=True)
class ParameterSeparator:
    id: int

    def to_parts(self) -> list[str]:
        return [f"PS-{self.id:X}"]


@dataclass(frozen=True, slots=True)
class ParameterType:
    """PT-{id} with optional EN-N enumeration child."""

    id: str
    enumeration: int | None = None

    def to_parts(self) -> list[str]:
        parts = [f"PT-{self.id}"]
        if self.enumeration is not None:
            parts.append(f"EN-{self.enumeration:X}")
        return parts


@dataclass(frozen=True, slots=True)
class UnionParameter:
    id: int

    def to_parts(self) -> list[str]:
        return [f"UP-{self.id:X}"]


@dataclass(frozen=True, slots=True)
class UnionParameterRef:
    id: int
    ref: int

    def to_parts(self) -> list[str]:
        return [f"UP-{self.id:X}", f"R-{self.ref:X}"]


@dataclass(frozen=True, slots=True)
class AddressSpace:
    id: str  # typed address space value, e.g. "00C8" or "U045D2"

    def to_parts(self) -> list[str]:
        return [f"AS-{self.id}"]


@dataclass(frozen=True, slots=True)
class ParameterCalc:
    id: int
    suffix: str | None = None  # e.g. "SceneNumber_1"

    def to_parts(self) -> list[str]:
        parts = [f"PC-{self.id:X}"]
        if self.suffix is not None:
            parts.append(self.suffix)
        return parts


@dataclass(frozen=True, slots=True)
class BinaryInput:
    id: int

    def to_parts(self) -> list[str]:
        return [f"BI-{self.id:X}"]


@dataclass(frozen=True, slots=True)
class StatusResponse:
    id: int

    def to_parts(self) -> list[str]:
        return [f"SR-{self.id:X}"]


@dataclass(frozen=True, slots=True)
class ResourceSpec:
    """RS-{id} resource style reference at application level."""

    id: str  # e.g. "01-00000"

    def to_parts(self) -> list[str]:
        return [f"RS-{self.id}"]


@dataclass(frozen=True, slots=True)
class ParameterValue:
    id: int

    def to_parts(self) -> list[str]:
        return [f"PV-{self.id:X}"]


@dataclass(frozen=True, slots=True)
class ParameterRename:
    id: int

    def to_parts(self) -> list[str]:
        return [f"PR-{self.id:X}"]


@dataclass(frozen=True, slots=True)
class Block:
    id: int

    def to_parts(self) -> list[str]:
        return [f"B-{self.id:X}"]


@dataclass(frozen=True, slots=True)
class BitmapDef:
    """BD-{id} bitmap definition reference at application level."""

    id: str

    def to_parts(self) -> list[str]:
        return [f"BD-{self.id}"]


@dataclass(frozen=True, slots=True)
class Baggage:
    """BG-{id} baggage file reference at manufacturer level (no application segment)."""

    id: str

    def to_parts(self) -> list[str]:
        return [f"BG-{self.id}"]


@dataclass(frozen=True, slots=True)
class Channel:
    id: str  # alphanumeric identifier, e.g. "1", "I1", "S10", "RF.20parameters"

    def to_parts(self) -> list[str]:
        return [f"CH-{self.id}"]


@dataclass(frozen=True, slots=True)
class ComObject:
    id: str  # may be composite e.g. "2-0" inside ModuleDef

    def to_parts(self) -> list[str]:
        return [f"O-{self.id}"]


@dataclass(frozen=True, slots=True)
class ComObjectRef:
    id: str  # may be composite e.g. "2-0" inside ModuleDef
    ref: int

    def to_parts(self) -> list[str]:
        return [f"O-{self.id}", f"R-{self.ref:X}"]


# ── Module-level leaves ───────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class ParamRef:
    parameter: int
    ref: int

    def to_parts(self) -> list[str]:
        return [f"P-{self.parameter:X}", f"R-{self.ref:X}"]


@dataclass(frozen=True, slots=True)
class ArgRef:
    argument: int

    def to_parts(self) -> list[str]:
        return [f"A-{self.argument:X}"]


@dataclass(frozen=True, slots=True)
class AllocatorRef:
    allocator: int

    def to_parts(self) -> list[str]:
        return [f"L-{self.allocator:X}"]


@dataclass(frozen=True, slots=True)
class RepeatPath:
    """Path through one or more nested Repeat elements (X-N[_X-M...])."""

    index: int
    rest: RepeatPath | None = None

    def to_parts(self) -> list[str]:
        parts = [f"X-{self.index:X}"]
        if self.rest is not None:
            parts.extend(self.rest.to_parts())
        return parts


# ── Structural nodes ──────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class SubModule:
    """M-N[_MI-N] within a SubModuleDef scope."""

    id: int
    instance: int | None = None
    content: ParamRef | ArgRef | None = None

    @property
    def param_ref(self) -> ParamRef | None:
        return self.content if isinstance(self.content, ParamRef) else None

    @property
    def arg_ref(self) -> ArgRef | None:
        return self.content if isinstance(self.content, ArgRef) else None

    def to_parts(self) -> list[str]:
        parts = [f"M-{self.id:X}"]
        if self.instance is not None:
            parts.append(f"MI-{self.instance:X}")
        if self.content is not None:
            parts.extend(self.content.to_parts())
        return parts


@dataclass(frozen=True, slots=True)
class SubModuleDef:
    """SM-N and its contents; appears directly under ModuleDef or under Module."""

    id: int
    content: (
        ArgRef
        | RepeatPath
        | SubModule
        | Channel
        | ComObject
        | ComObjectRef
        | ParamRef
        | Parameter
        | ParameterBlock
        | ParameterBlockRef
        | ParameterBlockCell
        | ParameterSeparator
        | ParameterCalc
        | AllocatorRef
        | UnionParameter
        | UnionParameterRef
        | None
    ) = None

    @property
    def sub_module(self) -> SubModule | None:
        return self.content if isinstance(self.content, SubModule) else None

    @property
    def arg_ref(self) -> ArgRef | None:
        return self.content if isinstance(self.content, ArgRef) else None

    @property
    def repeat_path(self) -> RepeatPath | None:
        return self.content if isinstance(self.content, RepeatPath) else None

    @property
    def channel(self) -> Channel | None:
        return self.content if isinstance(self.content, Channel) else None

    @property
    def com_object(self) -> ComObject | None:
        return self.content if isinstance(self.content, ComObject) else None

    @property
    def com_object_ref(self) -> ComObjectRef | None:
        return self.content if isinstance(self.content, ComObjectRef) else None

    @property
    def param_ref(self) -> ParamRef | None:
        return self.content if isinstance(self.content, ParamRef) else None

    @property
    def parameter(self) -> Parameter | None:
        return self.content if isinstance(self.content, Parameter) else None

    @property
    def parameter_block(self) -> ParameterBlock | None:
        return self.content if isinstance(self.content, ParameterBlock) else None

    @property
    def parameter_block_ref(self) -> ParameterBlockRef | None:
        return self.content if isinstance(self.content, ParameterBlockRef) else None

    @property
    def parameter_block_cell(self) -> ParameterBlockCell | None:
        return self.content if isinstance(self.content, ParameterBlockCell) else None

    @property
    def parameter_separator(self) -> ParameterSeparator | None:
        return self.content if isinstance(self.content, ParameterSeparator) else None

    @property
    def parameter_calc(self) -> ParameterCalc | None:
        return self.content if isinstance(self.content, ParameterCalc) else None

    @property
    def allocator_ref(self) -> AllocatorRef | None:
        return self.content if isinstance(self.content, AllocatorRef) else None

    @property
    def union_parameter(self) -> UnionParameter | None:
        return self.content if isinstance(self.content, UnionParameter) else None

    @property
    def union_parameter_ref(self) -> UnionParameterRef | None:
        return self.content if isinstance(self.content, UnionParameterRef) else None

    def to_parts(self) -> list[str]:
        parts = [f"SM-{self.id:X}"]
        if self.content is not None:
            parts.extend(self.content.to_parts())
        return parts


@dataclass(frozen=True, slots=True)
class Module:
    """M-N[_MI-N] within a ModuleDef scope."""

    id: int
    instance: int | None = None
    content: ParamRef | ArgRef | SubModuleDef | None = None

    @property
    def sub_module_def(self) -> SubModuleDef | None:
        return self.content if isinstance(self.content, SubModuleDef) else None

    @property
    def param_ref(self) -> ParamRef | None:
        return self.content if isinstance(self.content, ParamRef) else None

    @property
    def arg_ref(self) -> ArgRef | None:
        return self.content if isinstance(self.content, ArgRef) else None

    def to_parts(self) -> list[str]:
        parts = [f"M-{self.id:X}"]
        if self.instance is not None:
            parts.append(f"MI-{self.instance:X}")
        if self.content is not None:
            parts.extend(self.content.to_parts())
        return parts


@dataclass(frozen=True, slots=True)
class ModuleDef:
    """MD-N and its contents."""

    id: int
    content: (
        Module
        | SubModuleDef
        | Parameter
        | ParamRef
        | ParameterBlock
        | ParameterBlockRef
        | ParameterBlockCell
        | ParameterSeparator
        | ParameterCalc
        | ArgRef
        | AllocatorRef
        | UnionParameter
        | UnionParameterRef
        | Channel
        | ComObject
        | ComObjectRef
        | RepeatPath
        | ParameterValue
        | Block
        | ParameterRename
        | None
    ) = None

    @property
    def module(self) -> Module | None:
        return self.content if isinstance(self.content, Module) else None

    @property
    def sub_module_def(self) -> SubModuleDef | None:
        return self.content if isinstance(self.content, SubModuleDef) else None

    @property
    def param_ref(self) -> ParamRef | None:
        return self.content if isinstance(self.content, ParamRef) else None

    @property
    def arg_ref(self) -> ArgRef | None:
        return self.content if isinstance(self.content, ArgRef) else None

    @property
    def allocator_ref(self) -> AllocatorRef | None:
        return self.content if isinstance(self.content, AllocatorRef) else None

    @property
    def repeat_path(self) -> RepeatPath | None:
        return self.content if isinstance(self.content, RepeatPath) else None

    @property
    def parameter(self) -> Parameter | None:
        return self.content if isinstance(self.content, Parameter) else None

    @property
    def parameter_block(self) -> ParameterBlock | None:
        return self.content if isinstance(self.content, ParameterBlock) else None

    @property
    def parameter_block_ref(self) -> ParameterBlockRef | None:
        return self.content if isinstance(self.content, ParameterBlockRef) else None

    @property
    def parameter_block_cell(self) -> ParameterBlockCell | None:
        return self.content if isinstance(self.content, ParameterBlockCell) else None

    @property
    def parameter_separator(self) -> ParameterSeparator | None:
        return self.content if isinstance(self.content, ParameterSeparator) else None

    @property
    def parameter_calc(self) -> ParameterCalc | None:
        return self.content if isinstance(self.content, ParameterCalc) else None

    @property
    def union_parameter(self) -> UnionParameter | None:
        return self.content if isinstance(self.content, UnionParameter) else None

    @property
    def union_parameter_ref(self) -> UnionParameterRef | None:
        return self.content if isinstance(self.content, UnionParameterRef) else None

    @property
    def channel(self) -> Channel | None:
        return self.content if isinstance(self.content, Channel) else None

    @property
    def com_object(self) -> ComObject | None:
        return self.content if isinstance(self.content, ComObject) else None

    @property
    def com_object_ref(self) -> ComObjectRef | None:
        return self.content if isinstance(self.content, ComObjectRef) else None

    @property
    def parameter_value(self) -> ParameterValue | None:
        return self.content if isinstance(self.content, ParameterValue) else None

    @property
    def parameter_record(self) -> ParameterRename | None:
        return self.content if isinstance(self.content, ParameterRename) else None

    @property
    def block(self) -> Block | None:
        return self.content if isinstance(self.content, Block) else None

    def to_parts(self) -> list[str]:
        parts = [f"MD-{self.id:X}"]
        if self.content is not None:
            parts.extend(self.content.to_parts())
        return parts


# ── Application and root ──────────────────────────────────────────────────────

_AppContent = (
    ModuleDef
    | Module
    | Parameter
    | ParamRef
    | ParameterBlock
    | ParameterBlockRef
    | ParameterBlockCell
    | ParameterSeparator
    | ParameterType
    | UnionParameter
    | UnionParameterRef
    | AllocatorRef
    | AddressSpace
    | ParameterCalc
    | BinaryInput
    | StatusResponse
    | ResourceSpec
    | ParameterValue
    | ParameterRename
    | Block
    | BitmapDef
    | Channel
    | ComObject
    | ComObjectRef
    | RepeatPath
)


@dataclass(frozen=True, slots=True)
class Application:
    """
    Structured application program identifier: A-{number:04X}-{version:02X}-{fingerprint:04X}[-{order}].

    number      — application program number (4 hex digits)
    version     — version (2 hex digits)
    fingerprint — checksum / fingerprint (4 hex digits)
    order       — optional hardware-order suffix, e.g. "O000A"
    content     — optional application-level segment
    """

    number: int
    version: int
    fingerprint: int
    order: str | None = None
    content: _AppContent | None = None

    @property
    def module_def(self) -> ModuleDef | None:
        return self.content if isinstance(self.content, ModuleDef) else None

    @property
    def module(self) -> Module | None:
        return self.content if isinstance(self.content, Module) else None

    @property
    def param_ref(self) -> ParamRef | None:
        return self.content if isinstance(self.content, ParamRef) else None

    @property
    def parameter(self) -> Parameter | None:
        return self.content if isinstance(self.content, Parameter) else None

    @property
    def parameter_block(self) -> ParameterBlock | None:
        return self.content if isinstance(self.content, ParameterBlock) else None

    @property
    def parameter_block_ref(self) -> ParameterBlockRef | None:
        return self.content if isinstance(self.content, ParameterBlockRef) else None

    @property
    def parameter_block_cell(self) -> ParameterBlockCell | None:
        return self.content if isinstance(self.content, ParameterBlockCell) else None

    @property
    def parameter_separator(self) -> ParameterSeparator | None:
        return self.content if isinstance(self.content, ParameterSeparator) else None

    @property
    def parameter_type(self) -> ParameterType | None:
        return self.content if isinstance(self.content, ParameterType) else None

    @property
    def union_parameter(self) -> UnionParameter | None:
        return self.content if isinstance(self.content, UnionParameter) else None

    @property
    def union_parameter_ref(self) -> UnionParameterRef | None:
        return self.content if isinstance(self.content, UnionParameterRef) else None

    @property
    def allocator_ref(self) -> AllocatorRef | None:
        return self.content if isinstance(self.content, AllocatorRef) else None

    @property
    def address_space(self) -> AddressSpace | None:
        return self.content if isinstance(self.content, AddressSpace) else None

    @property
    def parameter_calc(self) -> ParameterCalc | None:
        return self.content if isinstance(self.content, ParameterCalc) else None

    @property
    def binary_input(self) -> BinaryInput | None:
        return self.content if isinstance(self.content, BinaryInput) else None

    @property
    def status_response(self) -> StatusResponse | None:
        return self.content if isinstance(self.content, StatusResponse) else None

    @property
    def resource_spec(self) -> ResourceSpec | None:
        return self.content if isinstance(self.content, ResourceSpec) else None

    @property
    def parameter_value(self) -> ParameterValue | None:
        return self.content if isinstance(self.content, ParameterValue) else None

    @property
    def parameter_record(self) -> ParameterRename | None:
        return self.content if isinstance(self.content, ParameterRename) else None

    @property
    def block(self) -> Block | None:
        return self.content if isinstance(self.content, Block) else None

    @property
    def bitmap_def(self) -> BitmapDef | None:
        return self.content if isinstance(self.content, BitmapDef) else None

    @property
    def channel(self) -> Channel | None:
        return self.content if isinstance(self.content, Channel) else None

    @property
    def com_object(self) -> ComObject | None:
        return self.content if isinstance(self.content, ComObject) else None

    @property
    def com_object_ref(self) -> ComObjectRef | None:
        return self.content if isinstance(self.content, ComObjectRef) else None

    @property
    def repeat_path(self) -> RepeatPath | None:
        return self.content if isinstance(self.content, RepeatPath) else None

    def to_parts(self) -> list[str]:
        app_id = f"A-{self.number:04X}-{self.version:02X}-{self.fingerprint:04X}"
        if self.order is not None:
            app_id += f"-{self.order}"
        parts = [app_id]
        if self.content is not None:
            parts.extend(self.content.to_parts())
        return parts


@dataclass(frozen=True, slots=True)
class KnxId:
    """
    Structured KNX manufacturer-level identifier: M-{manufacturer:04X}[_A-...|_BG-...].

    manufacturer — manufacturer ID (4 hex digits)
    content      — Application, Baggage, or None

    Hierarchy (each node holds exactly one typed child):

      KnxId(manufacturer, content: Application?)
        └─ Application(number, version, fingerprint, order?)
             ├─ ModuleDef(id)
             │    ├─ Module(id, instance?)
             │    │    ├─ SubModuleDef(id)
             │    │    │    └─ SubModule(id, instance?) ──► ParamRef | ArgRef
             │    │    ├─ ArgRef | ParamRef
             │    │    └─ (nothing)
             │    ├─ SubModuleDef(id)
             │    │    ├─ ArgRef | RepeatPath
             │    │    ├─ SubModule(id, instance?) ──► ParamRef | ArgRef
             │    │    ├─ Channel | ComObject | ComObjectRef
             │    │    ├─ Parameter | ParamRef | ParameterBlock | ParameterBlockRef
             │    │    ├─ ParameterBlockCell | ParameterSeparator | ParameterCalc
             │    │    ├─ AllocatorRef | UnionParameter | UnionParameterRef
             │    │    └─ (nothing)
             │    ├─ Parameter | ParamRef | ParameterBlock | ParameterBlockRef
             │    ├─ ParameterBlockCell | ParameterSeparator | ParameterCalc
             │    ├─ ArgRef | AllocatorRef | RepeatPath
             │    ├─ UnionParameter | UnionParameterRef
             │    ├─ Channel | ComObject | ComObjectRef
             │    ├─ ParameterValue | ParameterRename | Block
             │    └─ (nothing)
             ├─ Parameter | ParamRef | ParameterBlock | ParameterBlockRef
             ├─ ParameterBlockCell | ParameterSeparator | ParameterType
             ├─ UnionParameter | UnionParameterRef | AllocatorRef
             ├─ AddressSpace | Channel | ComObject | ComObjectRef
             ├─ ParameterCalc | BinaryInput | StatusResponse | ResourceSpec
             ├─ ParameterValue | ParameterRename | Block | BitmapDef
             ├─ RepeatPath | Module
             └─ (nothing)
      KnxId(manufacturer, content: Baggage?)
        ├─ Baggage(id)
        └─ (nothing)
    """

    manufacturer: int
    content: Application | Baggage | None = None

    @property
    def app(self) -> Application | None:
        return self.content if isinstance(self.content, Application) else None

    @property
    def baggage(self) -> Baggage | None:
        return self.content if isinstance(self.content, Baggage) else None

    @staticmethod
    def from_string(s: str) -> KnxId:
        tokens = s.split("_")
        pos = 0

        def peek() -> str | None:
            return tokens[pos].partition("-")[0] if pos < len(tokens) else None

        def consume() -> tuple[str, str]:
            nonlocal pos
            prefix, _, value = tokens[pos].partition("-")
            pos += 1
            return prefix, value

        def maybe(prefix: str) -> str | None:
            if peek() == prefix:
                return consume()[1]
            return None

        def require(prefix: str) -> str:
            p, v = consume()
            if p != prefix:
                raise ValueError(f"Expected {prefix!r}, got {p!r} in {s!r}")
            return v

        def hx(v: str) -> int:
            return int(v, 16)

        def parse_repeat() -> RepeatPath | None:
            if peek() != "X":
                return None
            idx = hx(consume()[1])
            return RepeatPath(idx, parse_repeat())

        def parse_param_ref() -> ParamRef | None:
            if peek() != "P":
                return None
            if pos + 1 >= len(tokens) or not tokens[pos + 1].startswith("R-"):
                return None  # bare P-N without R-N is not a ParamRef
            p = hx(consume()[1])
            return ParamRef(p, hx(require("R")))

        def parse_sub_module() -> SubModule | None:
            if peek() != "M":
                return None
            m_id = hx(consume()[1])
            mi = maybe("MI")
            sub_content: ParamRef | ArgRef | None
            if peek() == "A":
                sub_content = ArgRef(hx(consume()[1]))
            else:
                sub_content = parse_param_ref()
            return SubModule(m_id, hx(mi) if mi is not None else None, sub_content)

        def parse_sub_module_def() -> SubModuleDef | None:
            if peek() != "SM":
                return None
            sm_id = hx(consume()[1])
            sub_content: (
                ArgRef
                | RepeatPath
                | SubModule
                | Channel
                | ComObject
                | ComObjectRef
                | ParamRef
                | Parameter
                | ParameterBlock
                | ParameterBlockRef
                | ParameterBlockCell
                | ParameterSeparator
                | ParameterCalc
                | AllocatorRef
                | UnionParameter
                | UnionParameterRef
                | None
            )
            if peek() == "A":
                sub_content = ArgRef(hx(consume()[1]))
            elif peek() == "X":
                sub_content = parse_repeat()
            elif peek() == "M":
                sub_content = parse_sub_module()
            elif peek() == "CH":
                sub_content = Channel(consume()[1])
            elif peek() == "O":
                o_id = consume()[1]
                r = maybe("R")
                sub_content = (
                    ComObjectRef(o_id, hx(r)) if r is not None else ComObject(o_id)
                )
            elif peek() == "P":
                p_id = hx(consume()[1])
                r = maybe("R")
                sub_content = (
                    ParamRef(p_id, hx(r)) if r is not None else Parameter(p_id)
                )
            elif peek() == "PB":
                pb_id = hx(consume()[1])
                if peek() == "R":
                    sub_content = ParameterBlockRef(pb_id, hx(consume()[1]))
                elif peek() == "C":
                    sub_content = ParameterBlockCell(pb_id, hx(consume()[1]))
                else:
                    sub_content = ParameterBlock(pb_id)
            elif peek() == "PS":
                sub_content = ParameterSeparator(hx(consume()[1]))
            elif peek() == "UP":
                up_id = hx(consume()[1])
                r = maybe("R")
                sub_content = (
                    UnionParameterRef(up_id, hx(r))
                    if r is not None
                    else UnionParameter(up_id)
                )
            elif peek() == "L":
                sub_content = AllocatorRef(hx(consume()[1]))
            elif peek() == "PC":
                pc_id = hx(consume()[1])
                raw_rest: list[str] = []
                while pos < len(tokens):
                    raw_rest.append(tokens[pos])
                    consume()
                sub_content = ParameterCalc(pc_id, "_".join(raw_rest) or None)
            else:
                sub_content = None
            return SubModuleDef(sm_id, sub_content)

        def parse_module() -> Module | None:
            if peek() != "M":
                return None
            m_id = hx(consume()[1])
            mi = maybe("MI")
            instance = hx(mi) if mi is not None else None
            mod_content: ParamRef | ArgRef | SubModuleDef | None = None
            if peek() == "SM":
                mod_content = parse_sub_module_def()
            elif peek() == "A":
                mod_content = ArgRef(hx(consume()[1]))
            else:
                mod_content = parse_param_ref()
            return Module(m_id, instance, mod_content)

        def parse_module_def_content() -> (
            Module
            | SubModuleDef
            | Parameter
            | ParamRef
            | ParameterBlock
            | ParameterBlockRef
            | ParameterBlockCell
            | ParameterSeparator
            | ParameterCalc
            | ArgRef
            | AllocatorRef
            | UnionParameter
            | UnionParameterRef
            | Channel
            | ComObject
            | ComObjectRef
            | RepeatPath
            | ParameterValue
            | Block
            | ParameterRename
            | None
        ):
            if peek() == "X":
                return parse_repeat()
            if peek() == "M":
                return parse_module()
            if peek() == "SM":
                return parse_sub_module_def()
            if peek() == "P":
                p_id = hx(consume()[1])
                r = maybe("R")
                if r is not None:
                    return ParamRef(p_id, hx(r))
                return Parameter(p_id)
            if peek() == "PB":
                pb_id = hx(consume()[1])
                if peek() == "R":
                    return ParameterBlockRef(pb_id, hx(consume()[1]))
                if peek() == "C":
                    return ParameterBlockCell(pb_id, hx(consume()[1]))
                return ParameterBlock(pb_id)
            if peek() == "PS":
                return ParameterSeparator(hx(consume()[1]))
            if peek() == "A":
                return ArgRef(hx(consume()[1]))
            if peek() == "L":
                return AllocatorRef(hx(consume()[1]))
            if peek() == "UP":
                up_id = hx(consume()[1])
                r = maybe("R")
                if r is not None:
                    return UnionParameterRef(up_id, hx(r))
                return UnionParameter(up_id)
            if peek() == "CH":
                return Channel(consume()[1])
            if peek() == "PC":
                pc_id = hx(consume()[1])
                raw_rest: list[str] = []
                while pos < len(tokens):
                    raw_rest.append(tokens[pos])
                    consume()
                return ParameterCalc(pc_id, "_".join(raw_rest) or None)
            if peek() == "O":
                o_id = consume()[1]
                r = maybe("R")
                if r is not None:
                    return ComObjectRef(o_id, hx(r))
                return ComObject(o_id)
            if peek() == "PV":
                return ParameterValue(hx(consume()[1]))
            if peek() == "B":
                return Block(hx(consume()[1]))
            if peek() == "PR":
                return ParameterRename(hx(consume()[1]))
            return None

        def parse_app_content() -> _AppContent | None:
            p = peek()
            if p == "MD":
                md = hx(consume()[1])
                return ModuleDef(md, parse_module_def_content())
            if p == "X":
                return parse_repeat()
            if p == "P":
                p_id = hx(consume()[1])
                r = maybe("R")
                if r is not None:
                    return ParamRef(p_id, hx(r))
                return Parameter(p_id)
            if p == "PB":
                pb_id = hx(consume()[1])
                if peek() == "R":
                    return ParameterBlockRef(pb_id, hx(consume()[1]))
                if peek() == "C":
                    return ParameterBlockCell(pb_id, hx(consume()[1]))
                return ParameterBlock(pb_id)
            if p == "PS":
                return ParameterSeparator(hx(consume()[1]))
            if p == "PT":
                pt_id = consume()[1]
                en = maybe("EN")
                return ParameterType(pt_id, hx(en) if en is not None else None)
            if p == "UP":
                up_id = hx(consume()[1])
                r = maybe("R")
                if r is not None:
                    return UnionParameterRef(up_id, hx(r))
                return UnionParameter(up_id)
            if p == "AS":
                return AddressSpace(consume()[1])
            if p == "PC":
                pc_id = hx(consume()[1])
                raw_rest: list[str] = []
                while pos < len(tokens):
                    raw_rest.append(tokens[pos])
                    consume()
                return ParameterCalc(pc_id, "_".join(raw_rest) or None)
            if p == "RS":
                return ResourceSpec(consume()[1])
            if p == "L":
                return AllocatorRef(hx(consume()[1]))
            if p == "M":
                return parse_module()
            if p == "BI":
                return BinaryInput(hx(consume()[1]))
            if p == "SR":
                return StatusResponse(hx(consume()[1]))
            if p == "PV":
                return ParameterValue(hx(consume()[1]))
            if p == "PR":
                return ParameterRename(hx(consume()[1]))
            if p == "B":
                return Block(hx(consume()[1]))
            if p == "BD":
                return BitmapDef(consume()[1])
            if p == "CH":
                return Channel(consume()[1])
            if p == "O":
                o_id = consume()[1]  # may be composite e.g. "2-0"
                r = maybe("R")
                if r is not None:
                    return ComObjectRef(o_id, hx(r))
                return ComObject(o_id)
            return None

        mfr = hx(require("M"))
        knx_content: Application | Baggage | None
        if peek() == "A":
            app_str = consume()[1]  # e.g. "9A1B-01-ABAF" or "7072-21-5CC3-O000A"
            app_parts = app_str.split("-")
            number = hx(app_parts[0])
            version = hx(app_parts[1])
            fingerprint = hx(app_parts[2])
            order = app_parts[3] if len(app_parts) > 3 else None
            knx_content = Application(
                number=number,
                version=version,
                fingerprint=fingerprint,
                order=order,
                content=parse_app_content(),
            )
        elif peek() == "BG":
            knx_content = Baggage(consume()[1])
        else:
            knx_content = None

        return KnxId(manufacturer=mfr, content=knx_content)

    def __str__(self) -> str:
        parts = [f"M-{self.manufacturer:04X}"]
        if self.content is not None:
            parts.extend(self.content.to_parts())
        return "_".join(parts)
