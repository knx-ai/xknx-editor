"""Group-address datapoint-type normalization.

ETS stores a group address' datapoint type as a token (``DPST-1-1`` for a sub-type,
``DPT-5`` for a main-only type) and rejects any other form when it opens the project.
This module turns what a user (or an agent) actually types into that token form so a
value like ``1.001`` never reaches the exported ``0.xml``.
"""

import re

_DPST = re.compile(r"^DPST-(\d+)-(\d+)$")
_DPT = re.compile(r"^DPT-(\d+)$")
_DOTTED = re.compile(r"^(\d+)\.(\d+)$")
_MAIN = re.compile(r"^(\d+)$")

# ETS parses each number part of a datapoint-type token with Convert.ToUInt32, so a
# value outside the unsigned 32-bit range overflows when it opens the project.
_UINT32_MAX = 0xFFFFFFFF


def _bounded(value: str, number: int) -> int:
    if number > _UINT32_MAX:
        raise ValueError(
            f"datapoint type {value!r} has a number out of range (max {_UINT32_MAX})"
        )
    return number


def normalize_datapoint_type(value: str | None) -> str | None:
    """Normalize a datapoint type to ETS token form.

    The canonical tokens (``DPST-1-1``, ``DPT-5``) pass through; the dotted notation
    (``1.001`` / ``1.1`` -> ``DPST-1-1``, ``5.010`` -> ``DPST-5-10``) and a bare main
    number (``1`` -> ``DPT-1``) are converted. Leading zeros are dropped but the
    sub-number is kept distinct (``5.001`` and ``5.010`` map to different tokens).

    Returns ``None`` for an empty value and raises :class:`ValueError` for anything
    that cannot be parsed or whose numbers exceed ETS' unsigned 32-bit range, so a bad
    value is rejected rather than silently stored.
    """
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    m = _DPST.match(text.upper())
    if m:
        return f"DPST-{_bounded(value, int(m.group(1)))}-{_bounded(value, int(m.group(2)))}"
    m = _DPT.match(text.upper())
    if m:
        return f"DPT-{_bounded(value, int(m.group(1)))}"
    m = _DOTTED.match(text)
    if m:
        return f"DPST-{_bounded(value, int(m.group(1)))}-{_bounded(value, int(m.group(2)))}"
    m = _MAIN.match(text)
    if m:
        return f"DPT-{_bounded(value, int(m.group(1)))}"
    raise ValueError(
        f"unrecognized datapoint type {value!r}; use e.g. DPST-1-1, DPT-5 or 1.001"
    )
