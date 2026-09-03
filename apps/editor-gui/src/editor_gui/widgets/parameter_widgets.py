from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from imgui_bundle import imgui

from editor_gui.device import Device
from editor_gui.widgets.strings import S
from xknxmono.models.intermediate.parameter_block_layout_t import ParameterBlockLayout
from xknxmono.product.parser_v2.ui import (
    UiComObject,
    UiNode,
    UiParameter,
    UiParameterBlock,
    UiSeparator,
    UiTab,
)
from xknxmono.product.parser_v2.ui.parameter import (
    CheckBoxWidget,
    EnumWidget,
    NumberSliderWidget,
    NumberWidget,
    PictureWidget,
    TextWidget,
)

# ETS marks parameters changed from their default; we tint the label to match.
_CHANGED_COLOR = imgui.ImVec4(0.36, 0.71, 1.0, 1.0)


def _default_display(param: UiParameter) -> str:
    """Human-readable default value (enum default resolved to its label)."""
    if isinstance(param.widget, EnumWidget):
        for choice in param.widget.choices:
            if str(choice.value) == param.default_value:
                return choice.label
    return param.default_value or "-"


@dataclass
class EnumPopupRequest:
    device: Device
    param: UiParameter


def render_param_widget(
    param: UiParameter,
    widget_id: str,
    on_change: Callable[[str], None],
    deferred_enum: bool = False,
    differs: bool = False,
) -> EnumPopupRequest | None:
    """``differs`` (multi-device edit): the parameter's value diverges across the selected devices,
    so show a ``<differs>`` placeholder instead of one device's value. Any edit still writes the
    chosen value to all of them via ``on_change``."""
    match param.widget:
        case EnumWidget() as w:
            current_idx = 0
            for i, choice in enumerate(w.choices):
                if str(choice.value) == param.value:
                    current_idx = i
                    break
            preview = w.choices[current_idx].label if w.choices else param.value
            if differs:
                preview = S.PARAM_DIFFERS
            if deferred_enum:
                if imgui.button(f"{preview}##{widget_id}", imgui.ImVec2(-1, 0)):
                    return EnumPopupRequest(device=None, param=param)  # type: ignore[arg-type]
            else:
                if imgui.begin_combo(f"##{widget_id}", preview):
                    for choice in w.choices:
                        selected = not differs and str(choice.value) == param.value
                        if imgui.selectable(choice.label, selected)[0]:
                            on_change(str(choice.value))
                    imgui.end_combo()
        case NumberWidget() | NumberSliderWidget() as w:
            _render_int_param(
                widget_id,
                "" if differs else param.value,
                w.min,
                w.max,
                on_change,
                differs,
            )
        case CheckBoxWidget():
            if differs:
                _render_differs_text(widget_id, on_change)
            else:
                checked = param.value == "1"
                changed, new_checked = imgui.checkbox(f"##{widget_id}", checked)
                if changed:
                    on_change("1" if new_checked else "0")
        case TextWidget():
            _render_text_param(widget_id, param.value, on_change, differs)
        case PictureWidget():
            imgui.text_disabled(S.NODE_IMAGE_PLACEHOLDER)
        case _:
            _render_text_param(widget_id, param.value, on_change, differs)
    return None


def _render_text_param(
    widget_id: str, value: str, on_change: Callable[[str], None], differs: bool
) -> None:
    if differs:
        _, new_value = imgui.input_text_with_hint(f"##{widget_id}", S.PARAM_DIFFERS, "")
    else:
        _, new_value = imgui.input_text(f"##{widget_id}", value)
    if imgui.is_item_deactivated_after_edit() and (not differs or new_value):
        on_change(new_value)


def _render_differs_text(widget_id: str, on_change: Callable[[str], None]) -> None:
    """A checkbox cannot show a third "differs" state, so offer an explicit Off/On choice that,
    once picked, writes the same value to every selected device."""
    if imgui.begin_combo(f"##{widget_id}", S.PARAM_DIFFERS):
        if imgui.selectable(S.PARAM_OFF, False)[0]:
            on_change("0")
        if imgui.selectable(S.PARAM_ON, False)[0]:
            on_change("1")
        imgui.end_combo()


