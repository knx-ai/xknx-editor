"""Tests for the synthesized System B group communication load procedure."""

from __future__ import annotations

from xknxmono.download.group_communication import (
    synthesize_group_communication_controls,
)
from xknxmono.download.image import DownloadImage, RelativeSegment
from xknxmono.models.intermediate.ld_ctrl_rel_segment_t import LdCtrlRelSegment
from xknxmono.models.intermediate.ld_ctrl_write_rel_mem_t import LdCtrlWriteRelMem


def _image(*relative: RelativeSegment) -> DownloadImage:
    return DownloadImage(segments=(), properties=(), relative_segments=relative)


def test_no_relative_segments_yields_no_controls() -> None:
    assert synthesize_group_communication_controls(_image()) == []


def test_controls_ordered_address_association_group_object() -> None:
    image = _image(
        RelativeSegment(9, b"\x00\xc8", b"\xff\xff"),
        RelativeSegment(1, b"\x00\x02", b"\xff\xff"),
        RelativeSegment(2, b"\x00\x01", b"\xff\xff"),
    )
    controls = synthesize_group_communication_controls(image)
    # three controls per table (two allocations then a write), in table order
    object_types = [
        c.obj_type
        for c in controls
        if isinstance(c, (LdCtrlRelSegment, LdCtrlWriteRelMem))
    ]
    assert object_types == [1, 1, 1, 2, 2, 2, 9, 9, 9]


def test_write_control_carries_full_table_size_at_offset_zero() -> None:
    image = _image(RelativeSegment(1, b"\x00\x02\x0b\x08", b"\xff\xff\xff\xff"))
    writes = [
        c
        for c in synthesize_group_communication_controls(image)
        if isinstance(c, LdCtrlWriteRelMem)
    ]
    assert len(writes) == 1
    assert writes[0].obj_type == 1
    assert writes[0].offset == 0
    assert writes[0].size == 4
    assert writes[0].inline_data is None


def test_allocations_mirror_two_mode_pattern() -> None:
    image = _image(RelativeSegment(1, b"\x00\x00", b"\xff\xff"))
    allocations = [
        c
        for c in synthesize_group_communication_controls(image)
        if isinstance(c, LdCtrlRelSegment)
    ]
    assert [a.mode for a in allocations] == [1, 0]
    assert all(a.size == 2 for a in allocations)
