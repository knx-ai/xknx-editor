"""Errors raised while recovering a project from the bus."""

from __future__ import annotations


class RecoverError(Exception):
    """A device could not be recovered (missing application, unreadable data)."""
