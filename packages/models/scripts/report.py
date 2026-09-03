"""Structural diff between each `files.vXX` model and the unified `intermediate` model.

For every dataclass shared by name (Meta.name, or class name for inner types), compare fields
by their XML name and flag the things a converter — or a manual intermediate edit — must resolve:

  REQUIRED-GAP : field is required in intermediate but absent from the version  → synth/override
                 (or relax the intermediate field to optional)
  DROPPED      : field exists in the version but not in intermediate            → data loss / merge artifact
  LIST->SCALAR : list in the version, scalar in intermediate                    → reject>1, take single
  SCALAR->LIST : scalar in the version, list in intermediate                    → wrap
  TYPE-ONLY    : present in intermediate, missing whole type in the version     → (informational)

Findings are de-duplicated across versions, so each line shows which versions exhibit it.

Run:  uv run python packages/models/scripts/report.py
"""

from __future__ import annotations

import dataclasses
import importlib
from collections import defaultdict
from dataclasses import MISSING, Field

VERSIONS = ["v10", "v11", "v12", "v13", "v14", "v20", "v21", "v22", "v23"]
INTERMEDIATE = "xknxmono.models.intermediate"


def type_map(module) -> dict[str, type]:
    """Map stable type key (Meta.name or class name) → dataclass, for all dataclasses in module."""
    out: dict[str, type] = {}
    for name in dir(module):
        obj = getattr(module, name)
        if dataclasses.is_dataclass(obj) and isinstance(obj, type):
            meta = getattr(obj, "Meta", None)
            key = getattr(meta, "name", None) if meta else None
            out[key or obj.__name__] = obj
    return out


def field_index(cls: type) -> dict[str, Field]:
    """Map XML name (metadata['name'] or python name) → field."""
    return {(f.metadata or {}).get("name", f.name): f for f in dataclasses.fields(cls)}


def is_required(f: Field) -> bool:
    return f.default is MISSING and f.default_factory is MISSING


def is_list(f: Field) -> bool:
    if f.default_factory is list:
        return True
    t = f.type if isinstance(f.type, str) else ""
    return t.strip().startswith("list[")


def main() -> None:
    inter = type_map(importlib.import_module(INTERMEDIATE))
    # finding -> set of versions; finding = (kind, type_key, field_name_or_"")
    findings: dict[tuple[str, str, str], set[str]] = defaultdict(set)

    for v in VERSIONS:
        vmod = type_map(importlib.import_module(f"xknxmono.models.files.{v}"))
        for key, vcls in vmod.items():
            icls = inter.get(key)
            if icls is None:
                findings[("MISSING-TYPE-IN-INTERMEDIATE", key, "")].add(v)
                continue
            vf, iff = field_index(vcls), field_index(icls)
            for fname, vfd in vf.items():
                ifd = iff.get(fname)
                if ifd is None:
                    findings[("DROPPED", key, fname)].add(v)
                elif is_list(vfd) and not is_list(ifd):
                    findings[("LIST->SCALAR", key, fname)].add(v)
                elif not is_list(vfd) and is_list(ifd):
                    findings[("SCALAR->LIST", key, fname)].add(v)
            for fname, ifd in iff.items():
                if fname not in vf and is_required(ifd):
                    findings[("REQUIRED-GAP", key, fname)].add(v)

    order = [
        "REQUIRED-GAP",
        "LIST->SCALAR",
        "SCALAR->LIST",
        "DROPPED",
        "MISSING-TYPE-IN-INTERMEDIATE",
    ]
    for kind in order:
        rows = sorted((t, f, vs) for (k, t, f), vs in findings.items() if k == kind)
        if not rows:
            continue
        print(f"\n=== {kind} ({len(rows)}) ===")
        for t, f, vs in rows:
            vers = ",".join(v for v in VERSIONS if v in vs)
            label = f"{t}.{f}" if f else t
            print(f"  {label:60} [{vers}]")

    total = sum(len(v) for v in findings.values())
    print(f"\nTotal findings: {len(findings)} distinct ({total} across versions)")


if __name__ == "__main__":
    main()
