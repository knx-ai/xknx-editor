"""Bulk-ingest .knxprod files from a directory into the catalog database."""

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from xknxmono.catalog.core.upload import upload_knxprod  # noqa: E402
from xknxmono.catalog.db import (  # noqa: E402
    default_db_url,
    knxprod_dir_for,
    make_engine,
)
from xknxmono.product.errors import ArchiveError  # noqa: E402


def main() -> None:
    url = default_db_url()
    engine = make_engine(url)
    dest_dir = knxprod_dir_for(Path(url.removeprefix("sqlite:///")))

    source_dir = sys.argv[1] if len(sys.argv) > 1 else str(dest_dir)

    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"ERROR: KNXPROD_DIR not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    files = sorted(source_path.glob("*.knxprod"))
    total = len(files)
    print(f"Found {total} .knxprod files in {source_path}")

    errors = 0
    for i, fp in enumerate(files, 1):
        if i % 100 == 0 or i == total:
            print(f"  [{i}/{total}] {fp.name}")
        try:
            upload_knxprod(fp.read_bytes(), dest_dir, engine)
        except ArchiveError as e:
            print(f"  SKIP {fp.name}: {e}", file=sys.stderr)
            errors += 1
        except Exception as e:
            print(f"  ERROR {fp.name}: {e}", file=sys.stderr)
            errors += 1

    print(f"Done. {total - errors} succeeded, {errors} failed.")
