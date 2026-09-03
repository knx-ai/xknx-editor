from __future__ import annotations

from xknxmono.models.intermediate import (
    ComObjectInstanceRef,
    ModuleArg,
    ModuleInstance,
    ModuleTextArg,
    ParameterInstanceRef,
)
from xknxmono.models.intermediate.module_t_numeric_arg import ModuleNumericArg

from .application_indexer import ApplicationIndexer


def compute_arg_defaults(
    mod_def_arguments: object, instance_args: list[ModuleArg]
) -> dict[str, str]:
    """Return {arg_name: value} for all text args in a module instance."""
    result: dict[str, str] = {}
    if mod_def_arguments is None:
        return result
    arg_def_by_id = {a.id: a for a in getattr(mod_def_arguments, "argument", [])}
    for arg in instance_args:
        if isinstance(arg, ModuleTextArg):
            arg_def = arg_def_by_id.get(arg.ref_id)
            if arg_def is not None:
                result[arg_def.name] = arg.value
    return result


def compute_param_ref_defaults(
    refs_container: object, idx: ApplicationIndexer
) -> dict[str, str]:
    """Return {pr.id: effective_value} for all ParameterRefs in a static section.

    Tries pr.value first; falls back to the base Parameter's value via idx.
    """
    result: dict[str, str] = {}
    refs = (
        getattr(refs_container, "parameter_ref", None)
        if refs_container is not None
        else None
    )
    if not refs:
        return result
    for pr in refs:
        value = pr.value
        if value is None:
            base = idx.parameters.get(pr.ref_id)
            if base is not None:
                value = base.value
        if value is not None:
            result[pr.id] = value
    return result


