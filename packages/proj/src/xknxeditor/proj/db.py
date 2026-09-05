"""Engine and storage helpers for a project's SQLite document.

A project *is* a file on disk. No global engine, no in-memory mode: a caller builds one via
:func:`make_engine` and owns its lifetime (:class:`ProjectService` holds one per open project).
:func:`url_for` maps a project path to its SQLAlchemy URL.

Schema changes: ``create_all`` only creates missing *tables*, never adds columns to an existing one.
So when the model gains a column, an already-saved ``.xknx`` would break on the next full-entity
query ("no such column"). :func:`_migrate` closes that gap by additively adding any mapped column
that a pre-existing table is missing (``ALTER TABLE ... ADD COLUMN`` with the column's type and
default). This handles the common additive case automatically; a non-additive change (rename, drop,
type change, data backfill) needs an explicit numbered step keyed off ``PRAGMA user_version``.
"""

import json
from pathlib import Path
from typing import Any

from sqlalchemy import JSON, create_engine, event, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.schema import Column

from xknxeditor.proj.models import Base

# Bump when adding a non-additive migration below. Additive column adds are handled generically and
# do not require a bump. Stamped into the file's ``PRAGMA user_version`` so future migrations can
# branch on the version a file was last written with.
SCHEMA_VERSION = 1


def url_for(path: Path) -> str:
    """SQLAlchemy URL for a project file at ``path``."""
    return f"sqlite:///{path}"


def _json_default(default: Any) -> str:
    """Serialize a JSON column's model default to a literal (``[]`` for ``default=list`` etc.).

    Handles a scalar default arg and a zero-arg factory (``list``/``dict``); anything unexpected
    falls back to JSON ``null``.
    """
    value: Any = None
    if default is not None:
        arg = getattr(default, "arg", None)
        if getattr(default, "is_callable", False) and callable(arg):
            # SQLAlchemy wraps a plain factory (``list``/``dict``) to take an ExecutionContext, so
            # try the zero-arg form first, then pass a dummy context.
            for call in (lambda: arg(), lambda: arg(None)):
                try:
                    value = call()
                    break
                except TypeError:
                    continue
        elif getattr(default, "is_scalar", False):
            value = arg
    try:
        return json.dumps(value)
    except (TypeError, ValueError):
        return "null"


def _column_ddl(column: Column[Any], dialect: Any) -> str:
    """``ALTER TABLE ADD COLUMN`` body for ``column`` (type + NOT NULL + DEFAULT).

    SQLite requires a literal DEFAULT when adding a NOT NULL column, so a scalar model default is
    rendered; NOT NULL columns without one fall back to a type-appropriate empty value.
    """
    type_sql = column.type.compile(dialect)
    default = column.default
    literal: str | None = None
    is_json = isinstance(column.type, JSON)
    if is_json:
        # A JSON column must default to valid JSON: '' would crash json.loads on read. Render the
        # model default (scalar value or the result of a zero-arg factory like ``list``/``dict``),
        # falling back to JSON null.
        literal = "'" + _json_default(default).replace("'", "''") + "'"
    elif default is not None and getattr(default, "is_scalar", False):
        arg: object = getattr(default, "arg", None)
        if isinstance(arg, bool):
            literal = "1" if arg else "0"
        elif isinstance(arg, (int, float)):
            literal = str(arg)
        else:
            literal = "'" + str(arg).replace("'", "''") + "'"
    parts = [f'"{column.name}"', type_sql]
    if not column.nullable:
        if literal is None:
            # NOT NULL with no scalar default: pick a safe empty value by type family.
            literal = (
                "0" if "INT" in type_sql.upper() or "BOOL" in type_sql.upper() else "''"
            )
        parts.append("NOT NULL")
    if literal is not None:
        parts.append(f"DEFAULT {literal}")
    return " ".join(parts)


def _migrate(engine: Engine) -> None:
    """Additively add any mapped column missing from a pre-existing table, then stamp the version."""
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    with engine.begin() as conn:
        for table in Base.metadata.sorted_tables:
            if table.name not in tables:
                continue  # create_all just made it fresh with every column
            have = {c["name"] for c in inspector.get_columns(table.name)}
            for column in table.columns:
                if column.name in have:
                    continue
                conn.execute(
                    text(
                        f'ALTER TABLE "{table.name}" '
                        f"ADD COLUMN {_column_ddl(column, engine.dialect)}"
                    )
                )
        conn.execute(text(f"PRAGMA user_version = {SCHEMA_VERSION}"))


def make_engine(url: str) -> Engine:
    """Build a configured SQLAlchemy engine (SQLite pragmas + schema auto-create/migrate).

    The caller owns it. Existing files are migrated additively to the current model (see module doc).
    """
    engine = create_engine(url, connect_args={"check_same_thread": False})

    @event.listens_for(engine, "connect")
    def set_pragmas(dbapi_conn: Any, _: Any) -> None:  # pyright: ignore[reportUnusedFunction]
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=DELETE")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    _migrate(engine)
    return engine
