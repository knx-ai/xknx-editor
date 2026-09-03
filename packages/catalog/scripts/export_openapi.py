"""Export the OpenAPI spec to a JSON file without starting the server."""

import json
import sys
from pathlib import Path

_DEFAULT_OUT = Path(__file__).resolve().parents[4] / "openapi.json"


def main():
    from xknxmono.catalog.http.app import app

    out = Path(sys.argv[1]) if len(sys.argv) > 1 else _DEFAULT_OUT
    spec = app.openapi()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(spec, indent=2))
    print(f"Wrote OpenAPI spec to {out}")
