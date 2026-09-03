"""Render the unified `intermediate` (IR) model as Mermaid class diagrams.

The IR is one big tree under KNX, so we draw its three top-level subtrees independently:
MasterData, ManufacturerData (the product side: catalog / hardware / application programs), and
Project. For each, every reachable type becomes a class box listing its attribute fields, and
containment is drawn as composition (`*--`) labelled with the XML element name and a cardinality
(`0..1` optional, `1` required, `0..*` list). Types are de-duplicated, so a type shared by several
parents appears once with multiple incoming edges.

Run:  uv run python packages/models/scripts/viz.py [out_dir]
      (writes ir_master_data.md, ir_product.md, ir_project.md; out_dir defaults to the CWD)

View the .md files on GitHub, in VS Code (Markdown preview), or paste into https://mermaid.live.
"""

from __future__ import annotations

import sys
import types as _types
import typing
from dataclasses import Field, fields, is_dataclass
from pathlib import Path
from typing import Union, get_args, get_origin

from xknxmono.models.adapters.convert import _unwrap, type_key
from xknxmono.models.intermediate.knx import Knx

ROOTS = [
    ("master_data", "MasterData"),
    ("manufacturer_data", "Product (ManufacturerData)"),
    ("project", "Project"),
]


def _classify(cls: type, f: Field) -> tuple[bool, list[type], str | None]:
    """Split a field into (is_list, contained_dataclass_types, scalar_attr_type | None).

    Element fields whose type is a dataclass — or a union of them, as xsdata emits for xs:choice —
    are containment (returned as `members`). Everything else is a scalar attribute whose rendered
    type name is returned."""
    hints = typing.get_type_hints(cls)
    is_list, base = _unwrap(hints.get(f.name, f.type))
    args = (
        [a for a in get_args(base) if a is not type(None)]
        if get_origin(base) in (Union, _types.UnionType)
        else [base]
    )
    members = [a for a in args if is_dataclass(a)]
    if f.metadata.get("type") in (None, "Element", "Elements") and members:
        return is_list, members, None
    names = [getattr(a, "__name__", "object") for a in args] or ["object"]
    name = names[0] if len(names) == 1 else "_or_".join(names)
    return is_list, [], (f"List~{name}~" if is_list else name)


def class_diagram(root_cls: type, title: str) -> str:
    blocks: list[str] = []
    rels: list[str] = []
    seen: set[str] = set()

    def walk(cls: type) -> None:
        key = type_key(cls)
        if key in seen:
            return
        seen.add(key)
        attrs: list[str] = []
        for f in fields(cls):
            is_list, members, scalar = _classify(cls, f)
            if scalar is not None:
                attrs.append(f"    +{scalar} {f.name}")
                continue
            card = "0..*" if is_list else "0..1"
            # single member -> the element's XML name; a choice -> the field name (e.g. "choice")
            label = f.metadata.get("name", f.name) if len(members) == 1 else f.name
            for m in members:
                rels.append(f'  {key} *-- "{card}" {type_key(m)} : {label}')
                walk(m)
        blocks.append(
            f"  class {key} {{\n" + "\n".join(attrs) + "\n  }"
            if attrs
            else f"  class {key}"
        )

    walk(root_cls)
    body = "\n".join([*blocks, "", *rels])
    return f"# IR — {title}\n\n{len(seen)} types.\n\n```mermaid\nclassDiagram\n{body}\n```\n"


def main() -> None:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    hints = typing.get_type_hints(Knx)
    for field_name, title in ROOTS:
        _, root_cls = _unwrap(hints[field_name])
        text = class_diagram(root_cls, title)
        slug = field_name.replace("manufacturer_data", "product")
        path = out_dir / f"ir_{slug}.md"
        path.write_text(text)
        print(f"  {title:32} -> {path}  ({text.splitlines()[2]})")


if __name__ == "__main__":
    main()
