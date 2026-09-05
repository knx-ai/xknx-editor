"""Health plugin strings."""

from pathlib import Path

from editor_gui.strings import create_translator

_locale_dir = Path(__file__).parent / "locales"
_ = create_translator("health", _locale_dir)


class HealthStrings:
    @property
    def PANEL_HEALTH(self) -> str:
        return _("Health")

    @property
    def HEALTH_EMPTY(self) -> str:
        return _("No project open")

    @property
    def HEALTH_ALL_GOOD(self) -> str:
        return _("No issues found")

    @property
    def HEALTH_SUMMARY(self) -> str:
        return _("{errors} errors, {warnings} warnings")


S = HealthStrings()
