from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UiSeparator:
    id: str
    text: str | None
    cell: str | None = None
