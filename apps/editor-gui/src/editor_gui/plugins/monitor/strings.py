"""Group monitor plugin strings."""

from pathlib import Path

from editor_gui.strings import create_translator

_locale_dir = Path(__file__).parent / "locales"
_ = create_translator("monitor", _locale_dir)


class MonitorStrings:
    @property
    def PANEL_MONITOR(self) -> str:
        return _("Group Monitor")

    @property
    def MONITOR_NO_GAS(self) -> str:
        return _("No group addresses (open or import a project)")

    @property
    def MONITOR_DISCONNECTED(self) -> str:
        return _("Not connected")

    @property
    def MONITOR_VALUE_HINT(self) -> str:
        return _("value (e.g. on / 21.5 / 50)")

    @property
    def MONITOR_VALUE_LABEL(self) -> str:
        return _("Value:")

    @property
    def MONITOR_FILTER_HINT(self) -> str:
        return _("Filter by address or name…")

    @property
    def MONITOR_WRITE(self) -> str:
        return _("Write")

    @property
    def MONITOR_READ(self) -> str:
        return _("Read")

    @property
    def MONITOR_TAB_GROUP_OBJECTS(self) -> str:
        return _("Group Objects")

    @property
    def MONITOR_TAB_BUS(self) -> str:
        return _("Bus Monitor")

    @property
    def MONITOR_CLEAR(self) -> str:
        return _("Clear")

    @property
    def MONITOR_TELEGRAM_COUNT(self) -> str:
        return _("{count} telegrams")

    @property
    def MONITOR_BUS_LOAD(self) -> str:
        return _("Bus load: {rate} telegrams/s")


S = MonitorStrings()
