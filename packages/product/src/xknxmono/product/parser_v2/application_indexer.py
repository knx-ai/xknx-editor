from __future__ import annotations

from xknxmono.models.intermediate import (
    ApplicationProgram,
    ApplicationProgramStaticParametersUnion,
    ModuleDef,
    ModuleDefStaticParametersUnion,
    ParameterType,
)
from xknxmono.models.intermediate.com_object_ref_t import ComObjectRef
from xknxmono.models.intermediate.com_object_t import ComObject
from xknxmono.models.intermediate.parameter_base_t import ParameterBase
from xknxmono.models.intermediate.parameter_calculation_t import ParameterCalculation
from xknxmono.models.intermediate.parameter_ref_t import ParameterRef
from xknxmono.models.intermediate.segment_base_t import SegmentBase

from .allocator import Allocator


class ApplicationIndexer:
    """Pre-built lookup tables for static IR sections (parameters, parameter refs, parameter types, module defs)."""

    __slots__ = (
        "_calculations",
        "allocators",
        "app_allocators",
        "arg_alloc",
        "code_segments",
        "com_object_refs",
        "com_objects",
        "module_defs",
        "parameter_refs",
        "parameter_types",
        "parameters",
        "script",
    )

    def __init__(self, app: ApplicationProgram) -> None:
        self.module_defs: dict[str, ModuleDef] = {}
        self.parameter_refs: dict[str, ParameterRef] = {}
        self.parameters: dict[str, ParameterBase] = {}
        self.parameter_types: dict[str, ParameterType] = {}
        self.com_objects: dict[str, ComObject] = {}
        self.com_object_refs: dict[str, ComObjectRef] = {}
        self.code_segments: dict[str, SegmentBase] = {}
        self._calculations: dict[str, dict[str, list[ParameterCalculation]]] = {}
        self.script: str | None = None
        self.allocators: dict[str, dict[str, Allocator]] = {}
        # Application-level allocators: a module argument's Allocator can be defined on the
        # application (not the module def), so keep them separate for allocate() to fall back to.
        self.app_allocators: dict[str, Allocator] = {}
        self.arg_alloc: dict[str, dict[str, tuple[int, int]]] = {}
        self._index_app(app)
        if app.module_defs is not None:
            for md in app.module_defs.module_def:
                self._index_module_def(md)

    def _index_app(self, app: ApplicationProgram) -> None:
        s = app.static
        if s.script is not None:
            self.script = s.script.value or None
        if s.code is not None:
            for seg in s.code.absolute_segment:
                self.code_segments[seg.id] = seg
            for seg in s.code.relative_segment:
                self.code_segments[seg.id] = seg
        if s.parameter_types is not None:
            for pt in s.parameter_types.parameter_type:
                self.parameter_types[pt.id] = pt
        if s.parameters is not None:
            for p in s.parameters.choice:
                if isinstance(p, ApplicationProgramStaticParametersUnion):
                    for up in p.parameter:
                        self.parameters[up.id] = up
                else:
                    self.parameters[p.id] = p
        if s.parameter_refs is not None:
            for pr in s.parameter_refs.parameter_ref:
                self.parameter_refs[pr.id] = pr
        if s.com_object_table is not None:
            for co in s.com_object_table.com_object:
                self.com_objects[co.id] = co
        if s.com_object_refs is not None:
            for cor in s.com_object_refs.com_object_ref:
                self.com_object_refs[cor.id] = cor
        if s.parameter_calculations is not None:
            self._index_calculations(s.parameter_calculations.parameter_calculation)
        if s.allocators is not None:
            self.app_allocators = {
                a.id: Allocator(id=a.id, start=a.start, max_inclusive=a.max_inclusive)
                for a in s.allocators.allocator
            }

    def segment_base_addr(self, seg_id: str) -> int:
        seg = self.code_segments.get(seg_id)
        if seg is None:
            return 0
        return int(getattr(seg, "address", getattr(seg, "offset", 0)))

    def calculations_for_l(self, ref_id: str) -> list[ParameterCalculation]:
        return self._calculations.get(ref_id, {}).get("l", [])

    def calculations_for_r(self, ref_id: str) -> list[ParameterCalculation]:
        return self._calculations.get(ref_id, {}).get("r", [])

    def _index_calculations(self, calcs: list[ParameterCalculation]) -> None:
        for calc in calcs:
            for pr in calc.lparameters.parameter_ref_ref:
                self._calculations.setdefault(pr.ref_id, {}).setdefault("l", []).append(
                    calc
                )
            for pr in calc.rparameters.parameter_ref_ref:
                self._calculations.setdefault(pr.ref_id, {}).setdefault("r", []).append(
                    calc
                )

    def _index_module_def(self, md: ModuleDef) -> None:
        if md.id:
            self.module_defs[md.id] = md
        if md.static.parameters is not None:
            for p in md.static.parameters.choice:
                if isinstance(p, ModuleDefStaticParametersUnion):
                    for up in p.parameter:
                        self.parameters[up.id] = up
                else:
                    self.parameters[p.id] = p
        if md.static.parameter_refs is not None:
            for pr in md.static.parameter_refs.parameter_ref:
                self.parameter_refs[pr.id] = pr
        if md.static.com_objects is not None:
            for co in md.static.com_objects.com_object:
                self.com_objects[co.id] = co
        if md.static.com_object_refs is not None:
            for cor in md.static.com_object_refs.com_object_ref:
                self.com_object_refs[cor.id] = cor
        if md.static.parameter_calculations is not None:
            self._index_calculations(
                md.static.parameter_calculations.parameter_calculation
            )
        if md.static.allocators is not None:
            self.allocators[md.id] = {
                a.id: Allocator(id=a.id, start=a.start, max_inclusive=a.max_inclusive)
                for a in md.static.allocators.allocator
            }
        if md.arguments is not None:
            self.arg_alloc[md.id] = {
                a.id: (a.allocates if a.allocates is not None else 1, a.alignment.value)
                for a in md.arguments.argument
            }
        if md.sub_module_defs is not None:
            for sub in md.sub_module_defs.module_def:
                self._index_module_def(sub)
