"""Connection plugin strings."""

from pathlib import Path

from editor_gui.strings import create_translator

_locale_dir = Path(__file__).parent / "locales"
_ = create_translator("connection", _locale_dir)


class ConnectionStrings:
    @property
    def MENU_CONNECTION(self) -> str:
        return _("Gateway")

    @property
    def MENU_CONNECT(self) -> str:
        return _("Connect")

    @property
    def MENU_DISCONNECT(self) -> str:
        return _("Disconnect")

    @property
    def SECTION_DISCOVERED(self) -> str:
        return _("Discovered gateways")

    @property
    def SECTION_DIAGNOSTICS(self) -> str:
        return _("Diagnostics")

    @property
    def MENU_READ_PROGMODE(self) -> str:
        return _("Check for devices in programming mode")

    @property
    def NO_GATEWAYS_FOUND(self) -> str:
        return _("No gateways found")

    @property
    def SECTION_MANUAL(self) -> str:
        return _("Manual connection")

    @property
    def STATUS_CONNECTED(self) -> str:
        return _("Connected: {ip}")

    @property
    def STATUS_CONNECTED_TO(self) -> str:
        return _("Connected to {ip}")

    @property
    def STATUS_DISCONNECTED(self) -> str:
        return _("Disconnected")

    @property
    def PANEL_GATEWAY(self) -> str:
        return _("Gateway")

    @property
    def GW_CONNECTING(self) -> str:
        return _("Connecting…")

    @property
    def GW_ERROR(self) -> str:
        return _("Connection failed")

    @property
    def GW_SCAN(self) -> str:
        return _("Scan")

    @property
    def GW_SETTINGS(self) -> str:
        return _("Settings")

    @property
    def GW_ROUTING(self) -> str:
        return _("Use multicast routing (instead of tunneling)")

    @property
    def GW_IP(self) -> str:
        return _("Gateway IP")

    @property
    def GW_MULTICAST(self) -> str:
        return _("Multicast group")

    @property
    def GW_APPLY(self) -> str:
        return _("Apply")


S = ConnectionStrings()
