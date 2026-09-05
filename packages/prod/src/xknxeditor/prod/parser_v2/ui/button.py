from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UiButton:
    id: str
    text: str
