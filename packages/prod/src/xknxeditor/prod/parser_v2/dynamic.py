from __future__ import annotations

from collections.abc import Mapping

from xknxeditor.namespaces.intermediate import (
    ApplicationProgram,
    ApplicationProgramChannel,
    ApplicationProgramDynamic,
    Assign,
    BinaryDataRef,
    Button,
    ChannelChoose,
    ChannelIndependentBlock,
    ComObjectInstanceRef,
    ComObjectParameterBlock,
    ComObjectParameterChoose,
    ComObjectRefRef,
    DependentChannelChoose,
    Module,
    ModuleArg,
    ModuleInstance,
    ParameterInstanceRef,
    ParameterRefRef,
    ParameterSeparator,
    Rename,
    Repeat,
)

from .application_indexer import ApplicationIndexer
from .calculation import evaluate_lr, evaluate_rl
from .context import EvalCapture, EvalContext
from .encode import (
    MemWrite,
    PropertyKey,
    PropWrite,
    Writes,
    build_memory_param_map,
    build_property_param_map,
    collect_writes,
    decode_memory_parameters,
    decode_module_parameters,
    decode_property_parameters,
    encode_to_memory,
    encode_to_memory_masked,
    encode_to_properties,
    resolve_param_values,
    written_bit_mask,
)
from .nodes import (
    AssignNode,
    BinaryDataRefNode,
    ButtonNode,
    ChannelNode,
    ChooseWhenNode,
    ComObjectParameterBlockNode,
    ComObjectRefRefNode,
    DynamicNode,
    GenericCollectionNode,
    ModuleNode,
    ParameterRefRefNode,
    ParameterSeparatorNode,
    RenameNode,
    RepeatNode,
)
from .state import GlobalState, compute_arg_defaults, compute_param_ref_defaults
from .ui import UiNode

__all__ = [
    "AssignNode",
    "BinaryDataRefNode",
    "ButtonNode",
    "ChooseWhenNode",
    "ComObjectRefRefNode",
    "DynamicNode",
    "DynamicTreeBuilder",
    "DynamicUI",
    "EvalContext",
    "GenericCollectionNode",
    "MemWrite",
    "ModuleNode",
    "ParameterRefRefNode",
    "ParameterSeparatorNode",
    "PropWrite",
    "PropertyKey",
    "RenameNode",
    "RepeatNode",
    "Writes",
    "build_memory_param_map",
    "build_property_param_map",
    "collect_writes",
    "decode_memory_parameters",
    "decode_module_parameters",
    "decode_property_parameters",
    "encode_to_memory",
    "encode_to_memory_masked",
    "encode_to_properties",
    "resolve_param_values",
    "written_bit_mask",
]


class _AppNode(DynamicNode):
    """Top wrapper that seeds global param-ref defaults before the app tree evaluates."""

    def __init__(
        self, subtree: DynamicNode, param_ref_defaults: dict[str, str]
    ) -> None:
        self._subtree = subtree
        self._param_ref_defaults = param_ref_defaults

    def eval(self, ctx: EvalContext) -> list[UiNode]:
        ctx.seed_param_ref_defaults(self._param_ref_defaults)
        return self._subtree.eval(ctx)


