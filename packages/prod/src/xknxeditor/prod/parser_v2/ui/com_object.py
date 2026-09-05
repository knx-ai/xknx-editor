from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UiComObject:
    ref_id: str  # ComObjectRef ID, instance-qualified
    name: str  # display name; {{0}} from text_parameter_ref_id
    function_text: (
        str  # object function (e.g. "Switch"), distinguishes same-channel objects
    )
    number: int
    dpt_codes: tuple[str, ...]  # e.g. "1.0", "1.1"
    object_size: (
        str  # resolved ComObjectSize value, e.g. "1 Bit" / "1 Byte" ("" if unset)
    )
    priority: str  # resolved ComObjectPriority value, e.g. "Low" ("" if unset)
    communication: bool
    read: bool
    write: bool
    transmit: bool
    update: bool
    read_on_init: bool
    # Locked flags: from base ComObject, manufacturer-fixed and read-only
    read_locked: bool
    write_locked: bool
    transmit_locked: bool
    update_locked: bool
    read_on_init_locked: bool