class ParameterState:
    """Shared base for GlobalState and ModuleState.

    Forms a tree: root → module children → submodule children.
    Reads walk the parent chain; writes go to the node itself only.
    Text overrides (from Rename nodes) are scope-local only — no parent walk.

    Active ref sets persist after trim_to_active() and are cleared by reset_active()
    at the start of each traversal, so callers can read active_param_refs() /
    active_com_object_refs() after ui() or evaluate() returns.
    """

    __slots__ = (
        "_active_com_object_refs",
        "_active_module_keys",
        "_active_param_refs",
        "_alloc_positions",
        "_children",
        "_com_obj_instance_refs",
        "_param_ref_defaults",
        "_parent",
        "_text",
        "param_ref_id_to_value",
    )

    def __init__(
        self,
        values: dict[str, str] | None = None,
        parent: ParameterState | None = None,
        param_ref_defaults: dict[str, str] | None = None,
    ) -> None:
        self.param_ref_id_to_value: dict[str, str] = dict(values or {})
        self._parent: ParameterState | None = parent
        self._children: dict[str, ModuleState] = {}
        self._text: dict[str, str] = {}
        self._active_param_refs: set[str] = set()
        self._active_module_keys: set[str] = set()
        self._active_com_object_refs: set[str] = set()
        self._alloc_positions: dict[str, int] = {}
        self._param_ref_defaults: dict[str, str] = param_ref_defaults or {}
        self._com_obj_instance_refs: dict[str, ComObjectInstanceRef] = {}

    def get(self, ref_id: str) -> str | None:
        val = self.param_ref_id_to_value.get(ref_id)
        if val is not None:
            return val
        if self._parent is not None:
            parent_val = self._parent.get(ref_id)
            if parent_val is not None:
                return parent_val
        return self._param_ref_defaults.get(ref_id)

    def set_param_ref_defaults(self, param_ref_defaults: dict[str, str]) -> None:
        self._param_ref_defaults = param_ref_defaults

    def get_arg(self, ref_id: str) -> ModuleNumericArg | None:
        return None

    def get_arg_defaults(self) -> dict[str, str]:
        return {}

    def set(self, ref_id: str, value: str) -> None:
        self.param_ref_id_to_value[ref_id] = value

    def set_text(self, ref_id: str, text: str) -> None:
        self._text[ref_id] = text

    def get_text(self, ref_id: str) -> str | None:
        return self._text.get(ref_id)

    def mark_active_param(self, ref_id: str) -> None:
        self._active_param_refs.add(ref_id)

    def mark_active_com_object(self, ref_id: str) -> None:
        self._active_com_object_refs.add(ref_id)

    def set_com_obj_instance_ref(self, ref_id: str, coir: ComObjectInstanceRef) -> None:
        self._com_obj_instance_refs[ref_id] = coir

    def get_com_obj_instance_ref(self, ref_id: str) -> ComObjectInstanceRef | None:
        result = self._com_obj_instance_refs.get(ref_id)
        if result is not None:
            return result
        if self._parent is not None:
            return self._parent.get_com_obj_instance_ref(ref_id)
        return None

    def com_obj_instance_ref_ids(self) -> set[str]:
        """Every com-object instance ref id known to this scope and its children.

        These are the com objects the device actually instantiated (its GroupObjectTree),
        provided when reconstructing state from a project. Empty for a device configured
        from scratch (no saved instances)."""
        result = set(self._com_obj_instance_refs)
        for child in self._children.values():
            result |= child.com_obj_instance_ref_ids()
        return result

    def alloc_position(self, alloc_id: str, default: int) -> int:
        return self._alloc_positions.get(alloc_id, default)

    def set_alloc_position(self, alloc_id: str, position: int) -> None:
        self._alloc_positions[alloc_id] = position

    def reset_active(self) -> None:
        """Clear active ref sets before a new traversal."""
        self._active_param_refs.clear()
        self._active_module_keys.clear()
        self._active_com_object_refs.clear()
        self._alloc_positions.clear()
        for child in self._children.values():
            child.reset_active()

    def discard_active_refs(
        self, param_ref_ids: set[str], com_object_ref_ids: set[str]
    ) -> None:
        """Drop the given refs from the active sets (this scope and its children).

        Used to deactivate an inactive channel's parameters and com objects after the
        traversal, so a device configured with that channel disabled does not encode
        or expose them (matching the device's instantiated group objects)."""
        self._active_param_refs -= param_ref_ids
        self._active_com_object_refs -= com_object_ref_ids
        for child in self._children.values():
            child.discard_active_refs(param_ref_ids, com_object_ref_ids)

    def trim_to_active(self) -> None:
        """Remove values for param refs not marked active, then recurse into module children.

        Module children not visited during the last traversal are removed entirely so
        their parameters are not encoded when the module is inactive.

        Active ref sets are NOT cleared here — they persist so callers can read
        active_param_refs() / active_com_object_refs() after the traversal.
        """
        inactive = self.param_ref_id_to_value.keys() - self._active_param_refs
        for key in inactive:
            del self.param_ref_id_to_value[key]
        self._text.clear()
        inactive_modules = self._children.keys() - self._active_module_keys
        for key in inactive_modules:
            del self._children[key]
        for child in self._children.values():
            child.trim_to_active()

    def active_param_refs(self) -> set[str]:
        result = set(self._active_param_refs)
        for child in self._children.values():
            result.update(child.active_param_refs())
        return result

    def active_com_object_refs(self) -> set[str]:
        result = set(self._active_com_object_refs)
        for child in self._children.values():
            result.update(child.active_com_object_refs())
        return result

    def qualify(self, ref_id: str) -> str:
        return ref_id

    def find_scope_for_qualified(
        self, ref_id: str
    ) -> tuple[ParameterState, str] | None:
        for child in self._children.values():
            result = child.find_scope_for_qualified(ref_id)
            if result is not None:
                return result
        return None

    def set_instance_ref(self, ref_id: str, value: str) -> None:
        found = self.find_scope_for_qualified(ref_id)
        if found is not None:
            scope, local = found
            scope.set(local, value)
        else:
            self.set(ref_id, value)

    def clear_instance_ref(self, ref_id: str) -> None:
        found = self.find_scope_for_qualified(ref_id)
        if found is not None:
            scope, local = found
            scope.param_ref_id_to_value.pop(local, None)
        else:
            self.param_ref_id_to_value.pop(ref_id, None)

    def module_child(
        self,
        module_id: str,
        repeat_idx: int = 1,
        arguments: dict[str, ModuleArg] | None = None,
        param_ref_defaults: dict[str, str] | None = None,
        arg_defaults: dict[str, str] | None = None,
        ref_id: str | None = None,
    ) -> ModuleState:
        """Returns (creating if needed) the module instance state and wires it into the tree."""
        key = f"{module_id}_MI-{repeat_idx}"
        self._active_module_keys.add(key)
        if key not in self._children:
            child = ModuleState(
                key,
                arguments,
                param_ref_defaults=param_ref_defaults,
                arg_defaults=arg_defaults,
                ref_id=ref_id,
            )
            child._parent = self
            self._children[key] = child
        else:
            child = self._children[key]
            child._parent = self
            if ref_id is not None:
                child.ref_id = ref_id
            if arguments is not None:
                child.arguments = arguments
            if param_ref_defaults is not None:
                child.set_param_ref_defaults(param_ref_defaults)
            if arg_defaults is not None:
                child.set_arg_defaults(arg_defaults)
        return self._children[key]

    def parameter_instance_refs(self) -> dict[str, str]:
        result = dict(self.param_ref_id_to_value)
        for child in self._children.values():
            result.update(child.parameter_instance_refs())
        return result

    def module_children(self) -> list[ModuleState]:
        return list(self._children.values())

    def relative_param_values(self) -> list[tuple[str, str]]:
        """Return (def-relative_ref_id, value) pairs for all scopes.

        Unlike parameter_instance_refs(), these keys are never qualified, so they can
        be looked up directly in ApplicationIndexer.parameter_refs regardless of module nesting.
        """
        result = list(self.param_ref_id_to_value.items())
        for child in self._children.values():
            result.extend(child.relative_param_values())
        return result

    def module_instances(self) -> list[tuple[str, str, dict[str, ModuleArg]]]:
        result: list[tuple[str, str, dict[str, ModuleArg]]] = []
        for child in self._children.values():
            result.extend(child.module_instances())
        return result