class DynamicTreeBuilder:
    """Constructs an ApplicationProgram's eval tree, pre-resolving Module refs into
    subtrees so evaluation never re-reads the IR."""

    def __init__(self, app: ApplicationProgram) -> None:
        self.idx = ApplicationIndexer(app)
        self._app_id = app.id
        # Param-refs rendered as a widget somewhere in the app, collected during _build. A Choose/Repeat
        # gate parameter that is never a widget (a purely structural/dummy selector) can never be marked
        # active, so it must not gate the capture chain (would wrongly disqualify every object under it).
        # This set is shared by reference into the Choose/Repeat nodes and is complete once _build ends.
        self._widget_param_refs: set[str] = set()
        # Some applications (e.g. simple power supplies / couplers) carry no <Dynamic> section, or
        # one that produces no tree. Such a device has no parameters/objects to show — build an
        # empty tree so it still appears in the project instead of failing to load.
        node = self._build(app.dynamic) if app.dynamic is not None else None
        if node is None:
            node = GenericCollectionNode([])
        global_param_ref_defaults = compute_param_ref_defaults(
            app.static.parameter_refs, self.idx
        )
        self.tree: DynamicNode = _AppNode(node, global_param_ref_defaults)

    def _build(self, elem: object) -> DynamicNode | None:
        if isinstance(elem, ApplicationProgramDynamic):
            return GenericCollectionNode([self._build(child) for child in elem.choice])
        elif isinstance(elem, ChannelIndependentBlock):
            return ChannelNode(
                [self._build(child) for child in elem.choice],
                id=f"{self._app_id}_general",
                name="General",
            )
        elif isinstance(elem, ApplicationProgramChannel):
            return ChannelNode(
                [self._build(child) for child in elem.choice],
                id=elem.id,
                name=elem.name,
                text=elem.text,
                number=elem.number,
                icon=elem.icon,
                text_parameter_ref_id=elem.text_parameter_ref_id,
            )
        elif isinstance(elem, ComObjectParameterBlock):
            # The importer labels a block with its heading parameter's (ParamRefId) Text when it has one — e.g.
            # a channel-prefixed "A: Drive" — in preference to the block's generic Name ("Jalousie X: …").
            heading_text: str | None = None
            if elem.param_ref_id:
                pr = self.idx.parameter_refs.get(elem.param_ref_id)
                param = self.idx.parameters.get(pr.ref_id) if pr else None
                heading_text = (getattr(pr, "text", None) or None) or (
                    param.text if param else None
                )
            return ComObjectParameterBlockNode(
                elem,
                [self._build(child) for child in elem.choice],
                heading_text,
            )
        elif isinstance(
            elem, (DependentChannelChoose, ChannelChoose, ComObjectParameterChoose)
        ):
            # Choose blocks pick content by parameter value: DependentChannelChoose
            # toggles root-level channels, ChannelChoose the content inside a channel,
            # ComObjectParameterChoose the content inside a parameter block.
            default_nodes: list[DynamicNode | None] | None = None
            condition_to_nodes: dict[str, list[DynamicNode | None]] = {}
            for when in elem.when:
                built = [self._build(node) for node in when.choice]
                if when.default:
                    # Module definitions can repeat a branch (e.g. the same test resolves per
                    # module instance); merge rather than assert so the device still loads.
                    default_nodes = (default_nodes or []) + built
                if when.test is not None:
                    condition_to_nodes.setdefault(when.test, []).extend(built)
            return ChooseWhenNode(
                elem.param_ref_id,
                condition_to_nodes,
                default_nodes,
                self._widget_param_refs,
            )
        elif isinstance(elem, Repeat):
            # TODO: index substitution for non-Module children still missing
            return RepeatNode(
                elem,
                [self._build(child) for child in elem.choice],
                self._widget_param_refs,
            )
        elif isinstance(elem, Module):
            ref_id = elem.ref_id
            mod_def = self.idx.module_defs.get(ref_id)
            if mod_def is None or mod_def.dynamic is None:
                return None
            children = [self._build(child) for child in mod_def.dynamic.choice]
            arguments: dict[str, ModuleArg] = {arg.ref_id: arg for arg in elem.choice}
            param_ref_defaults = compute_param_ref_defaults(
                mod_def.static.parameter_refs if mod_def.static else None, self.idx
            )
            arg_defaults = compute_arg_defaults(mod_def.arguments, list(elem.choice))
            arg_names = (
                {a.id: a.name for a in mod_def.arguments.argument if a.name}
                if mod_def.arguments is not None
                else {}
            )
            return ModuleNode(
                elem.id,
                GenericCollectionNode(children),
                ref_id,
                arguments,
                param_ref_defaults,
                arg_defaults,
                arg_names,
            )
        elif isinstance(elem, ParameterRefRef):
            # Leaf parameter widget; resolve ParameterRef/Parameter/ParameterType now
            pr = self.idx.parameter_refs.get(elem.ref_id)
            assert pr is not None, f"ParameterRef {elem.ref_id!r} not found in static"
            param = self.idx.parameters.get(pr.ref_id)
            assert param is not None, f"Parameter {pr.ref_id!r} not found in static"
            pt = self.idx.parameter_types.get(param.parameter_type)
            assert pt is not None, (
                f"ParameterType {param.parameter_type!r} not found in static"
            )
            assert not pt.plugin, (
                f"ParameterType {param.parameter_type!r} uses unsupported plugin {pt.plugin!r}"
            )
            # Record this ref as widget-rendered so Choose/Repeat gates on it count toward activeness.
            self._widget_param_refs.add(elem.ref_id)
            return ParameterRefRefNode(elem, pr, param, pt)
        elif isinstance(elem, ComObjectRefRef):
            cor = self.idx.com_object_refs.get(elem.ref_id)
            co = self.idx.com_objects.get(cor.ref_id) if cor else None
            return ComObjectRefRefNode(elem, cor, co)
        elif isinstance(elem, ParameterSeparator):
            # Leaf: label or divider between parameters
            return ParameterSeparatorNode(elem)
        elif isinstance(elem, Button):
            # Leaf: button wired to a load-procedure action
            return ButtonNode(elem)
        elif isinstance(elem, BinaryDataRef):
            # Leaf: binary blob from the application's Static section
            return BinaryDataRefNode(elem)
        elif isinstance(elem, Assign):
            # Leaf: pins a parameter to a fixed value; state-only, no UI
            return AssignNode(elem)
        elif isinstance(elem, Rename):
            # Leaf: renames a channel or element inside a choose branch
            return RenameNode(elem)
        return None