def _render_int_param(
    widget_id: str,
    value: str,
    min_value: int | None,
    max_value: int | None,
    on_change: Callable[[str], None],
    differs: bool = False,
) -> None:
    if differs:
        _, new_text = imgui.input_text_with_hint(
            f"##{widget_id}", S.PARAM_DIFFERS, "", imgui.InputTextFlags_.chars_decimal
        )
        if not (imgui.is_item_deactivated_after_edit() and new_text):
            return
    else:
        _, new_text = imgui.input_text(
            f"##{widget_id}", value, imgui.InputTextFlags_.chars_decimal
        )
        if not imgui.is_item_deactivated_after_edit():
            return
    try:
        clamped = int(new_text)
    except ValueError:
        clamped = min_value if min_value is not None else 0
    if min_value is not None:
        clamped = max(min_value, clamped)
    if max_value is not None:
        clamped = min(max_value, clamped)
    if differs or str(clamped) != value:
        on_change(str(clamped))


def _flatten_params(nodes: list[UiNode] | tuple[UiNode, ...]) -> list[UiParameter]:
    params: list[UiParameter] = []
    for node in nodes:
        if isinstance(node, UiParameter):
            params.append(node)
        elif isinstance(node, (UiTab, UiParameterBlock)):
            params.extend(_flatten_params(node.children))
    return params


def differing_param_refs(devices: list[Device]) -> frozenset[str]:
    """ref_ids whose value diverges across ``devices`` (multi-device edit). Devices are expected to
    share an application, so ref_ids line up. Builds each device's UI tree — the caller must cache
    the result (do not call per frame)."""
    if len(devices) < 2:
        return frozenset()
    seen: dict[str, str] = {}
    diff: set[str] = set()
    for device in devices:
        for p in _flatten_params(device.get_ui()):
            if p.ref_id in seen:
                if seen[p.ref_id] != p.value:
                    diff.add(p.ref_id)
            else:
                seen[p.ref_id] = p.value
    return frozenset(diff)


def _all_blocks(nodes: list[UiNode] | tuple[UiNode, ...]) -> list[UiParameterBlock]:
    out: list[UiParameterBlock] = []
    for node in nodes:
        if isinstance(node, UiParameterBlock):
            out.append(node)
            out.extend(_all_blocks(node.children))
        elif isinstance(node, UiTab):
            out.extend(_all_blocks(node.children))
    return out


def _ancestor_blocks(
    nodes: list[UiNode] | tuple[UiNode, ...],
    ref_id: str,
    stack: tuple[UiParameterBlock, ...] = (),
) -> tuple[UiParameterBlock, ...] | None:
    """The chain of ``UiParameterBlock`` ancestors (outermost first) of the parameter ``ref_id``."""
    for node in nodes:
        if isinstance(node, UiParameter):
            if node.ref_id == ref_id:
                return stack
        elif isinstance(node, UiTab):
            found = _ancestor_blocks(node.children, ref_id, stack)
            if found is not None:
                return found
        elif isinstance(node, UiParameterBlock):
            found = _ancestor_blocks(node.children, ref_id, (*stack, node))
            if found is not None:
                return found
    return None


def _block_signature(block: UiParameterBlock) -> tuple[tuple[str, str], ...]:
    """Structural fingerprint of a block: (label, widget-type) of each parameter it contains. Two
    repeated channels of the same type share this signature regardless of the channel's own name."""
    return tuple(
        (p.label, type(p.widget).__name__) for p in _flatten_params(block.children)
    )


def channel_apply_targets(nodes: list[UiNode], ref_id: str) -> list[str]:
    """ref_ids of the *same* parameter in every other repeated channel — for "apply to all channels".

    A device like an OpenKNX PresenceModule expands its channels (PM 1, PM 2, …) into structurally
    identical parameter blocks (no ETS module link). Given a parameter the user just edited, this
    finds its channel block (the outermost ancestor block whose structure repeats elsewhere in the
    tree) and returns the ref_id of the positionally-corresponding parameter in each twin block. The
    label must also match, so a channel currently showing a different (conditionally visible)
    structure is skipped rather than mis-mapped. Empty when the parameter is not inside a repeated
    channel."""
    chain = _ancestor_blocks(nodes, ref_id)
    if not chain:
        return []
    blocks = _all_blocks(nodes)
    counts: dict[tuple[tuple[str, str], ...], int] = {}
    sig_by_block: dict[int, tuple[tuple[str, str], ...]] = {}
    for block in blocks:
        sig = _block_signature(block)
        sig_by_block[id(block)] = sig
        counts[sig] = counts.get(sig, 0) + 1
    # Channel unit = the outermost ancestor block whose structure occurs more than once.
    channel_block = next(
        (b for b in chain if counts.get(sig_by_block[id(b)], 0) >= 2), None
    )
    if channel_block is None:
        return []
    sig = sig_by_block[id(channel_block)]
    params = _flatten_params(channel_block.children)
    idx = next((i for i, p in enumerate(params) if p.ref_id == ref_id), None)
    if idx is None:
        return []
    label = params[idx].label
    targets: list[str] = []
    for block in blocks:
        if block is channel_block or sig_by_block[id(block)] != sig:
            continue
        twin = _flatten_params(block.children)
        if idx < len(twin) and twin[idx].label == label:
            targets.append(twin[idx].ref_id)
    return targets


