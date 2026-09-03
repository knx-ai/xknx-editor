"""Group-address folder edits: create/rename/remove of GroupRange folders (main/middle groups),
each an event with a working undo/redo round-trip. Folders are auto-numbered (next free number per
level); deleting a folder removes the group addresses in it (restored on undo)."""

from pathlib import Path

from xknxmono.project import ProjectService
from xknxmono.project.core.addressing import GroupAddressStyle


def _new(
    tmp_path: Path,
    style: GroupAddressStyle = GroupAddressStyle.THREE_LEVEL,
    name: str = "p.xknx",
) -> tuple[ProjectService, str]:
    svc = ProjectService()
    pid = svc.create(tmp_path / name, "P-0001", group_address_style=style)
    return svc, pid


def _roots(svc: ProjectService, pid: str):
    return svc.group_ranges(pid, 0)


def _find(nodes, range_id: int):
    for n in nodes:
        if n.id == range_id:
            return n
        hit = _find(n.children, range_id)
        if hit is not None:
            return hit
    return None


def test_create_main_group_auto_numbered_with_undo(tmp_path: Path) -> None:
    svc, pid = _new(tmp_path)

    first = svc.create_group_range(pid, 0, None, "Beleuchtung")
    second = svc.create_group_range(pid, 0, None, "Jalousie")
    assert first is not None and second is not None

    roots = _roots(svc, pid)
    by_id = {r.id: r for r in roots}
    # Auto-numbered from the lowest free main number: 0 << 11 -> stored start max(1, 0) = 1;
    # 1 << 11 = 2048.
    assert by_id[first].range_start == 1
    assert by_id[second].range_start == 2048
    assert by_id[first].name == "Beleuchtung"

    svc.undo(pid)  # remove "Jalousie"
    assert _find(_roots(svc, pid), second) is None
    svc.redo(pid)  # back
    assert _find(_roots(svc, pid), second) is not None


def test_create_middle_group_and_reuse_by_new_ga(tmp_path: Path) -> None:
    svc, pid = _new(tmp_path)
    main = svc.create_group_range(pid, 0, None, "Beleuchtung")  # main 0
    assert main is not None
    middle = svc.create_group_range(pid, 0, main, "EG")  # middle 0/0
    assert middle is not None
    assert [c.id for c in _find(_roots(svc, pid), main).children] == [middle]

    # Adding a GA at 0/0/1 must reuse the existing folders, not duplicate them, and keep our names.
    svc.create_group_address(pid, 0, 1, "Licht Flur")  # 0/0/1
    main_node = _find(_roots(svc, pid), main)
    assert main_node.name == "Beleuchtung"
    assert len(main_node.children) == 1
    assert main_node.children[0].name == "EG"
    assert [ga.name for ga in main_node.children[0].group_addresses] == ["Licht Flur"]


def test_rename_folder_with_undo(tmp_path: Path) -> None:
    svc, pid = _new(tmp_path)
    main = svc.create_group_range(pid, 0, None, "Alt")
    assert main is not None
    svc.rename_group_range(pid, main, "Neu")
    assert _find(_roots(svc, pid), main).name == "Neu"
    svc.undo(pid)
    assert _find(_roots(svc, pid), main).name == "Alt"


def test_remove_folder_takes_gas_and_restores_on_undo(tmp_path: Path) -> None:
    svc, pid = _new(tmp_path)
    main = svc.create_group_range(pid, 0, None, "Beleuchtung")  # main 0
    assert main is not None
    ga = svc.create_group_address(pid, 0, 1, "Licht")  # 0/0/1, nested under main 0

    svc.remove_group_range(pid, main)
    assert _find(_roots(svc, pid), main) is None
    assert all(g.address != 1 for g in svc.group_addresses(pid))

    svc.undo(pid)  # folder subtree (incl. the GA) comes back with original ids
    node = _find(_roots(svc, pid), main)
    assert node is not None and node.name == "Beleuchtung"
    assert ga in {g.id for g in svc.group_addresses(pid)}


def test_folders_gated_by_style(tmp_path: Path) -> None:
    # Free style has no folders at all.
    svc, pid = _new(tmp_path, GroupAddressStyle.FREE)
    assert svc.create_group_range(pid, 0, None, "x") is None

    # TwoLevel has main groups but no middle groups.
    svc2, pid2 = _new(tmp_path, GroupAddressStyle.TWO_LEVEL, name="two.xknx")
    main = svc2.create_group_range(pid2, 0, None, "Main")
    assert main is not None
    assert svc2.create_group_range(pid2, 0, main, "Middle") is None