def _subtree_activeness(node: UiNode, instantiated: set[str]) -> tuple[bool, bool]:
    """Return ``(has_com_object, has_instantiated_com_object)`` for ``node``'s subtree."""
    from .ui import UiComObject, UiParameterBlock, UiTab

    has_co = has_inst = False
    stack: list[UiNode] = [node]
    while stack:
        current = stack.pop()
        if isinstance(current, UiComObject):
            has_co = True
            if current.ref_id in instantiated:
                has_inst = True
        elif isinstance(current, (UiTab, UiParameterBlock)):
            stack.extend(current.children)
    return has_co, has_inst


def _collect_refs(node: UiNode, params: set[str], cos: set[str]) -> None:
    """Add every UiParameter and UiComObject ref id in ``node``'s subtree."""
    from .ui import UiComObject, UiParameter, UiParameterBlock, UiTab

    stack: list[UiNode] = [node]
    while stack:
        current = stack.pop()
        if isinstance(current, UiComObject):
            cos.add(current.ref_id)
        elif isinstance(current, UiParameter):
            params.add(current.ref_id)
        elif isinstance(current, (UiTab, UiParameterBlock)):
            stack.extend(current.children)


def _prune_inactive(
    nodes: list[UiNode],
    instantiated: set[str],
    dropped_params: set[str],
    dropped_cos: set[str],
    kept_params: set[str],
    kept_cos: set[str],
) -> list[UiNode]:
    """Drop inactive-channel sections; record dropped vs kept parameter/com-object refs.

    A ``UiTab``/``UiParameterBlock`` whose subtree carries com objects but none is
    instantiated is dropped (its refs go to ``dropped_*``). Surviving containers are
    pruned recursively; their leaf refs go to ``kept_*`` so a ref shared with a live
    section is never deactivated."""
    import dataclasses

    from .ui import UiComObject, UiParameter, UiParameterBlock, UiTab

    result: list[UiNode] = []
    for node in nodes:
        if isinstance(node, (UiTab, UiParameterBlock)):
            has_co, has_inst = _subtree_activeness(node, instantiated)
            if has_co and not has_inst:
                _collect_refs(node, dropped_params, dropped_cos)
                continue
            pruned = _prune_inactive(
                list(node.children),
                instantiated,
                dropped_params,
                dropped_cos,
                kept_params,
                kept_cos,
            )
            result.append(dataclasses.replace(node, children=tuple(pruned)))
        else:
            if isinstance(node, UiComObject):
                kept_cos.add(node.ref_id)
            elif isinstance(node, UiParameter):
                kept_params.add(node.ref_id)
            result.append(node)
    return result


