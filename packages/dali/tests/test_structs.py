"""Byte-layout tests for the MDT DALI property structs (exact wire format from the DCA)."""

from xknxeditor.dali.structs import (
    Command,
    CommissionSync,
    EcgProp,
    EcgStatic,
    EcgStatus,
    ExtCommand,
    GroupDyn,
    SceneItemValue,
    decode_table,
    encode_table,
)


def test_ecg_prop_roundtrip() -> None:
    p = EcgProp(ecg_type=8, sub_type=2, group_index=5, ets_ecg_index=12)
    assert p.encode() == bytes((8, 2, 5, 12))
    assert EcgProp.decode(p.encode()) == p


def test_ecg_static_24bit_be_addr_and_le_temps() -> None:
    s = EcgStatic(
        long_address=0xAABBCC, min_value=10, min_color_temp=2700, max_color_temp=6500
    )
    raw = s.encode()
    assert len(raw) == 8
    assert raw[:3] == bytes((0xAA, 0xBB, 0xCC))  # 24-bit big-endian
    assert raw[3] == 10
    assert raw[4:6] == (2700).to_bytes(2, "little")
    assert raw[6:8] == (6500).to_bytes(2, "little")
    assert EcgStatic.decode(raw) == s


def test_ecg_status_decode() -> None:
    st = EcgStatus.decode(bytes((0x01, 0x04, 200, 100, 0)))
    assert st.alarm == 0x04 and st.dali_value == 200 and st.knx_value == 100


def test_group_dyn_le() -> None:
    raw = (123456).to_bytes(4, "little") + (42).to_bytes(2, "little")
    d = GroupDyn.decode(raw)
    assert d.run_hours == 123456 and d.run_seconds == 42


def test_commission_sync() -> None:
    assert CommissionSync(ets_index=12, group_index=5).encode() == bytes((12, 5))
    assert CommissionSync.decode(bytes((7, 16))) == CommissionSync(7, 16)


def test_command_and_ext_command() -> None:
    assert Command(24, 1, 2).encode() == bytes((24, 1, 2))
    assert Command.decode(bytes((0, 3, 4))) == Command(0, 3, 4)
    ext = ExtCommand(func=4, color=b"\x01\x02\x03\x04", target=1, index=9, members_hi=0)
    assert ext.encode() == bytes((4, 1, 2, 3, 4, 1, 9, 0))


def test_scene_item_value_layout() -> None:
    v = SceneItemValue(
        scene=3, item_index=20, level=254, color=b"\xaa\xbb\xcc\xdd", flags=2
    )
    raw = v.encode()
    assert raw == bytes((3, 20, 254, 0xAA, 0xBB, 0xCC, 0xDD, 2))
    assert SceneItemValue.decode(raw) == v


def test_table_helpers() -> None:
    table = encode_table([EcgProp(1, 0, 32, 0).encode(), EcgProp(2, 0, 5, 1).encode()])
    assert len(table) == 8
    parts = decode_table(table, 4)
    assert [EcgProp.decode(p) for p in parts] == [
        EcgProp(1, 0, 32, 0),
        EcgProp(2, 0, 5, 1),
    ]
