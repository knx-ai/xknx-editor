from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticScript:
    class Meta:
        global_type = False

    value: str = field(default="")
