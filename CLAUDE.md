# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                             # Install dependencies
uv run pytest                       # Run all package tests
uv run pytest packages/namespaces       # Run tests for a single package
uv run ruff check                   # Lint
uv run ruff format                  # Format
uv run pyright                      # Type check (strict mode)
```

All Python commands must use `uv run` — do not activate the venv manually.

## Architecture

UV monorepo: `packages/` holds five core libraries; `apps/` holds applications.

**Package dependency order** (bottom to top):
- `xknxeditor-namespaces` — foundation: KNX XML dataclass bindings for versions 10–14 and 20–23, plus `detect_version()`, `load_xml()`, `serialize_xml()`
- `xknxeditor-prod` — reads `.knxprod` archives (ZIP files), validates structure, parses manufacturer/catalog/hardware/application XMLs via models
- `xknxeditor-catalog` — SQLite catalog of imported `.knxprod` hardware/applications, depends on product
- `xknxeditor-proj` — project state management, depends on models
- `xknxeditor-datasecure` — parses/serializes KNX keyring XML, depends on models
- `apps/editor-gui` — project editor GUI app; consumes all packages; see `apps/editor-gui/CLAUDE.md`

**Import paths** use the `xknxeditor` namespace package (src layout):
- `from xknxeditor.namespaces import ...`
- `from xknxeditor.prod import ...`
- `from xknxeditor.catalog import ...`
- `from xknxeditor.proj import ...`
- `from xknxeditor.datasecure import ...`

**Generated code** lives under `**/files/` and `**/intermediate/` (e.g. `xknxeditor.namespaces.files`) — never edit these directly. Both are excluded from linting and type checking.

## Code Style

- Pyright strict mode; all public APIs must be fully typed
- Ruff rules: E, W, F, I, UP, B, SIM, RUF — double quotes, 2-space indent, LF line endings

## Adding a New Package

1. Create `packages/<name>/` with `pyproject.toml` (`name = "xknx-<name>"`), `src/xknxeditor/<name>/__init__.py`, `src/xknxeditor/<name>/py.typed`, and `tests/`
2. Add `"xknx-<name>"` to root `pyproject.toml` dependencies
3. Run `uv sync`
