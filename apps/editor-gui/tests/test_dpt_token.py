from editor_gui.dpt import DPT_UNKNOWN, lookup_or_make_dpt


def test_main_only_code_yields_main_token() -> None:
    dpt = lookup_or_make_dpt("16")
    assert dpt.major == 16
    assert dpt.has_subtype is False
    assert dpt.token == "DPT-16"


def test_zero_subtype_is_kept_distinct() -> None:
    dpt = lookup_or_make_dpt("16.0")
    assert dpt.major == 16
    assert dpt.minor == 0
    assert dpt.has_subtype is True
    assert dpt.token == "DPST-16-0"


def test_regular_subtype_token() -> None:
    assert lookup_or_make_dpt("1.1").token == "DPST-1-1"


def test_unknown_has_no_token() -> None:
    assert DPT_UNKNOWN.token is None
    assert lookup_or_make_dpt("nonsense").token is None
    assert lookup_or_make_dpt("").token is None
