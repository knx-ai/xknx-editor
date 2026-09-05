"""Cross-device sanity checks over recovered group communication.

Correlates the decoded links of every recovered device and reports group
addresses whose wiring looks incomplete or contradictory - no sending object, or
more than one - so the user can spot a partial scan or a genuine configuration
problem. No bus access; operates purely on already-recovered data.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .recover import RecoveredDevice


@dataclass(frozen=True, slots=True)
class LinkWarning:
    """One cross-device group-communication anomaly."""

    group_address: int
    kind: str  # "no_sender" | "multiple_senders"
    senders: int
    receivers: int


def validate_group_communication(
    devices: Sequence[RecoveredDevice],
) -> list[LinkWarning]:
    """Return anomalies in the recovered group links across ``devices``.

    Flags a group address that has receivers but no sending object (``no_sender``)
    and one that has more than one sending object (``multiple_senders``). Both can
    be legitimate (a status-only address, or a scan that did not cover the sending
    device), so they are warnings, not errors. A group address with a single
    sender is not reported.
    """
    senders: dict[int, int] = defaultdict(int)
    receivers: dict[int, int] = defaultdict(int)
    for device in devices:
        for link in device.links:
            if link.sending:
                senders[link.group_address] += 1
            else:
                receivers[link.group_address] += 1

    warnings: list[LinkWarning] = []
    for group_address in sorted(set(senders) | set(receivers)):
        sending = senders.get(group_address, 0)
        receiving = receivers.get(group_address, 0)
        if sending == 0 and receiving > 0:
            kind = "no_sender"
        elif sending > 1:
            kind = "multiple_senders"
        else:
            continue
        warnings.append(
            LinkWarning(
                group_address=group_address,
                kind=kind,
                senders=sending,
                receivers=receiving,
            )
        )
    return warnings
