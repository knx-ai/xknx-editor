from pathlib import Path

from editor_gui.strings import BaseStrings, create_translator

_locale_dir = Path(__file__).parent / "locales"
_ = create_translator("network", _locale_dir)


class NetworkStrings(BaseStrings):
    @property
    def PANEL_NETWORK(self) -> str:
        return _("Network")

    @property
    def TELEGRAMS_TITLE(self) -> str:
        return _("Telegrams")

    @property
    def TELEGRAMS_SELECTED(self) -> str:
        return _("({count} selected)")

    @property
    def BTN_RECORD(self) -> str:
        return _("Record")

    @property
    def BTN_RECORDING(self) -> str:
        return _("Recording")


S = NetworkStrings()
