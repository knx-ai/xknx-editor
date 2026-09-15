"""Regression: module com-objects (MDT/Gira button channels) must surface and get a db_id.

We persist two lossy forms per com-object row: ``ref_id`` is xknxproject's ``com_object_ref_id``
(app-prefixed but with the module-instance segment stripped, so distinct instances collapse to one
string), and ``instance_ref_id`` is the raw ETS ``@RefId`` (per-instance but with no app prefix).
The dynamic UI keys every object by the app-prefixed, per-instance ``qualify()`` form, which matches
neither stored form on its own -> module button channels were pruned from the visible set and their
group-address links resolved to "?". ``_qualified_com_object_ref`` reconstructs the UI form from the
per-instance ``instance_ref_id``; this proves it round-trips and that a device built from the stored
forms now shows its module objects with ``db_id`` attached (and would not with the stripped ref).
"""

from pathlib import Path
from types import SimpleNamespace

import pytest

from editor_gui.device import Device
from editor_gui.plugins.project.service import (
    _co_instance_ref_from_row,
    _qualified_com_object_ref,
)
from xknxeditor.namespaces.intermediate.com_object_instance_ref_t import (
    ComObjectInstanceRef,
)
from xknxeditor.prod import Application, load
from xknxeditor.prod.parser_v2.ui import UiComObject, UiNode, UiParameterBlock, UiTab

_APP_ID = "M-0008_A-7072-21-5CC3-O000A"


def _fixture_path() -> Path:
    # tests run from the repo but the package tree nests deep; walk up to the monorepo root.
    p = Path(__file__).resolve()
    for parent in p.parents:
        cand = (
            parent
            / "packages"
            / "prod"
            / "tests"
            / "fixtures"
            / "gira_2gang_button_interface.knxprod"
        )
        if cand.exists():
            return cand
    raise FileNotFoundError("gira_2gang_button_interface.knxprod not found")


def _app() -> Application:
    return load(_fixture_path().read_bytes()).applications[_APP_ID]


def _ui_com_object_refs(nodes: list[UiNode]) -> list[str]:
    out: list[str] = []
    for node in nodes:
        if isinstance(node, UiComObject):
            out.append(node.ref_id)
        elif isinstance(node, (UiTab, UiParameterBlock)):
            out.extend(_ui_com_object_refs(list(node.children)))
    return out


def _stored_row(app: Application, qualified_ref: str) -> SimpleNamespace:
    """Emulate a persisted ComObject row: strip the app prefix for the raw ``@RefId`` and run it
    through xknxproject's ``strip_module_instance`` for the shared ``com_object_ref_id``."""
    from xknxproject.util import strip_module_instance

    prefix = f"{app.program.id}_"
    assert qualified_ref.startswith(prefix)
    instance_ref_id = qualified_ref[len(prefix) :]
    stripped = strip_module_instance(instance_ref_id, "O")
    return SimpleNamespace(
        id=hash(qualified_ref) & 0xFFFF,
        ref_id=f"{prefix}{stripped}",
        instance_ref_id=instance_ref_id,
        communication_flag=None,
        read_flag=None,
        write_flag=None,
        transmit_flag=None,
        update_flag=None,
        read_on_init_flag=None,
    )


def test_qualified_ref_roundtrips_to_ui_form() -> None:
    app = _app()
    ui_refs = _ui_com_object_refs(app.dynamic_ui().eval_unpruned_ui())  # type: ignore[union-attr]
    assert ui_refs, "fixture must expose module com-objects"
    for ref in ui_refs:
        row = _stored_row(app, ref)
        # The stored ref_id (stripped) and instance_ref_id (unprefixed) both differ from the UI form.
        assert row.ref_id != ref
        assert row.instance_ref_id != ref
        # The reconstruction restores exactly the UI form the dynamic evaluator emits.
        assert _qualified_com_object_ref(row, app.program.id) == ref


def test_qualified_ref_falls_back_to_ref_id_when_no_instance() -> None:
    # Editor-created objects have no raw @RefId; the app-prefixed ref_id is already the UI form.
    row = SimpleNamespace(ref_id=f"{_APP_ID}_O-1_R-1", instance_ref_id="")
    assert _qualified_com_object_ref(row, _APP_ID) == f"{_APP_ID}_O-1_R-1"


def test_module_objects_surface_with_db_id() -> None:
    app = _app()
    ui_refs = _ui_com_object_refs(app.dynamic_ui().eval_unpruned_ui())  # type: ignore[union-attr]
    rows = [_stored_row(app, ref) for ref in ui_refs]

    coirs = [
        _co_instance_ref_from_row(
            r, ref_id=_qualified_com_object_ref(r, app.program.id)
        )
        or ComObjectInstanceRef(ref_id=_qualified_com_object_ref(r, app.program.id))
        for r in rows
    ]
    device = Device(
        node_id=1,
        name="Gira 2gang",
        app=app,
        individual_address="1.1.1",
        parameter_instance_refs=[],
        module_instances=[],
        com_object_instance_refs=coirs,
    )
    for r in rows:
        co = device.find_com_object(_qualified_com_object_ref(r, app.program.id))
        assert co is not None
        co.db_id = r.id

    visible = device.get_visible_com_objects()
    assert len(visible) == len(ui_refs)
    assert all(co.db_id is not None for co in visible)


def test_stripped_ref_alone_prunes_module_objects() -> None:
    # Guards the regression: seeding coirs with the stored (stripped) ref_id — the pre-fix
    # behaviour — makes the dynamic UI prune every module object.
    app = _app()
    ui_refs = _ui_com_object_refs(app.dynamic_ui().eval_unpruned_ui())  # type: ignore[union-attr]
    rows = [_stored_row(app, ref) for ref in ui_refs]
    coirs = [ComObjectInstanceRef(ref_id=r.ref_id) for r in rows]
    device = Device(
        node_id=1,
        name="Gira 2gang",
        app=app,
        individual_address="1.1.1",
        com_object_instance_refs=coirs,
    )
    assert device.get_visible_com_objects() == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