class DynamicUI:
    __slots__ = ("_app", "_idx", "_state", "_tree", "_ui")

    def __init__(
        self,
        app: ApplicationProgram,
        parameter_instance_refs: list[ParameterInstanceRef] | None = None,
        module_instances: list[ModuleInstance] | None = None,
        com_object_instance_refs: list[ComObjectInstanceRef] | None = None,
    ) -> None:
        builder = DynamicTreeBuilder(app)
        self._app = app
        self._tree = builder.tree
        self._idx = builder.idx
        self._state = GlobalState.from_project(
            parameter_instance_refs=parameter_instance_refs,
            module_instances=module_instances,
            com_object_instance_refs=com_object_instance_refs,
        )
        self._ui: list[UiNode] | None = None

    def ui(self) -> list[UiNode]:
        if self._ui is None:
            self._state.reset_active()
            self._ui = self._tree.eval(EvalContext(self._state, idx=self._idx))
            self._state.trim_to_active()
            self._prune_inactive_channels()
        return self._ui

    def _prune_inactive_channels(self) -> None:
        """Drop UI sections of channels the device did not instantiate.

        When a project provides the instantiated com objects (an imported device),
        a section that carries com objects of which none is instantiated is an
        inactive channel: the parameter-driven UI over-activates it at its defaults
        (e.g. the individual A/B/C/D channels of a dimmer set to "2x Tunable White"),
        but activeness is derived from the stored group objects. Such sections are
        removed from the UI and their parameters/com objects (those exclusive to the
        dropped sections) are deactivated, so they are neither shown nor encoded."""
        instantiated = self._state.com_obj_instance_ref_ids()
        if not instantiated or self._ui is None:
            return
        dropped_params: set[str] = set()
        dropped_cos: set[str] = set()
        kept_params: set[str] = set()
        kept_cos: set[str] = set()
        self._ui = _prune_inactive(
            self._ui, instantiated, dropped_params, dropped_cos, kept_params, kept_cos
        )
        # Only deactivate refs that do not also occur in a surviving section.
        self._state.discard_active_refs(
            dropped_params - kept_params, dropped_cos - kept_cos
        )

    def eval_unpruned_ui(self) -> list[UiNode]:
        """Evaluate the dynamic tree against the CURRENT parameters WITHOUT the inactive-channel
        prune, returning the resulting UI nodes. Used to compute the parameter-driven "should-exist"
        com-object set — ``_prune_inactive_channels`` biases toward the stale saved instances, so it
        must be skipped here. Invalidates the cached ``ui()`` so the next call recomputes (and
        re-prunes) cleanly."""
        self._state.reset_active()
        tree = self._tree.eval(EvalContext(self._state, idx=self._idx))
        self._state.trim_to_active()
        self._ui = None
        return tree

    def com_objects_controlled_by(self, param_ref_id: str) -> set[str]:
        """The (instance-qualified) com-object ref-ids that ``param_ref_id`` gates at the CURRENT
        parameter value: every com-object emitted under a Choose/Repeat driven by that parameter.
        Invalidates the cached ``ui()`` so the next call recomputes cleanly."""
        capture = EvalCapture(param_ref_id)
        self._state.reset_active()
        self._tree.eval(EvalContext(self._state, idx=self._idx, capture=capture))
        self._state.trim_to_active()
        self._ui = None
        return capture.controlled_ref_ids()

    def active_parameter_driven_com_object_ref_ids(self) -> set[str]:
        """The com-object ref-ids the device should instantiate for its CURRENT parameter values —
        the parameter-driven active set, matching what a genuine import materialises.

        Computed in a single eval via chain-AND: an object is included iff some emission of it has EVERY
        Choose/Repeat gate on its path driven by an ACTIVE parameter (a parameter is active iff it is
        rendered as a widget somewhere), or it is ungated (an unconditional/global object). This keeps
        channels a function genuinely activates (their selector parameter is active) and the
        always-present objects, while excluding the channel over-activation of the raw tree — e.g. an
        individual channel whose objects sit under an outer selector that is NOT active because its
        widget only lives in a different function branch. Invalidates the cached ``ui()``."""
        capture = EvalCapture(None)  # record every emitted object's gate chain
        self._state.reset_active()
        self._tree.eval(EvalContext(self._state, idx=self._idx, capture=capture))
        self._state.trim_to_active()
        self._ui = None
        active = self._state.active_param_refs() or set()
        return capture.active_ref_ids(frozenset(active))

    def get_module_instances(self) -> list[tuple[str, str]]:
        """After eval, list ``(instance_id, ref_id)`` per top-level module instance."""
        self.ui()
        return [(iid, rid) for iid, rid, _ in self._state.module_instances()]

    def set_com_obj_instance_ref(self, ref_id: str, coir: ComObjectInstanceRef) -> None:
        self._state.set_com_obj_instance_ref(ref_id, coir)
        self._ui = None

    def instantiated_com_object_ref_ids(self) -> set[str]:
        """Com-object ref ids the device actually instantiated (from saved project state).

        Empty for a device configured from scratch. A download uses this as the
        authoritative set of active com objects (matching the device GroupObjectTree),
        rather than the parameter-driven visible set, which can over-activate objects
        of channel modes the device is not in."""
        return self._state.com_obj_instance_ref_ids()

    def segment_base_addrs(self) -> dict[str, int]:
        return {
            sid: self._idx.segment_base_addr(sid) for sid in self._idx.code_segments
        }

    def encode_to_memory(self) -> dict[str, bytes]:
        """Pack the current parameter state into per-segment byte buffers."""
        self.ui()  # refresh state
        return encode_to_memory(
            self._app,
            self._idx,
            resolve_param_values(self._idx, self._state),
            self._state,
        )

    def encode_to_memory_masked(self) -> dict[str, tuple[bytes, bytes]]:
        """Encode into ``{segment_id: (data, mask)}``; mask marks written bytes."""
        self.ui()  # refresh state
        return encode_to_memory_masked(
            self._app,
            self._idx,
            resolve_param_values(self._idx, self._state),
            self._state,
        )

    def decode_memory_parameters(
        self, segments: Mapping[str, bytes]
    ) -> dict[str, str | None]:
        """Best-effort inverse of :meth:`encode_to_memory` for recovering values.

        Decodes each top-level static memory parameter's value from the given
        segment bytes (read off a device). ``None`` marks a parameter whose type
        cannot be reconstructed from bytes alone; module-instanced parameters are
        skipped (see :func:`decode_memory_parameters`).
        """
        self.ui()
        return decode_memory_parameters(self._app, self._idx, segments, self._state)

    def decode_property_parameters(
        self, properties: Mapping[PropertyKey, bytes]
    ) -> dict[str, str | None]:
        """Best-effort inverse of :meth:`encode_to_properties` for recovering values.

        Decodes each top-level static property-backed parameter's value from the
        given property bytes (read off a device). ``None`` marks an unreconstructable
        value; module-instanced parameters are skipped (see
        :func:`decode_property_parameters`).
        """
        self.ui()
        return decode_property_parameters(self._app, self._idx, properties, self._state)

    def decode_module_parameters(
        self,
        segments: Mapping[str, bytes],
        properties: Mapping[PropertyKey, bytes],
    ) -> dict[str, str | None]:
        """Decode module-instance parameter values from device memory/properties.

        Uses this UI's evaluated module instances (seed it from the recovered
        top-level parameters first, so the instances match the device). Returns
        ``{qualified_parameter_ref_id: value}``; ``None`` marks unreconstructable
        values.
        """
        self.ui()
        return decode_module_parameters(
            self._app, self._idx, self._state, segments, properties
        )

    def memory_param_map(self) -> dict[str, dict[int, tuple[str, str]]]:
        """Map {seg_id: {byte_offset: (param_id, value)}} for hex-viewer hovers."""
        self.ui()
        return build_memory_param_map(
            self._app,
            self._idx,
            resolve_param_values(self._idx, self._state),
            self._state,
        )

    def written_bit_mask(self) -> dict[str, bytes]:
        """Return {seg_id: bit_mask} marking the bits an active parameter writes.

        Bit granular (one bit per written bit), unlike the byte-granular mask of
        :meth:`encode_to_memory_masked`. A pre-flight uses it to tell a real
        parameter value apart from a bit only rewritten to the segment seed.
        """
        self.ui()
        return written_bit_mask(
            self._app,
            self._idx,
            resolve_param_values(self._idx, self._state),
            self._state,
        )

    def encode_to_properties(self) -> dict[PropertyKey, bytes]:
        """Pack PropertyParameter-backed values into interface-object property data."""
        self.ui()
        return encode_to_properties(
            self._app,
            self._idx,
            resolve_param_values(self._idx, self._state),
            self._state,
        )

    def property_param_map(self) -> dict[PropertyKey, dict[int, tuple[str, str]]]:
        """Map {(object_index, property_id, occurrence): {byte_offset: (param_id, value)}}."""
        self.ui()
        return build_property_param_map(
            self._app,
            self._idx,
            resolve_param_values(self._idx, self._state),
            self._state,
        )

    def get_parameter_ref(self, ref_id: str) -> str | None:
        """Current value of a parameter ref in this UI state (None if unset)."""
        return self._state.get(ref_id)

    def set_parameter_ref(self, ref_id: str, value: str) -> None:
        active = self._state.active_param_refs()
        if active and ref_id not in active:
            raise ValueError(
                f"parameter ref {ref_id!r} is not active in the current UI state"
            )
        self._state.set_instance_ref(ref_id, value)
        self._ui = None
        script = self._idx.script
        for calc in self._idx.calculations_for_l(ref_id):
            l_values = {
                pr.alias_name or pr.ref_id: self._state.get(pr.ref_id) or ""
                for pr in calc.lparameters.parameter_ref_ref
            }
            try:
                r_values = evaluate_lr(calc, l_values, script)
            except NotImplementedError:
                continue
            for pr in calc.rparameters.parameter_ref_ref:
                v = r_values.get(pr.alias_name or pr.ref_id)
                if v is not None:
                    self._state.set_instance_ref(pr.ref_id, v)
                else:
                    self._state.clear_instance_ref(pr.ref_id)
        for calc in self._idx.calculations_for_r(ref_id):
            r_values = {
                pr.alias_name or pr.ref_id: self._state.get(pr.ref_id) or ""
                for pr in calc.rparameters.parameter_ref_ref
            }
            try:
                l_values = evaluate_rl(calc, r_values, script)
            except NotImplementedError:
                continue
            for pr in calc.lparameters.parameter_ref_ref:
                v = l_values.get(pr.alias_name or pr.ref_id)
                if v is not None:
                    self._state.set_instance_ref(pr.ref_id, v)
                else:
                    self._state.clear_instance_ref(pr.ref_id)
