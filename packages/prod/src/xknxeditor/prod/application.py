"""Per-program facade that resolves one IR application program on demand.

The raw `intermediate.ApplicationProgram` sits on `.program`; the methods surface the derived
views: code, load procedures, dynamic UI.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

from xknxeditor.namespaces import detect_version

if TYPE_CHECKING:
    from pathlib import Path

    from xknxeditor.namespaces.intermediate.application_program_static_t_code import (
        ApplicationProgramStaticCode,
    )
    from xknxeditor.namespaces.intermediate.application_program_t import (
        ApplicationProgram,
    )
    from xknxeditor.namespaces.intermediate.knx import Knx
    from xknxeditor.namespaces.intermediate.load_procedure_style_t import (
        LoadProcedureStyle,
    )
    from xknxeditor.namespaces.intermediate.load_procedures_t import LoadProcedures

    from .parser_v2.dynamic import DynamicUI


@dataclass(slots=True)
class Application:
    """A lazily resolved application program: `.program` is raw IR, methods yield computed types."""

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
        """Build a new caller-owned DynamicUI (with its own GlobalState), or None if no dynamic section."""
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
    """Parse one application XML on its own (no hardware/catalog context).

    With ``language`` (e.g. "de-DE" or "de") the .knxprod translations are overlaid for localized
    labels. ``cache_dir`` turns on a content-addressed disk cache for the parse (see :mod:`parse_cache`)."""
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
