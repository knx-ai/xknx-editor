"""Tests for download image assembly."""

from __future__ import annotations

from pathlib import Path

import pytest

from xknxeditor.download.errors import ImageError
from xknxeditor.download.image import DownloadImage, MemorySegment, build_image
from xknxeditor.prod import load

_FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "prod"
    / "tests"
    / "fixtures"
    / "gira_2gang_button_interface.knxprod"
)


def test_read_within_segment() -> None:
    image = DownloadImage(
        segments=(MemorySegment(address=0x100, data=bytes(range(16))),),
        properties=(),
    )
    assert image.read(0x104, 4) == bytes([4, 5, 6, 7])


def test_read_outside_segment_raises() -> None:
    image = DownloadImage(
        segments=(MemorySegment(address=0x100, data=bytes(4)),),
        properties=(),
    )
    with pytest.raises(ImageError, match="no image data"):
        image.read(0x100, 8)


def test_memory_segment_end() -> None:
    assert MemorySegment(address=0x100, data=bytes(4)).end == 0x104


def test_build_image_from_project_device() -> None:
    from types import SimpleNamespace
    from typing import cast

    from xknxeditor.download.project_data import SeedDevice

    registry = load(_FIXTURE)
    applications = [
        app for app in registry.applications.values() if app.dynamic_ui() is not None
    ]
    assert applications
    application = applications[0]

    # A device with no configured parameters/modules must yield the same image
    # as the plain default build (seeding with empty project data is a no-op).
    device = cast(
        "SeedDevice",
        SimpleNamespace(parameters=[], module_instances=[], com_objects=[]),
    )
    seeded = build_image(application, device=device)
    default = build_image(application)

    assert isinstance(seeded, DownloadImage)
    assert {s.address for s in seeded.segments} == {s.address for s in default.segments}


def test_build_image_from_fixture() -> None:
    registry = load(_FIXTURE)
    applications = [
        app for app in registry.applications.values() if app.dynamic_ui() is not None
    ]
    assert applications, "fixture should contain at least one application"

    image = build_image(applications[0])

    assert isinstance(image, DownloadImage)
    # every assembled segment carries data at a concrete address
    for segment in image.segments:
        assert segment.data
        assert segment.address >= 0
