from __future__ import annotations

from pathlib import Path

from xknxmono.keyring.files.knx_keyring import (
    Backbone,
    Devices,
    GroupAddresses,
    Interface,
    InterfaceType,
    Keyring,
)
from xknxmono.keyring.schema import load_keyring, serialize_keyring

MINIMAL_KEYRING_XML = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<Keyring xmlns="http://knx.org/xml/keyring/1"
    Project="TestProject"
    Created="2024-01-15T10:30:00"
    CreatedBy="ETS6"
    Signature="AAAAAAAAAAAAAAAAAAAAAAAAA==">
</Keyring>
"""

FULL_KEYRING_XML = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<Keyring xmlns="http://knx.org/xml/keyring/1"
    Project="FullProject"
    Created="2024-06-20T14:45:00"
    CreatedBy="ETS6"
    Signature="BBBBBBBBBBBBBBBBBBBBBBBBA==">
    <Backbone MulticastAddress="224.0.23.12" Latency="2000" Key="CCCCCCCCCCCCCCCCCCCCCCCCA=="/>
    <Interface Type="Tunneling" Host="1.1.1" IndividualAddress="1.1.2" UserID="2"
        Password="DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDQ="
        Authentication="EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEQ=">
        <Group Address="1" Senders="1.1.10 1.1.11"/>
        <Group Address="2" Senders="1.1.12"/>
    </Interface>
    <Interface Type="Backbone">
        <Group Address="100"/>
    </Interface>
    <GroupAddresses>
        <Group Address="1" Key="FFFFFFFFFFFFFFFFFFFFFFFA=="/>
        <Group Address="2" Key="GGGGGGGGGGGGGGGGGGGGGGGGA=="/>
        <Group Address="100" Key="HHHHHHHHHHHHHHHHHHHHHHHA=="/>
    </GroupAddresses>
    <Devices>
        <Device IndividualAddress="1.1.10" ToolKey="IIIIIIIIIIIIIIIIIIIIIIIA==" SequenceNumber="12345"/>
        <Device IndividualAddress="1.1.11" ToolKey="JJJJJJJJJJJJJJJJJJJJJJJA=="
            ManagementPassword="KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKI="
            Authentication="LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQ="/>
    </Devices>
</Keyring>
"""


class TestLoadKeyring:
    def test_load_from_bytes_minimal(self):
        keyring = load_keyring(MINIMAL_KEYRING_XML)

        assert isinstance(keyring, Keyring)
        assert keyring.project == "TestProject"
        assert keyring.created_by == "ETS6"
        assert keyring.signature == "AAAAAAAAAAAAAAAAAAAAAAAAA=="
        assert keyring.backbone is None
        assert keyring.interface == []
        assert keyring.group_addresses is None
        assert keyring.devices is None

    def test_load_from_bytes_full(self):
        keyring = load_keyring(FULL_KEYRING_XML)

        assert keyring.project == "FullProject"
        assert keyring.created_by == "ETS6"

    def test_load_backbone(self):
        keyring = load_keyring(FULL_KEYRING_XML)

        assert keyring.backbone is not None
        assert isinstance(keyring.backbone, Backbone)
        assert keyring.backbone.multicast_address == "224.0.23.12"
        assert keyring.backbone.latency == 2000
        assert keyring.backbone.key == "CCCCCCCCCCCCCCCCCCCCCCCCA=="

    def test_load_interfaces(self):
        keyring = load_keyring(FULL_KEYRING_XML)

        assert len(keyring.interface) == 2

        tunneling = keyring.interface[0]
        assert isinstance(tunneling, Interface)
        assert tunneling.type_value == InterfaceType.TUNNELING
        assert tunneling.host == "1.1.1"
        assert tunneling.individual_address == "1.1.2"
        assert tunneling.user_id == 2
        assert len(tunneling.group) == 2
        assert tunneling.group[0].address == 1
        assert tunneling.group[0].senders == ["1.1.10", "1.1.11"]

        backbone_if = keyring.interface[1]
        assert backbone_if.type_value == InterfaceType.BACKBONE
        assert len(backbone_if.group) == 1
        assert backbone_if.group[0].address == 100

    def test_load_group_addresses(self):
        keyring = load_keyring(FULL_KEYRING_XML)

        assert keyring.group_addresses is not None
        assert isinstance(keyring.group_addresses, GroupAddresses)
        assert len(keyring.group_addresses.group) == 3
        assert keyring.group_addresses.group[0].address == 1
        assert keyring.group_addresses.group[0].key == "FFFFFFFFFFFFFFFFFFFFFFFA=="

    def test_load_devices(self):
        keyring = load_keyring(FULL_KEYRING_XML)

        assert keyring.devices is not None
        assert isinstance(keyring.devices, Devices)
        assert len(keyring.devices.device) == 2

        device1 = keyring.devices.device[0]
        assert device1.individual_address == "1.1.10"
        assert device1.tool_key == "IIIIIIIIIIIIIIIIIIIIIIIA=="
        assert device1.sequence_number == 12345

        device2 = keyring.devices.device[1]
        assert device2.individual_address == "1.1.11"
        assert device2.management_password is not None
        assert device2.authentication is not None

    def test_load_from_path_string(self, tmp_path: Path):
        file_path = tmp_path / "test.knxkeys"
        file_path.write_bytes(MINIMAL_KEYRING_XML)

        keyring = load_keyring(str(file_path))

        assert keyring.project == "TestProject"

    def test_load_from_path_object(self, tmp_path: Path):
        file_path = tmp_path / "test.knxkeys"
        file_path.write_bytes(FULL_KEYRING_XML)

        keyring = load_keyring(file_path)

        assert keyring.project == "FullProject"
        assert keyring.backbone is not None


class TestRoundtrip:
    def test_roundtrip_minimal(self):
        keyring = load_keyring(MINIMAL_KEYRING_XML)
        serialized = serialize_keyring(keyring)
        keyring_restored = load_keyring(serialized)
        serialized_again = serialize_keyring(keyring_restored)

        assert serialized == serialized_again

    def test_roundtrip_full(self):
        keyring = load_keyring(FULL_KEYRING_XML)
        serialized = serialize_keyring(keyring)
        keyring_restored = load_keyring(serialized)
        serialized_again = serialize_keyring(keyring_restored)

        assert serialized == serialized_again
