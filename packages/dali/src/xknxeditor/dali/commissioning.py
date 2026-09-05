"""High-level MDT DALI commissioning flows over an :class:`MdtDaliConnection`.

Implements: read-only bus scan (P1), identify/blink (P2), group/ECG assignment download (P3), scene
write (P4), and new/post installation (P5, DALI bus scan + short-address assignment). Every write /
installation flow should be preceded by a scan and gated behind a user confirm in the GUI.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Sequence

from xknxeditor.dali.connection import DaliCommissioningError, MdtDaliConnection
from xknxeditor.dali.model import (
    GROUP_UNASSIGNED,
    MAX_ECG,
    MAX_GROUP,
    MAX_SCENES,
    DaliBusState,
    EcgAssignment,
    EcgState,
    GroupState,
    Scene,
    group_present,
)
from xknxeditor.dali.properties import (
    BLINK_AUTO,
    BLINK_STOP,
    DeviceCommand,
    PropertyType,
)
from xknxeditor.dali.structs import (
    SCENE_TERMINATOR,
    Command,
    CommissionSync,
    EcgProp,
    EcgStatic,
    EcgStatus,
    GroupDyn,
    GroupFailure,
    GroupStatus,
    SceneAssign,
    SceneItemValue,
    SceneKnxMap,
    decode_table,
    encode_table,
)


class MdtDaliCommissioner:
    """DALI bus commissioning for one channel of an MDT gateway."""

    def __init__(self, connection: MdtDaliConnection) -> None:
        self._c = connection

    # --- P1: read-only scan ------------------------------------------------

    async def scan(self) -> DaliBusState:
        """Read the full bus state (firmware, per-slot ECG props/status/static, group data)."""
        firmware = await self._c.read_firmware()
        props = decode_table(
            await self._c.read_table(PropertyType.EVG_PROP, MAX_ECG), 4
        )
        status = decode_table(
            await self._c.read_table(PropertyType.EVG_STATUS, MAX_ECG), 5
        )
        static = decode_table(
            await self._c.read_table(PropertyType.EVG_STATIC, MAX_ECG), 8
        )
        ecgs: list[EcgState] = []
        for slot in range(MAX_ECG):
            p = EcgProp.decode(props[slot]) if slot < len(props) else None
            if p is None:
                continue
            st = EcgStatic.decode(static[slot]) if slot < len(static) else None
            stat = EcgStatus.decode(status[slot]) if slot < len(status) else None
            ecgs.append(
                EcgState(
                    slot=slot,
                    present=group_present(p.group_index),
                    ecg_type=p.ecg_type,
                    sub_type=p.sub_type,
                    group_index=p.group_index,
                    ets_ecg_index=p.ets_ecg_index,
                    long_address=st.long_address if st else 0,
                    min_value=st.min_value if st else 0,
                    min_color_temp=st.min_color_temp if st else 0,
                    max_color_temp=st.max_color_temp if st else 0,
                    alarm=stat.alarm if stat else 0,
                )
            )
        groups = await self._read_groups()
        return DaliBusState(
            channel=self._c.channel, firmware=firmware, ecgs=ecgs, groups=groups
        )

    async def _read_groups(self) -> list[GroupState]:
        dyn = decode_table(
            await self._c.read_table(PropertyType.GROUP_DYN, MAX_GROUP), 6
        )
        status = decode_table(
            await self._c.read_table(PropertyType.GROUP_STATUS, MAX_GROUP), 8
        )
        failure = decode_table(
            await self._c.read_table(PropertyType.GROUP_FAILURE, MAX_GROUP), 6
        )
        groups: list[GroupState] = []
        for i in range(MAX_GROUP):
            d = GroupDyn.decode(dyn[i]) if i < len(dyn) else GroupDyn(0, 0)
            s = GroupStatus.decode(status[i]) if i < len(status) else None
            f = GroupFailure.decode(failure[i]) if i < len(failure) else None
            groups.append(
                GroupState(
                    index=i,
                    run_hours=d.run_hours,
                    run_seconds=d.run_seconds,
                    knx_value=s.knx_value if s else 0,
                    ecg_count=f.ecg_count if f else 0,
                    lamp_failures=f.lamp_fail_count if f else 0,
                    ecg_failures=f.ecg_fail_count if f else 0,
                )
            )
        return groups

    # --- P2: identify ------------------------------------------------------

    async def switch_ecg(self, slot: int, on: bool) -> None:
        """Switch a single ECG (by physical slot) fully on/off."""
        await self._c.send_command(DeviceCommand.SET_ECG_VALUE, slot, 0xFF if on else 0)

    async def blink_ecg(self, slot: int, start: bool = True) -> None:
        """Start/stop auto-blink on a single ECG (to physically identify it)."""
        param1 = slot | (BLINK_AUTO if start else BLINK_STOP)
        await self._c.send_command(DeviceCommand.BLINK, param1, 0)

    async def switch_group(self, group: int, on: bool) -> None:
        await self._c.send_command(
            DeviceCommand.SET_GROUP_VALUE, group, 0xFF if on else 0
        )

    async def blink_group(self, group: int, start: bool = True) -> None:
        param1 = group | (BLINK_AUTO if start else BLINK_STOP)
        await self._c.send_command(DeviceCommand.BLINK, param1, 0)

    async def broadcast(self, on: bool) -> None:
        """Switch all ECGs on/off (broadcast)."""
        await self._c.send_command(DeviceCommand.SET_ALL_ECG, 0xFF if on else 0, 0)

    # --- P3: assignment download ------------------------------------------

    async def commission(self, assignments: Sequence[EcgAssignment]) -> bool:
        """Write the full 64-slot group/ECG assignment table, apply it, and verify.

        The ComissionSync table is always the complete 64 slots (PLUGIN_SYNC applies every slot), so
        it is first seeded from the device's CURRENT mapping (a fresh EVG_PROP read) and the caller's
        ``assignments`` are overlaid on top — otherwise unlisted slots would be silently wiped to
        unassigned. Returns True when the device read-back matches the requested (ets, group) mapping.
        """
        by_slot = {a.slot: a for a in assignments}
        current = decode_table(
            await self._c.read_table(PropertyType.EVG_PROP, MAX_ECG), 4
        )
        elements: list[bytes] = []
        for slot in range(MAX_ECG):
            if slot in by_slot:
                sync = CommissionSync(
                    by_slot[slot].ets_index, by_slot[slot].group_index
                )
            elif slot < len(current):
                p = EcgProp.decode(current[slot])
                sync = CommissionSync(p.ets_ecg_index, p.group_index)
            else:
                sync = CommissionSync(slot, GROUP_UNASSIGNED)
            elements.append(sync.encode())
        await self._c.write_table(
            PropertyType.COMMISSION_SYNC, encode_table(elements), MAX_ECG
        )
        await self._c.run_command(DeviceCommand.PLUGIN_SYNC, timeout=180.0)
        return await self._verify(by_slot)

    async def _verify(self, by_slot: dict[int, EcgAssignment]) -> bool:
        """Re-read EVG_PROP and confirm every requested slot's ets-index AND group match."""
        props = decode_table(
            await self._c.read_table(PropertyType.EVG_PROP, MAX_ECG), 4
        )
        for slot, want in by_slot.items():
            if slot >= len(props):
                return False
            got = EcgProp.decode(props[slot])
            if (
                got.group_index != want.group_index
                or got.ets_ecg_index != want.ets_index
            ):
                return False
        return True

    # --- P4: scenes --------------------------------------------------------

    async def write_scenes(self, scenes: Sequence[Scene]) -> None:
        """Write scene fade times, per-target values, and the KNX scene map, then apply."""
        assign = encode_table(
            [SceneAssign(_scene_fade(scenes, i)).encode() for i in range(MAX_SCENES)]
        )
        records: list[bytes] = []
        for scene in scenes:
            for v in sorted(scene.values, key=lambda x: x.target_index):
                records.append(
                    SceneItemValue(
                        scene.index, v.target_index, v.level, v.color, v.flags
                    ).encode()
                )
        records.append(SCENE_TERMINATOR)

        await self._maybe_write_knx_map(scenes)
        await asyncio.sleep(0.5)
        await self._c.write_table(PropertyType.SCENE_ASSIGN, assign, MAX_SCENES)
        await asyncio.sleep(0.5)
        await self._c.write_table(
            PropertyType.SCENE_GROUP_VALUE, encode_table(records), len(records)
        )
        await self._c.run_command(DeviceCommand.SCENE_SYNC, timeout=180.0)

    async def _maybe_write_knx_map(self, scenes: Sequence[Scene]) -> None:
        """Write the KNX scene-number map if the firmware supports it (table size probe)."""
        try:
            size = await self._c.read_table_size(PropertyType.SCENE_KNX_MAP)
        except DaliCommissioningError:
            return  # firmware without KNX scene map
        if size is None:
            return  # property absent/unsupported (short response) -> don't write it
        knx_map = encode_table(
            [SceneKnxMap(_scene_knx(scenes, i)).encode() for i in range(MAX_SCENES)]
        )
        if size == 0:
            await self._c.write_table_size(PropertyType.SCENE_KNX_MAP, MAX_SCENES)
        await self._c.write_table(PropertyType.SCENE_KNX_MAP, knx_map, MAX_SCENES)

    # --- P5: new / post installation (bus renumbering — gate behind a confirm) ---

    async def new_installation(
        self,
        *,
        pre_assign_group: int = 0,
        timeout: float = 300.0,
        interval: float = 1.0,
        on_progress: Callable[[Command], None] | None = None,
    ) -> DaliBusState:
        """Full DALI bus scan with short-address (re)assignment, then read back the new state.

        Wipes and re-numbers every ballast on the bus (destructive) — always confirm with the user
        first. ``pre_assign_group`` optionally pre-assigns found ECGs to a group (firmware permitting).
        ``on_progress`` receives the live readback whose ``param1``/``param2`` are the found counters.
        """
        await self._c.run_command(
            DeviceCommand.NEW_INSTALLATION,
            0,
            pre_assign_group,
            timeout=timeout,
            interval=interval,
            on_progress=on_progress,
        )
        return await self.scan()

    async def post_installation(
        self,
        *,
        flags: int = 0,
        pre_assign_group: int = 0,
        timeout: float = 300.0,
        interval: float = 1.0,
        on_progress: Callable[[Command], None] | None = None,
    ) -> DaliBusState:
        """Add newly-found ECGs without renumbering the existing ones, then read back.

        ``flags`` is the raw MDT option byte (keep-unknown / delete-missing short addresses);
        ``on_progress`` readbacks carry found (param1) and removed (param2) counters.
        """
        await self._c.run_command(
            DeviceCommand.POST_INSTALLATION,
            flags,
            pre_assign_group,
            timeout=timeout,
            interval=interval,
            on_progress=on_progress,
        )
        return await self.scan()

    async def abort(self) -> None:
        """Abort a running installation/command."""
        await self._c.send_command(DeviceCommand.ABORT)


def _scene_fade(scenes: Sequence[Scene], index: int) -> int:
    for s in scenes:
        if s.index == index:
            return s.fade_time
    return 0


def _scene_knx(scenes: Sequence[Scene], index: int) -> int:
    for s in scenes:
        if s.index == index:
            return s.knx_scene
    return 0


__all__ = ["MdtDaliCommissioner"]
