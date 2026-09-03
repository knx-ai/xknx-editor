"""Generate or update the catalog database from knxprod files."""

import sys
from pathlib import Path

from xknxmono.catalog import CatalogService


def generate_catalog(catalog_path: Path, knxprod_paths: list[Path]) -> None:
    print(f"Opening catalog: {catalog_path}")
    catalog = CatalogService(catalog_path)

    total_added = 0
    for knxprod_path in knxprod_paths:
        if not knxprod_path.exists():
            print(f"  Skipping (not found): {knxprod_path}")
            continue

        print(f"  Loading: {knxprod_path.name}")
        before = {a.application_id for a in catalog.list_applications()}
        try:
            catalog.import_knxprod(knxprod_path.read_bytes())
        except Exception as e:
            print(f"    Error: {e}")
            continue
        added = sorted({a.application_id for a in catalog.list_applications()} - before)
        if added:
            print(f"    Added {len(added)} application(s)")
            for app_id in added:
                print(f"      - {app_id}")
            total_added += len(added)
        else:
            print("    No new applications (already in catalog)")

    print(f"\nCatalog updated: {total_added} application(s) added")
    print(f"Saved to: {catalog_path}")


def main() -> None:
    from editor_gui.settings import config_dir

    catalog_path = config_dir() / "catalog.xknxcatalog"
    catalog_path.parent.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) > 1:
        knxprod_paths = [Path(p) for p in sys.argv[1:]]
    else:
        internal_knxprod = (
            Path(__file__).parent.parent.parent.parent / "internal" / "knxprod"
        )
        if internal_knxprod.exists():
            knxprod_paths = list(internal_knxprod.glob("*.knxprod"))
            print(f"Loading from: {internal_knxprod}")
        else:
            knxprod_paths = []
            print("No knxprod files specified and internal/knxprod not found")
            print("Usage: generate-catalog [knxprod_file ...]")
            return

    generate_catalog(catalog_path, knxprod_paths)


if __name__ == "__main__":
    main()
