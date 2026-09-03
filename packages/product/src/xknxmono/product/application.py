"""`Application` — the resolution facade over a single IR application program.

It wraps one `intermediate.ApplicationProgram` (the IR is exposed directly as `.program`) and
resolves the per-program views consumers care about: code, load procedures, and the dynamic UI.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

from xknxmono.models import detect_version

if TYPE_CHECKING:
    from pathlib import Path

    from xknxmono.models.intermediate.application_program_static_t_code import (
        ApplicationProgramStaticCode,
    )
    from xknxmono.models.intermediate.application_program_t import ApplicationProgram
    from xknxmono.models.intermediate.knx import Knx
    from xknxmono.models.intermediate.load_procedure_style_t import LoadProcedureStyle
    from xknxmono.models.intermediate.load_procedures_t import LoadProcedures

    from .parser_v2.dynamic import DynamicUI


@dataclass(slots=True)
class Application:
    """One application program, resolved on demand. `program` is the raw IR; the methods return
    the computed value types."""

    program: ApplicationProgram
    version: str
    manufacturer_id: str

    @property
    def id(self) -> str:
        return self.program.id

    @property
    def name(self) -> str:
        return self.program.name or self.program.id

    @property
    def code(self) -> ApplicationProgramStaticCode | None:
        return self.program.static.code if self.program.static else None

    @property
    def load_procedures(self) -> LoadProcedures | None:
        return self.program.static.load_procedures if self.program.static else None

    @property
    def load_procedure_style(self) -> LoadProcedureStyle | None:
        return self.program.load_procedure_style

    def dynamic_ui(self) -> DynamicUI | None:
        """Create a fresh DynamicUI for this application. Returns None if the application has no
        dynamic section. The caller owns the returned instance and its embedded GlobalState."""
        if self.program.dynamic is None:
            return None
        from .parser_v2.dynamic import DynamicUI as _DynamicUI

        return _DynamicUI(self.program)


def _programs(knx: Knx) -> Iterator[ApplicationProgram]:
    if knx.manufacturer_data is None:
        return
    for manufacturer in knx.manufacturer_data.manufacturer:
        if manufacturer.application_programs is not None:
            yield from manufacturer.application_programs.application_program


def parse_application_xml(
    xml_bytes: bytes,
    manufacturer_id: str,
    language: str | None = None,
    cache_dir: Path | None = None,
) -> list[Application]:
    """Load a single application XML in isolation (no hardware/catalog context).

    When ``language`` is given (a KNX identifier like "de-DE" or a prefix like "de"), the .knxprod's
    translations for that language are overlaid so labels come back localized. ``cache_dir`` enables
    a content-addressed on-disk cache for the expensive XML parse (see :mod:`parse_cache`)."""
    from .parse_cache import cached_to_ir

    version = detect_version(xml_bytes)
    knx = cached_to_ir(xml_bytes, version, cache_dir)
    if language:
        from .translate import apply_translations

        apply_translations(knx, language)
    return [
        Application(program=p, version=version, manufacturer_id=manufacturer_id)
        for p in _programs(knx)
    ]
