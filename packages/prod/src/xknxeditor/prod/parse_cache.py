"""Content-addressed on-disk cache for the expensive application-XML parse (:func:`to_ir`).

``to_ir(xml_bytes, version)`` is a pure function of the raw application XML, so the cache key is the
SHA-256 of those bytes (plus the schema version). That makes the cache self-invalidating: a changed
or re-imported ``.knxprod`` has different bytes -> a different key -> a fresh parse; the same app
reused across projects hits the same entry. A ``CACHE_VERSION`` prefix and a defensive load guard
mean a Python/xsdata upgrade (or a corrupt file) simply misses and re-parses, never returns a wrong
result. Language translations are applied by the caller after parsing (cheap), so one cached IR
serves every language.
"""

from __future__ import annotations

import hashlib
import logging
import pickle
from pathlib import Path

from xknxeditor.namespaces.intermediate.knx import Knx

from .data import to_ir

logger = logging.getLogger(__name__)

# Bump when the IR shape or pickle compatibility changes, to abandon old cache entries.
CACHE_VERSION = "1"


def cached_to_ir(xml_bytes: bytes, version: str, cache_dir: Path | None) -> Knx:
    """``to_ir`` with an optional on-disk cache keyed by the XML content hash.

    With ``cache_dir=None`` this is a plain ``to_ir`` (no caching)."""
    if cache_dir is None:
        return to_ir(xml_bytes, version)
    digest = hashlib.sha256(xml_bytes).hexdigest()
    path = cache_dir / f"ir_{CACHE_VERSION}_{version}_{digest}.pkl"
    if path.exists():
        try:
            return pickle.loads(path.read_bytes())
        except (
            Exception
        ) as exc:  # corrupt / incompatible pickle -> reparse and overwrite
            logger.debug("parse cache miss (unreadable %s): %s", path.name, exc)
    knx = to_ir(xml_bytes, version)
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        path.write_bytes(pickle.dumps(knx, protocol=pickle.HIGHEST_PROTOCOL))
    except OSError as exc:  # a cache write failure must never break parsing
        logger.debug("could not write parse cache %s: %s", path.name, exc)
    return knx
