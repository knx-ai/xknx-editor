"""Shared widget strings (decoupled from any single plugin)."""

from pathlib import Path

from editor_gui.strings import BaseStrings, create_translator

_locale_dir = Path(__file__).parent / "locales"
_ = create_translator("widgets", _locale_dir)


class WidgetStrings(BaseStrings):
    @property
    def NODE_IMAGE_PLACEHOLDER(self) -> str:
        return _("(image)")

    @property
    def SEARCH_HINT(self) -> str:
        return _("Search…")

    @property
    def TOOLTIP_LOCKED(self) -> str:
        return _("{name} (locked)")

    @property
    def GROUP_OBJECTS_AUTO_CREATE(self) -> str:
        return _("Create group addresses ({count})")

    @property
    def GROUP_OBJECTS_SELECT_ALL(self) -> str:
        return _("All")

    @property
    def GROUP_OBJECTS_SELECT_NONE(self) -> str:
        return _("None")

    @property
    def GROUP_OBJECTS_BATCH_TITLE(self) -> str:
        return _("Create group addresses")

    @property
    def GROUP_OBJECTS_BATCH_HINT(self) -> str:
        return _("Name template placeholders: {object}, {device}, {n}")

    @property
    def GROUP_OBJECTS_BATCH_NAME(self) -> str:
        return _("Name template")

    @property
    def GROUP_OBJECTS_BATCH_START(self) -> str:
        return _("Start address")

    @property
    def GROUP_OBJECTS_BATCH_CANCEL(self) -> str:
        return _("Cancel")

    @property
    def GA_SENDING(self) -> str:
        return _("Sending group address")

    @property
    def GA_RECEIVING(self) -> str:
        return _("Receiving group address")

    @property
    def GA_LINK_TITLE(self) -> str:
        return _("Link group address")

    @property
    def GA_CREATE_NEW(self) -> str:
        return _("New group address")

    @property
    def GA_CREATE_ADDR_HINT(self) -> str:
        return _("Address")

    @property
    def GA_CREATE_NAME_HINT(self) -> str:
        return _("Name")

    @property
    def GA_CREATE_BUTTON(self) -> str:
        return _("Create & link")

    @property
    def PARAM_CHANGED_TOOLTIP(self) -> str:
        return _("Changed from default ({default}) — right-click to reset")

    @property
    def PARAM_RESET_DEFAULT(self) -> str:
        return _("Reset to default")

    @property
    def PARAM_DIFFERS(self) -> str:
        return _("<differs>")

    @property
    def PARAM_OFF(self) -> str:
        return _("Off")

    @property
    def PARAM_ON(self) -> str:
        return _("On")


S = WidgetStrings()
