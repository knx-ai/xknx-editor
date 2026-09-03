"""Convert a KNX XML to the unified IR.

The per-version `files.vXX` models are an implementation detail of parsing; once read they are
immediately converted to the `intermediate` (IR) representation, which is what the rest of the
package works with (IR-only — the per-version models are not retained).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xknxmono.models import load_xml
from xknxmono.models.adapters.convert import Context, convert

if TYPE_CHECKING:
    from xknxmono.models.intermediate.knx import Knx


def to_ir(xml_bytes: bytes, version: str) -> Knx:
    """Parse `xml_bytes` with the per-version model, then convert to the unified IR."""
    from xknxmono.models.intermediate.knx import Knx as _Knx

    model = load_xml(xml_bytes, version)
    return convert(Context(version=version), model, _Knx)
