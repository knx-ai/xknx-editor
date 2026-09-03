"""Building-function edits: create/rename/set-type/remove and group-address assignment, each an
event with a working undo/redo round-trip. Spaces come from import, so the test inserts one space
directly, then drives everything through the public service methods."""

from pathlib import Path

from xknxmono.project import ProjectService
from xknxmono.project.models import Installation, Space


def _new(tmp_path: Path) -> tuple[ProjectService, str]:
    svc = ProjectService()
    pid = svc.create(tmp_path / "p.xknx", "P-0001")
    return svc, pid


def _space(svc: ProjectService, pid: str) -> int:
    session = svc._state(pid).session  # type: ignore[attr-defined]
    inst = session.query(Installation).first()
    assert inst is not None
    space = Space(installation_id=inst.id, name="Flur", space_type="Room")
    session.add(space)
    session.flush()
    return space.id


def _functions(svc: ProjectService, pid: str, space_id: int):
    def walk(spaces):
        for s in spaces:
            if s.id == space_id:
                return s.functions
            hit = walk(s.children)
            if hit is not None:
                return hit
        return None

    return walk(svc.space_tree(pid, 0)) or []


def test_create_rename_set_type_with_undo(tmp_path: Path) -> None:
    svc, pid = _new(tmp_path)
    sid = _space(svc, pid)

    fid = svc.create_function(pid, sid, "FT-1", "Deckenlicht")
    fns = _functions(svc, pid, sid)
    assert [(f.id, f.name, f.function_type) for f in fns] == [
        (fid, "Deckenlicht", "FT-1")
    ]

    svc.rename_function(pid, fid, "Deckenlicht Flur")
    svc.set_function_type(pid, fid, "FT-6")
    f = _functions(svc, pid, sid)[0]
    assert f.name == "Deckenlicht Flur" and f.function_type == "FT-6"

    svc.undo(pid)  # undo set_type
    assert _functions(svc, pid, sid)[0].function_type == "FT-1"
    svc.undo(pid)  # undo rename
    assert _functions(svc, pid, sid)[0].name == "Deckenlicht"
    svc.undo(pid)  # undo create
    assert _functions(svc, pid, sid) == []
    svc.redo(pid)  # redo create
    assert _functions(svc, pid, sid)[0].name == "Deckenlicht"


def test_function_group_address_assign_and_remove(tmp_path: Path) -> None:
    svc, pid = _new(tmp_path)
    sid = _space(svc, pid)
    fid = svc.create_function(pid, sid, "FT-1", "Licht")
    ga = svc.create_group_address(pid, 0, 1, "Schalten")

    link = svc.add_function_group_address(pid, fid, ga, role="DR-1")
    gas = _functions(svc, pid, sid)[0].group_addresses
    assert [(g.id, g.group_address_id, g.role) for g in gas] == [(link, ga, "DR-1")]

    svc.undo(pid)  # undo assign
    assert _functions(svc, pid, sid)[0].group_addresses == []
    svc.redo(pid)  # redo assign
    assert len(_functions(svc, pid, sid)[0].group_addresses) == 1

    svc.remove_function_group_address(pid, link)
    assert _functions(svc, pid, sid)[0].group_addresses == []
    svc.undo(pid)  # undo remove -> link back with same id + role
    gas = _functions(svc, pid, sid)[0].group_addresses
    assert [(g.id, g.role) for g in gas] == [(link, "DR-1")]


def test_remove_function_restores_on_undo(tmp_path: Path) -> None:
    svc, pid = _new(tmp_path)
    sid = _space(svc, pid)
    fid = svc.create_function(pid, sid, "FT-6", "Dimmer")
    ga = svc.create_group_address(pid, 0, 2, "Wert")
    svc.add_function_group_address(pid, fid, ga, role="DR-4")

    svc.remove_function(pid, fid)
    assert _functions(svc, pid, sid) == []

    svc.undo(pid)  # undo remove -> function AND its group-address link come back
    fns = _functions(svc, pid, sid)
    assert len(fns) == 1
    assert fns[0].id == fid and fns[0].name == "Dimmer"
    assert [(g.group_address_id, g.role) for g in fns[0].group_addresses] == [
        (ga, "DR-4")
    ]
