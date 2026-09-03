"""Synthesize the load controls that write the System B group communication tables.

For the System B model the group communication tables (address, association,
group object) are not written by the application's own Load Procedure - they are
applied by a separate step. So when the download image carries these tables as
relative segments, this module produces the load controls that write them:
mirroring the application's own relative-segment pattern (two ``RelSegment``
allocations followed by a ``WriteRelMem``), addressed by interface object type so
the partial-download scope filter treats them as group communication.

The table *data* is validated byte-exact against real hardware; the allocation
framing here is modelled on the application's parameter segment (the only
relative segment a System B application program carries) rather than extracted
extracted from a reference implementation, so a full download's allocation must be confirmed by a
read-diff (preflight) before it is trusted.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xknxmono.models.intermediate.ld_ctrl_rel_segment_t import LdCtrlRelSegment
from xknxmono.models.intermediate.ld_ctrl_write_rel_mem_t import LdCtrlWriteRelMem

if TYPE_CHECKING:
    from .image import DownloadImage

# The order in which the three tables are written (address, association, group
# object), following the group communication table order in KNX Standard 3/5/1 Resources.
_TABLE_ORDER = (1, 2, 9)


def synthesize_group_communication_controls(image: DownloadImage) -> list[object]:
    """Return the load controls that write the image's group communication tables.

    Emits nothing when the image carries no relative group communication segments
    (e.g. a memory-mapped model, or a parameters-only image). For each table, in
    address/association/group-object order, emits two ``RelSegment`` allocations
    (mode 1 then mode 0, as the application does for its parameter segment) and a
    ``WriteRelMem`` that writes the table data at relative offset 0.
    """
    controls: list[object] = []
    for object_type in _TABLE_ORDER:
        segment = image.relative_segment(object_type)
        if segment is None:
            continue
        size = len(segment.data)
        controls.append(
            LdCtrlRelSegment(
                obj_type=object_type, occurrence=0, size=size, mode=1, fill=0
            )
        )
        controls.append(
            LdCtrlRelSegment(
                obj_type=object_type, occurrence=0, size=size, mode=0, fill=0
            )
        )
        controls.append(
            LdCtrlWriteRelMem(
                obj_type=object_type,
                occurrence=0,
                offset=0,
                size=size,
                verify=False,
                inline_data=None,
            )
        )
    return controls
