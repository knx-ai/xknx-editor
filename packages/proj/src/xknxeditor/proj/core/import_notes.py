"""Import-loss notes: things ETS/xknxproject data carries that our project store cannot fully
represent, detected at import (while the raw ``0.xml`` is still readable), persisted on the
``Project`` row, and echoed back at export so the user can be reminded.

The note is deliberately machine-readable (a ``code`` + ``count`` + short ``detail``) so the GUI can
render a localized message from the code; the core layer stays i18n-free.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import cast

# Loss codes (stable identifiers the GUI maps to localized messages).
MULTIPLE_INSTALLATIONS = "multiple_installations"
UNASSIGNED_DEVICES = "unassigned_devices"
COM_OBJECT_TEXT_OVERRIDES = "com_object_text_overrides"
IP_CONFIG = "ip_config"
MULTI_SEGMENT = "multi_segment"
DROPPED_DUPLICATE_LINES = "dropped_duplicate_lines"


@dataclass(frozen=True, slots=True)
class ImportLoss:
    """One class of data lost or merged on import. ``count`` is how many items were affected;
    ``detail`` is a short specifics string (e.g. a name or address list), possibly empty."""

    code: str
    count: int
    detail: str = ""


def dumps(losses: list[ImportLoss]) -> str:
    """Serialize a note list to the JSON string stored in ``Project.import_notes``."""
    return json.dumps(
        [{"code": n.code, "count": n.count, "detail": n.detail} for n in losses]
    )


def loads(raw: str | None) -> list[ImportLoss]:
    """Parse the JSON string from ``Project.import_notes`` back into notes. Empty/invalid -> []."""
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except (ValueError, TypeError):
        return []
    if not isinstance(data, list):
        return []
    out: list[ImportLoss] = []
    for item in cast(list[object], data):
        if not isinstance(item, dict):
            continue
        entry = cast(dict[str, object], item)
        if "code" not in entry:
            continue
        count = entry.get("count", 0)
        out.append(
            ImportLoss(
                code=str(entry.get("code", "")),
                count=count if isinstance(count, int) else 0,
                detail=str(entry.get("detail", "")),
            )
        )
    return out
