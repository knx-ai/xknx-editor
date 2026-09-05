"""Flow tests for MdtDaliCommissioner (scan / identify / commission / write_scenes)."""

from _dali_fakes import FakeProgrammer

from xknxeditor.dali.commissioning import MdtDaliCommissioner
from xknxeditor.dali.connection import MdtDaliConnection
from xknxeditor.dali.model import (
    GROUP_MISSING,
    MAX_ECG,
    EcgAssignment,
    Scene,
    SceneValue,
)
from xknxeditor.dali.properties import DeviceCommand, PropertyType
from xknxeditor.dali.structs import EcgProp, decode_table


def _evg_prop_table(entries: dict[int, EcgProp]) -> bytes:
    default = EcgProp(0, 0, GROUP_MISSING, 0)
    return b"".join(entries.get(slot, default).encode() for slot in range(MAX_ECG))


def _setup() -> tuple[MdtDaliCommissioner, FakeProgrammer]:
    prog = FakeProgrammer()
    return MdtDaliCommissioner(MdtDaliConnection(prog, 0)), prog


async def test_scan_reports_present_ecgs() -> None:
    comm, prog = _setup()
    prog.set_read(25, bytes((4, 0, 1)))  # firmware
    prog.set_read(
        PropertyType.EVG_PROP,
        _evg_prop_table({0: EcgProp(8, 2, 5, 0), 3: EcgProp(6, 0, 16, 3)}),
    )
    prog.set_read(PropertyType.EVG_STATUS, b"\x00\x02\x00\x00\x00" * MAX_ECG)
    prog.set_read(
        PropertyType.EVG_STATIC, (b"\x00\x00\x2a" + b"\x0a\x00\x00\x00\x00") * MAX_ECG
    )
    prog.set_read(PropertyType.GROUP_DYN, b"\x00" * (6 * 16))
    prog.set_read(PropertyType.GROUP_STATUS, b"\x00" * (8 * 16))
    prog.set_read(PropertyType.GROUP_FAILURE, b"\x00" * (6 * 16))

    state = await comm.scan()
    assert state.firmware == (4, 0, 1)
    present = {e.slot: e for e in state.present_ecgs}
    assert set(present) == {0, 3}
    assert present[0].group_index == 5 and present[0].ecg_type == 8
    assert present[0].long_address == 0x2A and present[0].alarm == 0x02
    assert len(state.groups) == 16


async def test_identify_sends_expected_command_bytes() -> None:
    comm, prog = _setup()
    await comm.switch_ecg(5, on=True)
    await comm.blink_ecg(5, start=True)
    await comm.broadcast(on=False)
    cmds = [w["data"] for w in prog.writes_for(PropertyType.COMMAND)]
    assert cmds[0] == bytes((DeviceCommand.SET_ECG_VALUE, 5, 0xFF))
    assert cmds[1] == bytes((DeviceCommand.BLINK, 5 | 0x40, 0))
    assert cmds[2] == bytes((DeviceCommand.SET_ALL_ECG, 0, 0))


async def test_commission_writes_sync_table_and_verifies() -> None:
    comm, prog = _setup()
    prog.queue_read(PropertyType.COMMAND, bytes((0, 0, 0)))  # PLUGIN_SYNC done
    prog.set_read(
        PropertyType.EVG_PROP, _evg_prop_table({0: EcgProp(8, 2, 5, 0)})
    )  # verify

    ok = await comm.commission([EcgAssignment(slot=0, ets_index=0, group_index=5)])
    assert ok is True
    (sync,) = prog.writes_for(PropertyType.COMMISSION_SYNC)
    assert sync["count"] == MAX_ECG
    table = decode_table(bytes(sync["data"]), 2)  # type: ignore[arg-type]
    assert table[0] == bytes((0, 5))  # slot 0 -> ets 0, group 5
    # unspecified slots are seeded from the current EVG_PROP (here: missing -> ets 0, group 255),
    # never blindly wiped to unassigned.
    assert table[1] == bytes((0, GROUP_MISSING))
    assert bytes((DeviceCommand.PLUGIN_SYNC, 0, 0)) in [
        w["data"] for w in prog.writes_for(PropertyType.COMMAND)
    ]


async def test_new_installation_sends_command_reports_progress_and_rescans() -> None:
    comm, prog = _setup()
    # poll: running (found=2), then done; scan afterwards reads the (new) bus.
    prog.queue_read(PropertyType.COMMAND, bytes((5, 2, 0)), bytes((0, 4, 0)))
    prog.set_read(25, bytes((4, 0, 1)))
    prog.set_read(PropertyType.EVG_PROP, _evg_prop_table({0: EcgProp(8, 0, 32, 0)}))
    prog.set_read(PropertyType.EVG_STATUS, b"\x00" * (5 * MAX_ECG))
    prog.set_read(PropertyType.EVG_STATIC, b"\x00" * (8 * MAX_ECG))
    prog.set_read(PropertyType.GROUP_DYN, b"\x00" * (6 * 16))
    prog.set_read(PropertyType.GROUP_STATUS, b"\x00" * (8 * 16))
    prog.set_read(PropertyType.GROUP_FAILURE, b"\x00" * (6 * 16))

    seen: list[int] = []
    state = await comm.new_installation(
        pre_assign_group=1, interval=0.0, on_progress=lambda c: seen.append(c.param1)
    )
    (cmd,) = [w["data"] for w in prog.writes_for(PropertyType.COMMAND)]
    assert cmd == bytes((DeviceCommand.NEW_INSTALLATION, 0, 1))
    assert seen == [2]  # live found counter surfaced from the running readback
    assert len(state.present_ecgs) == 1


async def test_post_installation_command_bytes() -> None:
    comm, prog = _setup()
    prog.queue_read(PropertyType.COMMAND, bytes((0, 0, 0)))
    for pid in (
        PropertyType.EVG_PROP,
        PropertyType.EVG_STATUS,
        PropertyType.EVG_STATIC,
        PropertyType.GROUP_DYN,
        PropertyType.GROUP_STATUS,
        PropertyType.GROUP_FAILURE,
    ):
        prog.set_read(pid, b"\x00" * (8 * MAX_ECG))
    await comm.post_installation(flags=3, pre_assign_group=2, interval=0.0)
    (cmd,) = [w["data"] for w in prog.writes_for(PropertyType.COMMAND)]
    assert cmd == bytes((DeviceCommand.POST_INSTALLATION, 3, 2))


async def test_write_scenes_builds_tables_and_syncs() -> None:
    comm, prog = _setup()
    prog.set_read(
        PropertyType.SCENE_KNX_MAP, bytes((0, 0))
    )  # size 0 -> write size + map
    prog.queue_read(PropertyType.COMMAND, bytes((0, 0, 0)))  # SCENE_SYNC done

    await comm.write_scenes(
        [Scene(index=0, fade_time=3, knx_scene=7, values=[SceneValue(0, 16, 254)])]
    )
    (assign,) = prog.writes_for(PropertyType.SCENE_ASSIGN)
    assert bytes(assign["data"])[0] == 3 and assign["count"] == 16  # type: ignore[index]
    (values,) = prog.writes_for(PropertyType.SCENE_GROUP_VALUE)
    data = bytes(values["data"])  # type: ignore[arg-type]
    assert data[:8] == bytes((0, 16, 254, 0, 0, 0, 0, 0))  # first record
    assert data[-8:] == b"\xff" * 8  # terminator
    assert bytes((DeviceCommand.SCENE_SYNC, 0, 0)) in [
        w["data"] for w in prog.writes_for(PropertyType.COMMAND)
    ]