def count_parameters(nodes: list[UiNode] | tuple[UiNode, ...]) -> int:
    count = 0
    for node in nodes:
        if isinstance(node, UiParameter):
            count += 1
        elif isinstance(node, (UiTab, UiParameterBlock)):
            count += count_parameters(node.children)
    return count


def _node_matches(node: UiNode, needle: str) -> bool:
    """Whether ``node`` or any descendant has a label containing ``needle`` (lowercased)."""
    if isinstance(node, UiParameter):
        return needle in node.label.lower()
    if isinstance(node, (UiTab, UiParameterBlock)):
        label = (
            getattr(node, "text", None) or getattr(node, "name", None) or ""
        ).lower()
        if needle in label:
            return True
        return any(_node_matches(c, needle) for c in node.children)
    return False


def render_ui_tree(
    device: Device,
    nodes: list[UiNode],
    on_change: Callable[[Device, str, str], None],
    deferred_enum: bool = False,
    filter_text: str = "",
    differing_refs: frozenset[str] = frozenset(),
) -> EnumPopupRequest | None:
    """Render a UiNode list as a tab bar (one tab per UiTab channel).

    ``filter_text`` (case-insensitive) hides parameter blocks/parameters that neither match nor
    contain a match; matching blocks are auto-expanded. ``differing_refs`` (multi-device edit) is
    the set of ref_ids whose value diverges across the selected devices; those show ``<differs>``."""
    if not nodes:
        return None
    needle = filter_text.lower().strip()
    popup_request: EnumPopupRequest | None = None
    tabs = [n for n in nodes if isinstance(n, UiTab)]
    if tabs:
        if imgui.begin_tab_bar(f"##tabs_{device.node_id}"):
            for tab in tabs:
                if needle and not _node_matches(tab, needle):
                    continue
                label = tab.text or tab.name or tab.id or "Tab"
                if imgui.begin_tab_item(f"{label}##{device.node_id}_{tab.id}")[0]:
                    req = _render_children(
                        device,
                        tab.children,
                        on_change,
                        deferred_enum,
                        f"{device.node_id}_{tab.id}",
                        needle,
                        differing_refs,
                    )
                    if req is not None:
                        popup_request = req
                    imgui.end_tab_item()
            imgui.end_tab_bar()
    else:
        req = _render_children(
            device,
            tuple(nodes),
            on_change,
            deferred_enum,
            str(device.node_id),
            needle,
            differing_refs,
        )
        if req is not None:
            popup_request = req
    return popup_request


def _render_children(
    device: Device,
    children: tuple[UiNode, ...],
    on_change: Callable[[Device, str, str], None],
    deferred_enum: bool,
    prefix: str,
    needle: str = "",
    differing_refs: frozenset[str] = frozenset(),
) -> EnumPopupRequest | None:
    popup_request: EnumPopupRequest | None = None
    pending_params: list[UiParameter] = []
    table_idx = 0

    def flush() -> None:
        nonlocal popup_request, table_idx
        if not pending_params:
            return
        req = _render_param_table(
            device,
            pending_params,
            on_change,
            deferred_enum,
            f"{prefix}_{table_idx}",
            differing_refs,
        )
        table_idx += 1
        if req is not None:
            popup_request = req
        pending_params.clear()

    for node in children:
        if isinstance(node, UiParameter):
            if not needle or needle in node.label.lower():
                pending_params.append(node)
        elif isinstance(node, UiParameterBlock):
            if needle and not _node_matches(node, needle):
                continue
            flush()
            req = _render_block(
                device, node, on_change, deferred_enum, prefix, needle, differing_refs
            )
            if req is not None:
                popup_request = req
        elif isinstance(node, UiSeparator):
            if needle:
                continue  # separators are noise while filtering
            flush()
            _render_separator(node)
        elif isinstance(node, UiComObject):
            pass  # shown in the com flags panel

    flush()
    return popup_request


