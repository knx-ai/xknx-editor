"""Engine and storage helpers for the catalog SQLite store.

There is no global engine: callers create one with :func:`make_engine` and own its lifetime (the
HTTP app keeps one on ``app.state``; an embedding GUI keeps its own). :func:`default_db_url` gives
the conventional location for the bundled CLI/server, and :func:`knxprod_dir_for` resolves where a
given database keeps its uploaded ``.knxprod`` files.
"""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine, event  # noqa: E402
from sqlalchemy.engine import Engine  # noqa: E402

from xknxmono.catalog.models import Base  # noqa: E402

_PACKAGE_DIR = Path(__file__).parents[3]


def default_db_url() -> str:
    """The conventional database URL (``DATABASE_URL`` env var, else the bundled ``data/catalog.db``)."""
    fallback = _PACKAGE_DIR / "data" / "catalog.db"
    return os.getenv("DATABASE_URL", f"sqlite:///{fallback}")


def knxprod_dir_for(db_path: Path) -> Path:
    """The directory (next to ``db_path``) where that database's uploaded ``.knxprod`` files live, created if needed."""
    dest = db_path.parent / "knxprod"
    dest.mkdir(parents=True, exist_ok=True)
    return dest


def make_engine(url: str) -> Engine:
    """Create a configured SQLAlchemy engine (SQLite pragmas + auto-created schema). The caller owns it."""
    engine = create_engine(url, connect_args={"check_same_thread": False})

    @event.listens_for(engine, "connect")
    def set_pragmas(dbapi_conn: Any, _: Any) -> None:  # pyright: ignore[reportUnusedFunction]
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=DELETE")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    return engine
