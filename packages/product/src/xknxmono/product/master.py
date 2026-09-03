"""The global `MasterData` (datapoint types, manufacturers, medium types…).

`parse_master_xml` builds it from a master XML in isolation. Holds the raw IR on `.raw`;
convenience id→name maps are added as consumers need them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from xknxmono.models import detect_version

from .data import to_ir

if TYPE_CHECKING:
    from xknxmono.models import intermediate as ir


@dataclass(slots=True)
class MasterData:
    raw: ir.MasterData | None
    _medium_types: dict[str, str] | None = field(default=None, repr=False)
    _manufacturers: dict[str, str] | None = field(default=None, repr=False)

    @property
    def medium_types(self) -> dict[str, str]:
        """id → display name for every medium type."""
        if self._medium_types is None:
            holder = self.raw.medium_types if self.raw is not None else None
            self._medium_types = (
                {m.id: (m.name or m.text or m.id) for m in holder.medium_type if m.id}
                if holder is not None
                else {}
            )
        return self._medium_types

    @property
    def manufacturers(self) -> dict[str, str]:
        """id → display name for every manufacturer."""
        if self._manufacturers is None:
            holder = self.raw.manufacturers if self.raw is not None else None
            self._manufacturers = (
                {m.id: (m.name or m.id) for m in holder.manufacturer if m.id}
                if holder is not None
                else {}
            )
        return self._manufacturers


def parse_master_xml(xml_bytes: bytes) -> MasterData:
    """Parse a master XML into `MasterData`."""
    knx = to_ir(xml_bytes, detect_version(xml_bytes))
    return MasterData(raw=knx.master_data)
