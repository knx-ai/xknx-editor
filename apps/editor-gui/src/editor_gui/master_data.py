"""The global KNX ``MasterData`` (mask-version load/unload procedures, manufacturers, DPTs).

A download resolves an application's Load/Unload procedure against the mask version's
default in the master data (see :mod:`xknxmono.download.merge`). ETS ships the same
``knx_master.xml`` into every ``.knxprod``; we bundle a copy under ``assets/`` so the
editor has it offline from the first launch.

This module loads it once and reports its version and date for display. A
conditional-GET refresh from update.knx.org can be added later; it must not write into
the cwd-relative ``config/`` directory.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from xknxmono.product import MasterData, parse_master_xml

_BUNDLED = Path(__file__).parent / "assets" / "knx_master.xml"
# ``Last-Modified`` of the bundled ``knx_master.xml`` (version 285) at bundle time.
_BUNDLED_DATE = "2026-08-26"


@dataclass(frozen=True, slots=True)
class MasterDataInfo:
    """Which master data is in use, for the status bar."""

    version: int
    date: str
    source: str  # "bundled" | "updated"


def load_master() -> tuple[MasterData, MasterDataInfo]:
    """Load the bundled global master data and report its version and date."""
    master = parse_master_xml(_BUNDLED.read_bytes())
    version = master.raw.version if master.raw is not None else 0
    return master, MasterDataInfo(version=version, date=_BUNDLED_DATE, source="bundled")


def bundled_master_xml() -> bytes:
    """Raw bytes of the bundled ``knx_master.xml`` — used to wrap OpenKNX/monolithic product XML
    (which carries no ``<MasterData>``) into an importable ``.knxprod``."""
    return _BUNDLED.read_bytes()
