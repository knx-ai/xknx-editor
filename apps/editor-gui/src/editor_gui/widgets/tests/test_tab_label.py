"""_tab_label: disambiguate repeated module-instance tabs whose app text is identical (e.g. the MDT
DALI gateway's 16 group tabs all labelled "G," — only their id's ``_MI-<n>`` differs)."""

from __future__ import annotations

from editor_gui.widgets.parameter_widgets import _tab_label
from xknxeditor.prod.parser_v2.ui import UiTab


def _tab(tab_id: str, text: str) -> UiTab:
    return UiTab(children=(), id=tab_id, text=text)


def test_appends_instance_index_to_identical_labels() -> None:
    assert _tab_label(_tab("M-0083_A-0153_MD-2_M-3_MI-1_CH-1", "G,")) == "G 1"
    assert _tab_label(_tab("M-0083_A-0153_MD-2_M-3_MI-16_CH-1", "G,")) == "G 16"


def test_non_repeated_tab_unchanged() -> None:
    assert _tab_label(_tab("M-0083_A-0153_CH-0", "GENERAL")) == "GENERAL"
    assert _tab_label(_tab("M-0083_A-0153_CH-17", "ECG")) == "ECG"


def test_skips_when_label_already_has_the_number() -> None:
    # Already-substituted labels ("Channel 3") must not become "Channel 3 3".
    assert _tab_label(_tab("x_MI-3", "Channel 3")) == "Channel 3"
