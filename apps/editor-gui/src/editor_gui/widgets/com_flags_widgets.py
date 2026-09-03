from collections.abc import Callable

from imgui_bundle import imgui

from editor_gui.device import (
    FLAG_LABELS,
    ComObject,
    Device,
    com_object_display_name,
)
from editor_gui.widgets.strings import S


class ComFlagsTable:
    def __init__(self, set_flag: Callable[[Device, str, str, bool], None]) -> None:
        self._set_flag = set_flag

    def render(self, device: Device, com_objects: list[ComObject]) -> None:
        flags = imgui.TableFlags_.borders_inner | imgui.TableFlags_.sizing_fixed_fit
        if not imgui.begin_table(
            f"##com_objs_{device.node_id}", 2 + len(FLAG_LABELS), flags
        ):
            return

        imgui.table_setup_column("#", imgui.TableColumnFlags_.width_fixed, 32.0)
        imgui.table_setup_column("Name")
        for _attr, letter, _name in FLAG_LABELS:
            imgui.table_setup_column(letter)
        imgui.table_headers_row()

        for com_obj in com_objects:
            self._render_row(device, com_obj, f"{device.node_id}_{com_obj.id}")

        imgui.end_table()

    def _render_row(self, device: Device, com_object: ComObject, row_id: str) -> None:
        imgui.table_next_row()
        imgui.table_set_column_index(0)
        imgui.text_disabled(str(com_object.number))
        imgui.table_set_column_index(1)
        imgui.text(com_object_display_name(com_object))

        for col, (attr, _letter, full_name) in enumerate(FLAG_LABELS, start=2):
            imgui.table_set_column_index(col)
            current = getattr(com_object.flags, attr)
            locked_attr = f"{attr}_locked"
            is_locked = (
                getattr(com_object.flags, locked_attr, False)
                if attr != "communication"
                else False
            )

            if is_locked:
                imgui.begin_disabled()
            changed, new_value = imgui.checkbox(f"##{row_id}_{attr}", current)
            if changed and not is_locked:
                self._set_flag(device, com_object.id, attr, new_value)
            if is_locked:
                imgui.end_disabled()

            if imgui.is_item_hovered(imgui.HoveredFlags_.allow_when_disabled):
                tooltip = (
                    S.TOOLTIP_LOCKED.format(name=full_name) if is_locked else full_name
                )
                imgui.set_tooltip(tooltip)