def _render_block(
    device: Device,
    block: UiParameterBlock,
    on_change: Callable[[Device, str, str], None],
    deferred_enum: bool,
    prefix: str,
    needle: str = "",
    differing_refs: frozenset[str] = frozenset(),
) -> EnumPopupRequest | None:
    block_prefix = f"{prefix}_{block.id}"

    if block.layout in (ParameterBlockLayout.GRID, ParameterBlockLayout.TABLE):
        return _render_grid_block(
            device, block, on_change, deferred_enum, block_prefix, differing_refs
        )

    if block.inline:
        return _render_children(
            device,
            block.children,
            on_change,
            deferred_enum,
            block_prefix,
            needle,
            differing_refs,
        )

    label = block.text or block.name or block.id
    param_count = count_parameters(block.children)
    popup_request: EnumPopupRequest | None = None
    if needle:  # while filtering, expand matching blocks so hits are visible
        imgui.set_next_item_open(True, imgui.Cond_.always)
    is_open = imgui.tree_node(f"{label}##{block_prefix}")
    imgui.same_line()
    imgui.text_disabled(f"({param_count})")
    if is_open:
        req = _render_children(
            device,
            block.children,
            on_change,
            deferred_enum,
            block_prefix,
            needle,
            differing_refs,
        )
        if req is not None:
            popup_request = req
        imgui.tree_pop()
    return popup_request


def _render_grid_block(
    device: Device,
    block: UiParameterBlock,
    on_change: Callable[[Device, str, str], None],
    deferred_enum: bool,
    prefix: str,
    differing_refs: frozenset[str] = frozenset(),
) -> EnumPopupRequest | None:
    """Render a GRID/TABLE block: UiParameter.cell holds the "row,col" position."""
    popup_request: EnumPopupRequest | None = None
    cells_by_pos: dict[tuple[int, int], UiParameter] = {}
    labels_by_pos: dict[tuple[int, int], str] = {}
    uncelled: list[UiParameter] = []

    for node in block.children:
        if isinstance(node, UiParameter):
            if node.cell:
                try:
                    r, c = node.cell.split(",")
                    cells_by_pos[(int(r), int(c))] = node
                    continue
                except ValueError:
                    pass
            uncelled.append(node)
        elif isinstance(node, UiSeparator) and node.cell and node.text:
            try:
                r, c = node.cell.split(",")
                labels_by_pos[(int(r), int(c))] = node.text
            except ValueError:
                pass

    if not cells_by_pos and not labels_by_pos:
        return _render_param_table(
            device, uncelled, on_change, deferred_enum, prefix, differing_refs
        )

    all_rows = {r for r, _ in cells_by_pos} | {r for r, _ in labels_by_pos}
    all_cols = {c for _, c in cells_by_pos} | {c for _, c in labels_by_pos}
    max_row = max(all_rows, default=1)
    max_col = max(all_cols, default=1)

    is_table = block.layout == ParameterBlockLayout.TABLE
    table_flags = (
        imgui.TableFlags_.no_saved_settings | imgui.TableFlags_.sizing_stretch_prop
    )
    if is_table:
        table_flags |= imgui.TableFlags_.borders | imgui.TableFlags_.row_bg

    has_row_labels = bool(block.row_labels)
    has_col_headers = bool(block.column_headers)
    col_offset = 1 if has_row_labels else 0
    declared_cols = max(max_col, len(block.column_headers))
    total_cols = declared_cols + col_offset

    if imgui.begin_table(f"##grid_{prefix}", total_cols, table_flags):
        if is_table and (has_row_labels or has_col_headers):
            if has_row_labels:
                imgui.table_setup_column(block.text or block.name or "")
            for header in block.column_headers:
                imgui.table_setup_column(header)
            for _ in range(declared_cols - len(block.column_headers)):
                imgui.table_setup_column("")
            imgui.table_headers_row()
        elif is_table:
            imgui.table_headers_row()
        for row in range(1, max_row + 1):
            imgui.table_next_row()
            if has_row_labels:
                imgui.table_set_column_index(0)
                label = (
                    block.row_labels[row - 1] if row - 1 < len(block.row_labels) else ""
                )
                imgui.text_disabled(label)
            for col in range(1, max_col + 1):
                imgui.table_set_column_index(col - 1 + col_offset)
                param = cells_by_pos.get((row, col))
                label = labels_by_pos.get((row, col))
                if param is not None:
                    imgui.set_next_item_width(-1)
                    widget_id = f"{device.node_id}_{param.ref_id}"
                    # GRID/TABLE cells carry no label to tint, so mark a changed value by tinting
                    # the widget's own text (combo preview / input), matching the table view.
                    changed = param.value != param.default_value
                    if changed:
                        imgui.push_style_color(imgui.Col_.text, _CHANGED_COLOR)
                    req = render_param_widget(
                        param,
                        widget_id,
                        lambda v, d=device, p=param.ref_id: on_change(d, p, v),
                        deferred_enum=deferred_enum,
                        differs=param.ref_id in differing_refs,
                    )
                    if changed:
                        imgui.pop_style_color()
                        if imgui.begin_popup_context_item(f"##reset_{widget_id}"):
                            if imgui.menu_item(S.PARAM_RESET_DEFAULT, "", False)[0]:
                                on_change(device, param.ref_id, param.default_value)
                            imgui.end_popup()
                    if req is not None:
                        popup_request = EnumPopupRequest(device=device, param=req.param)
                elif label is not None:
                    imgui.text_disabled(label)
        imgui.end_table()

    if uncelled:
        req = _render_param_table(
            device, uncelled, on_change, deferred_enum, prefix, differing_refs
        )
        if req is not None:
            popup_request = req

    return popup_request


