"""SQLite engine factory and storage-path helpers for the catalog."""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine, event  # noqa: E402
from sqlalchemy.engine import Engine  # noqa: E402
from sqlalchemy.exc import OperationalError  # noqa: E402

from xknxeditor.catalog.models import Base  # noqa: E402

_PACKAGE_DIR = Path(__file__).parents[3]


def default_db_url() -> str:
    """Return the DB URL from ``DATABASE_URL`` or fall back to ``data/catalog.db``."""
    fallback = _PACKAGE_DIR / "data" / "catalog.db"
    return os.getenv("DATABASE_URL", f"sqlite:///{fallback}")


def knxprod_dir_for(db_path: Path) -> Path:
    """Sibling ``knxprod/`` directory for uploaded archives, created on demand."""
    dest = db_path.parent / "knxprod"
    dest.mkdir(parents=True, exist_ok=True)
    return dest


def make_engine(url: str) -> Engine:
    """Build a SQLAlchemy engine with SQLite pragmas and auto-schema. Caller owns the engine."""
    engine = create_engine(url, connect_args={"check_same_thread": False})

    @event.listens_for(engine, "connect")
    def set_pragmas(dbapi_conn: Any, _: Any) -> None:  # pyright: ignore[reportUnusedFunction]
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=DELETE")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # create_all(checkfirst=True) normally skips existing tables, but on a database left in an
    # inconsistent state by a previous hard crash (the table exists yet the has_table probe misses
    # it — observed on Windows via x64 emulation) it still emits CREATE TABLE and fails with
    # "table ... already exists". The schema is genuinely present, so treat that as a no-op: the
    # catalog is a rebuildable cache and reusing the existing tables is correct and idempotent.
    try:
        Base.metadata.create_all(engine)
    except OperationalError as exc:
        if "already exists" not in str(exc.orig):
            raise
    return engine
