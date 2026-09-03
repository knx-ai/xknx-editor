"""Parse and compare KNX application-program ids.

An application-program id has the form ``M-<mfr>_A-<appnum>-<version>-<hash>``
(e.g. ``M-0083_A-0040-25-F9E1``), where ``<mfr>``, ``<appnum>`` and ``<version>``
are hex. It is the id ETS assigns to a specific version of an application program;
two versions of the same application share manufacturer + application number and
differ in the version segment (and hash).

This module is the string counterpart to :mod:`xknxmono.recover.identify`, which
parses the same fields out of the ``PID_PROGRAM_VERSION`` bytes read from a device.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# M-<mfr>_A-<appnum>-<version>-<hash>; mfr/appnum/version/hash are hex.
_APP_ID_RE = re.compile(
    r"^(M-[0-9A-F]{4})_A-([0-9A-F]+)-([0-9A-F]+)-([0-9A-F]+)$", re.IGNORECASE
)


@dataclass(frozen=True, slots=True)
class ParsedAppId:
    """The parsed fields of an application-program id."""

    manufacturer_id: str  # "M-0083"
    application_number: int
    version: int
    hash: str  # trailing hex segment, e.g. "F9E1"

    def same_application(self, other: ParsedAppId) -> bool:
        """Whether ``other`` is a different version of the *same* application."""
        return (
            self.manufacturer_id == other.manufacturer_id
            and self.application_number == other.application_number
        )


def parse_app_id(app_id: str) -> ParsedAppId | None:
    """Parse an application-program id string, or ``None`` if it is not one.

    The manufacturer id is normalised to upper-case hex (``M-0083``) so that ids
    differing only in hex casing compare equal.
    """
    match = _APP_ID_RE.match(app_id.strip())
    if match is None:
        return None
    mfr, appnum, version, hash_ = match.groups()
    return ParsedAppId(
        manufacturer_id=mfr.upper(),
        application_number=int(appnum, 16),
        version=int(version, 16),
        hash=hash_.upper(),
    )