def _render_param_table(
    device: Device,
    params: list[UiParameter],
    on_change: Callable[[Device, str, str], None],
    deferred_enum: bool,
    prefix: str,
    differing_refs: frozenset[str] = frozenset(),
) -> EnumPopupRequest | None:
    if not params:
        return None
    popup_request: EnumPopupRequest | None = None
    table_flags = (
        imgui.TableFlags_.no_saved_settings | imgui.TableFlags_.sizing_stretch_prop
    )
    if imgui.begin_table(f"##params_{prefix}", 2, table_flags):
        # Split label/value proportionally so wide combos (long enum labels) get real room
        # instead of being clipped in a narrow fixed column with a big gap to the left.
        imgui.table_setup_column("Name", imgui.TableColumnFlags_.width_stretch, 1.0)
        imgui.table_setup_column("Value", imgui.TableColumnFlags_.width_stretch, 1.0)
        for param in params:
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            indent = param.indent_level * 12.0
            if indent > 0:
                imgui.indent(indent)
            label = param.label + (f"  {param.suffix}" if param.suffix else "")
            differs = param.ref_id in differing_refs
            # In multi-edit a diverging value has no single "changed vs default" state to show.
            changed = not differs and param.value != param.default_value
            # ETS-style: changed parameters stand out. A leading marker plus the colour means the
            # state is not signalled by colour alone.
            if changed:
                imgui.text_colored(_CHANGED_COLOR, "*")
                imgui.same_line(0, 4)
                imgui.text_colored(_CHANGED_COLOR, label)
                if imgui.is_item_hovered():
                    imgui.set_tooltip(
                        S.PARAM_CHANGED_TOOLTIP.format(default=_default_display(param))
                    )
            else:
                imgui.text(label)
            if indent > 0:
                imgui.unindent(indent)
            imgui.table_set_column_index(1)
            imgui.set_next_item_width(-1)
            widget_id = f"{device.node_id}_{param.ref_id}"
            req = render_param_widget(
                param,
                widget_id,
                lambda v, d=device, p=param.ref_id: on_change(d, p, v),
                deferred_enum=deferred_enum,
                differs=differs,
            )
            # Right-click a changed value to restore the application default.
            if changed and imgui.begin_popup_context_item(f"##reset_{widget_id}"):
                if imgui.menu_item(S.PARAM_RESET_DEFAULT, "", False)[0]:
                    on_change(device, param.ref_id, param.default_value)
                imgui.end_popup()
            if req is not None:
                popup_request = EnumPopupRequest(device=device, param=req.param)
        imgui.end_table()
    return popup_request


def _render_separator(sep: UiSeparator) -> None:
    if sep.text:
        imgui.separator_text(sep.text)
    else:
        imgui.spacing()


class EnumPopup:
    def __init__(
        self,
        popup_id: str,
        on_change: Callable[[Device, str, str], None],
    ) -> None:
        self._popup_id = popup_id
        self._on_change = on_change
        self._request: EnumPopupRequest | None = None
        self._active: EnumPopupRequest | None = None

    def request(self, device: Device, param: UiParameter) -> None:
        self._request = EnumPopupRequest(device=device, param=param)

    def render(self) -> None:
        if self._request is not None:
            self._active = self._request
            self._request = None
            imgui.open_popup(self._popup_id)

        if imgui.begin_popup(self._popup_id):
            target = self._active
            if target is not None and isinstance(target.param.widget, EnumWidget):
                for choice in target.param.widget.choices:
                    selected = str(choice.value) == target.param.value
                    if imgui.menu_item(choice.label, "", selected)[0]:
                        self._on_change(
                            target.device, target.param.ref_id, str(choice.value)
                        )
            imgui.end_popup()
        else:
            self._active = None
