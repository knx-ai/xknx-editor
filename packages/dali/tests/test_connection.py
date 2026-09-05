"""Transport tests for MdtDaliConnection: command framing, poll state machine, table i/o."""

import pytest
from _dali_fakes import FakeProgrammer

from xknxeditor.dali.connection import DaliCommissioningError, MdtDaliConnection
from xknxeditor.dali.properties import DeviceCommand, PropertyType, object_index


def _conn(channel: int = 0) -> tuple[MdtDaliConnection, FakeProgrammer]:
    prog = FakeProgrammer()
    return MdtDaliConnection(prog, channel), prog


async def test_object_index_per_channel() -> None:
    assert object_index(0) == 6 and object_index(1) == 7


async def test_send_command_frames_three_bytes_on_object_6() -> None:
    conn, prog = _conn()
    await conn.send_command(DeviceCommand.PLUGIN_SYNC, 1, 2)
    (w,) = prog.writes_for(PropertyType.COMMAND)
    assert w["object_index"] == 6
    assert w["data"] == bytes((24, 1, 2))
    assert w["start_index"] == 1 and w["count"] == 1


async def test_poll_done_and_error_and_timeout() -> None:
    conn, prog = _conn()
    # running, running, done(0)
    prog.queue_read(
        PropertyType.COMMAND, bytes((1, 3, 0)), bytes((1, 5, 0)), bytes((0, 8, 0))
    )
    result = await conn.poll_result(timeout=5.0, interval=0.0)
    assert result.cmd == 0 and result.param1 == 8

    conn2, prog2 = _conn()
    prog2.queue_read(PropertyType.COMMAND, bytes((1, 0, 0)), bytes((0xFF, 0, 0)))
    with pytest.raises(DaliCommissioningError, match="error"):
        await conn2.poll_result(timeout=5.0, interval=0.0)

    conn3, prog3 = _conn()
    prog3.set_read(PropertyType.COMMAND, bytes((1, 0, 0)))  # never finishes
    with pytest.raises(DaliCommissioningError, match="timed out"):
        await conn3.poll_result(timeout=0.0, interval=0.0)


async def test_read_table_chunks_until_all_elements() -> None:
    conn, prog = _conn()
    # EVG_PROP is 4 B/elem; device returns 32 elems, then 32 elems.
    prog.queue_read(
        PropertyType.EVG_PROP, b"\x01\x00\x20\x00" * 32, b"\x02\x00\x05\x01" * 32
    )
    data = await conn.read_table(PropertyType.EVG_PROP, 64)
    assert len(data) == 64 * 4
    assert data[:4] == b"\x01\x00\x20\x00" and data[128:132] == b"\x02\x00\x05\x01"


async def test_table_size_read_write() -> None:
    conn, prog = _conn()
    prog.set_read(PropertyType.SCENE_KNX_MAP, bytes((0x00, 0x10)))
    assert await conn.read_table_size(PropertyType.SCENE_KNX_MAP) == 16
    await conn.write_table_size(PropertyType.SCENE_KNX_MAP, 16)
    (w,) = prog.writes_for(PropertyType.SCENE_KNX_MAP)
    assert w["data"] == bytes((0x00, 0x10)) and w["start_index"] == 0
