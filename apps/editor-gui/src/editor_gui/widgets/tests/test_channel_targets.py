"""channel_apply_targets: map an edited parameter to the same parameter in every other repeated
channel (for the "apply to all channels" toggle), positionally within structurally-identical blocks."""

from __future__ import annotations

from editor_gui.widgets import channel_apply_targets
from xknxeditor.prod.parser_v2.ui import UiParameterBlock, UiTab
from xknxeditor.prod.parser_v2.ui.parameter import (
    CheckBoxWidget,
    TextWidget,
    UiParameter,
)


def _p(ref_id: str, label: str, widget=None) -> UiParameter:
    return UiParameter(
        ref_id=ref_id, label=label, value="", widget=widget or TextWidget()
    )


def _channel(n: int) -> UiParameterBlock:
    # Same structure/labels every channel; only ref_ids and the block title differ.
    return UiParameterBlock(
        id=f"PB-{n}",
        name=f"PM {n}",
        text=f"PM {n}: ...",
        children=(
            _p(f"R-{n}-desc", "Beschreibung"),
            _p(f"R-{n}-delay", "Startverzögerung"),
            _p(f"R-{n}-active", "Kanalaktivität", CheckBoxWidget()),
        ),
    )


def _tree() -> list:
    return [
        UiTab(
            id="t",
            name="PM",
            text="Präsenzmelder",
            children=(
                UiParameterBlock(  # a non-repeated block -> never a channel target
                    id="PB-gen",
                    name="Allgemein",
                    text="Allgemein",
                    children=(_p("R-gen-x", "Etwas"),),
                ),
                _channel(1),
                _channel(2),
                _channel(3),
            ),
        )
    ]


def test_maps_to_same_param_in_other_channels():
    targets = channel_apply_targets(_tree(), "R-1-delay")
    assert targets == ["R-2-delay", "R-3-delay"]  # same position in PM2/PM3


def test_first_and_last_param_map():
    assert channel_apply_targets(_tree(), "R-2-desc") == ["R-1-desc", "R-3-desc"]
    assert channel_apply_targets(_tree(), "R-3-active") == ["R-1-active", "R-2-active"]


def test_non_repeated_block_has_no_targets():
    assert channel_apply_targets(_tree(), "R-gen-x") == []


def test_unknown_ref_is_empty():
    assert channel_apply_targets(_tree(), "R-nope") == []