class GlobalState(ParameterState):
    """Global (root) parameter state; top of the tree from which module children hang."""

    @classmethod
    def from_project(
        cls,
        parameter_instance_refs: list[ParameterInstanceRef] | None = None,
        module_instances: list[ModuleInstance] | None = None,
        com_object_instance_refs: list[ComObjectInstanceRef] | None = None,
    ) -> GlobalState:
        """Reconstruct a GlobalState tree from saved project data (parameter refs + module instance list)."""
        root = cls()
        mid_to_mdid: dict[str, str] = {}
        for mi in module_instances or []:
            if mi.id is None or mi.ref_id is None:
                continue
            ms = ModuleState(mi.id, ref_id=mi.ref_id)
            ms._parent = root
            root._children[mi.id] = ms
            mid_to_mdid[mi.id] = mi.ref_id
        for pir in parameter_instance_refs or []:
            if pir.value is None:
                continue
            ref_id, value = pir.ref_id, pir.value
            for mid, ms in root._children.items():
                p = f"_{ref_id}_".find(f"_{mid}_")
                if p != -1:
                    app_prefix = ref_id[:p]
                    suffix = ref_id[p + len(mid) :]
                    ms.module_instance_id = app_prefix + mid
                    ms.param_ref_id_to_value[app_prefix + mid_to_mdid[mid] + suffix] = (
                        value
                    )
                    break
            else:
                root.param_ref_id_to_value[ref_id] = value

        for coir in com_object_instance_refs or []:
            root._com_obj_instance_refs[coir.ref_id] = coir

        return root


class ModuleState(ParameterState):
    """Parameter state for one module instance; stores local (def-relative) ref IDs.

    parameter_instance_refs() qualifies each key by splicing module_instance_id in place of the
    shared prefix with the local ref ID — no def_ref_id needed at eval time.
    e.g. M-..._MD-1_P-5_R-5  →  M-..._MD-1_M-100_MI-2_P-5_R-5
    """

    __slots__ = ("_arg_defaults", "arguments", "module_instance_id", "ref_id")

    def __init__(
        self,
        module_instance_id: str,
        arguments: dict[str, ModuleArg] | None = None,
        param_ref_defaults: dict[str, str] | None = None,
        arg_defaults: dict[str, str] | None = None,
        ref_id: str | None = None,
    ) -> None:
        super().__init__(param_ref_defaults=param_ref_defaults)
        self.module_instance_id = module_instance_id
        self.ref_id: str | None = ref_id
        self.arguments: dict[str, ModuleArg] = arguments or {}
        self._arg_defaults: dict[str, str] = arg_defaults or {}

    def get_arg_defaults(self) -> dict[str, str]:
        return self._arg_defaults

    def set_arg_defaults(self, arg_defaults: dict[str, str]) -> None:
        self._arg_defaults = arg_defaults

    def get_arg(self, ref_id: str) -> ModuleNumericArg | None:
        arg = self.arguments.get(ref_id)
        return arg if isinstance(arg, ModuleNumericArg) else None

    def as_module_instance(self) -> tuple[str, str, dict[str, ModuleArg]]:
        instance_id = self.module_instance_id
        ref_id = (
            self.ref_id if self.ref_id is not None else instance_id.rsplit("_MI-", 1)[0]
        )
        args = {k[k.find("_MD-") + 1 :]: v for k, v in self.arguments.items()}
        return instance_id, ref_id, args

    def qualify(self, ref_id: str) -> str:
        return self._qualify(ref_id)

    def find_scope_for_qualified(
        self, ref_id: str
    ) -> tuple[ParameterState, str] | None:
        mid = self.module_instance_id
        if not ref_id.startswith(mid + "_"):
            return None
        for child in self._children.values():
            result = child.find_scope_for_qualified(ref_id)
            if result is not None:
                return result
        suffix = ref_id[len(mid) :]
        if self.ref_id is None:
            return None
        return (self, self.ref_id + suffix)

    def _qualify(self, ref_id: str) -> str:
        i, n = 0, min(len(self.module_instance_id), len(ref_id))
        while i < n and self.module_instance_id[i] == ref_id[i]:
            i += 1
        return self.module_instance_id + ref_id[i - 1 :]

    def active_param_refs(self) -> set[str]:
        result = {self.qualify(ref) for ref in self._active_param_refs}
        for child in self._children.values():
            result.update(child.active_param_refs())
        return result

    def active_com_object_refs(self) -> set[str]:
        result = {self.qualify(ref) for ref in self._active_com_object_refs}
        for child in self._children.values():
            result.update(child.active_com_object_refs())
        return result

    def parameter_instance_refs(self) -> dict[str, str]:
        result = {self._qualify(k): v for k, v in self.param_ref_id_to_value.items()}
        for child in self._children.values():
            result.update(child.parameter_instance_refs())
        return result

    def module_instances(self) -> list[tuple[str, str, dict[str, ModuleArg]]]:
        result: list[tuple[str, str, dict[str, ModuleArg]]] = [
            self.as_module_instance()
        ]
        for child in self._children.values():
            result.extend(child.module_instances())
        return result


__all__ = [
    "GlobalState",
    "ModuleState",
    "compute_arg_defaults",
    "compute_param_ref_defaults",
]
