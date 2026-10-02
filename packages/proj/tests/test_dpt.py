import pytest

from xknxeditor.proj.core.dpt import normalize_datapoint_type


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("DPST-1-1", "DPST-1-1"),
        ("dpst-1-1", "DPST-1-1"),
        ("DPT-5", "DPT-5"),
        ("dpt-5", "DPT-5"),
        ("1.001", "DPST-1-1"),
        ("1.1", "DPST-1-1"),
        ("5.001", "DPST-5-1"),
        ("5.010", "DPST-5-10"),
        ("1", "DPT-1"),
        ("  1.001  ", "DPST-1-1"),
        (None, None),
        ("", None),
        ("   ", None),
    ],
)
def test_normalize(value: str | None, expected: str | None) -> None:
    assert normalize_datapoint_type(value) == expected


def test_sub_types_stay_distinct() -> None:
    assert normalize_datapoint_type("5.001") != normalize_datapoint_type("5.010")


@pytest.mark.parametrize("value", ["garbage", "DPST-1", "x.y", "1.", ".1", "1-1"])
def test_unparseable_raises(value: str) -> None:
    with pytest.raises(ValueError):
        normalize_datapoint_type(value)


def test_uint32_boundary_passes() -> None:
    assert normalize_datapoint_type("4294967295.1") == "DPST-4294967295-1"
    assert normalize_datapoint_type("1.4294967295") == "DPST-1-4294967295"


@pytest.mark.parametrize(
    "value",
    [
        "4294967296.001",
        "1.4294967296",
        "4294967296",
        "DPST-4294967296-1",
        "DPT-4294967296",
    ],
)
def test_number_overflow_raises(value: str) -> None:
    with pytest.raises(ValueError, match="out of range"):
        normalize_datapoint_type(value)
