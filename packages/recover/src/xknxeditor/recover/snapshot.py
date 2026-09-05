"""Forensic snapshots of recovered devices.

Turns the raw and decoded data read off a device into a JSON-serialisable record:
the mask version, application id, descriptive dossier, decoded group communication,
recovered parameters, and the raw code-segment bytes (hex). This is a faithful,
loss-free capture for archiving, diffing or debugging, independent of whether the
data was mapped into a project.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .recover import RecoveredDevice


def device_snapshot(device: RecoveredDevice) -> dict[str, Any]:
    """A JSON-serialisable snapshot of one recovered device."""
    return {
        "address": device.address,
        "mask_version": f"{device.mask_version:#06x}",
        "application_id": device.application_id,
        "device_address": device.device_address,
        "dossier": asdict(device.dossier),
        "group_addresses": device.group_addresses,
        "links": [
            {
                "group_address": link.group_address,
                "group_object_number": link.group_object_number,
                "sending": link.sending,
            }
            for link in device.links
        ],
        "group_objects": {
            str(number): asdict(group_object)
            for number, group_object in device.group_objects.items()
        },
        "parameters": {
            "values": device.parameters.values,
            "unknown": device.parameters.unknown,
        },
        "raw_segments": {
            segment_id: data.hex()
            for segment_id, data in (device.parameter_segments or {}).items()
        },
    }


def snapshots_json(devices: Sequence[RecoveredDevice]) -> str:
    """Serialise recovered devices to a pretty-printed JSON snapshot document."""
    return json.dumps(
        {"devices": [device_snapshot(device) for device in devices]},
        indent=2,
        ensure_ascii=False,
    )
