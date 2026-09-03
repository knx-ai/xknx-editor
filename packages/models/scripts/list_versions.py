"""Show per-version file additions/removals across the generated `files.vXX` models.

Run:  uv run python packages/models/scripts/list_versions.py
"""

from pathlib import Path

FILES = Path(__file__).parent.parent / "src" / "xknxmono" / "models" / "files"


def get_files(version: str) -> set[str]:
    return {p.stem for p in (FILES / version).glob("*.py") if p.name != "__init__.py"}


def main() -> None:
    versions = sorted(
        d.name for d in FILES.iterdir() if d.is_dir() and d.name.startswith("v")
    )

    prev: set[str] = set()
    for version in versions:
        files = get_files(version)
        added = files - prev
        removed = prev - files
        print(f"\n{version}  ({len(files)} files)")
        for name in sorted(added):
            print(f"  + {name}")
        for name in sorted(removed):
            print(f"  - {name}")
        if not added and not removed:
            print("  (no changes)")
        prev = files


if __name__ == "__main__":
    main()
