"""End-to-end parameter recovery against a real application (Gira fixture).

Encodes known values into the application's memory image with the forward encoder,
then recovers them from those bytes and asserts they round-trip. This proves the
best-effort decoder inverts the encoder for the reliable (integer / enum) types.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from xknxeditor.prod import load
from xknxeditor.prod.parser_v2.application_indexer import ApplicationIndexer
from xknxeditor.recover.parameters import recover_parameters
from xknxeditor.recover.recover import com_object_ref_by_number

_FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "prod"
    / "tests"
    / "fixtures"
    / "gira_2gang_button_interface.knxprod"
)


@pytest.fixture(scope="module")
def application():  # type: ignore[no-untyped-def]
    if not _FIXTURE.exists():
        pytest.skip(f"fixture missing: {_FIXTURE}")
    registry = load(str(_FIXTURE))
    return next(iter(registry.applications.values()))


def _ref_ids_for(application, parameter_id: str) -> list[str]:  # type: ignore[no-untyped-def]
    indexer = ApplicationIndexer(application.program)
    return [
        rid for rid, ref in indexer.parameter_refs.items() if ref.ref_id == parameter_id
    ]


def test_recover_integer_and_enum_parameters(application) -> None:  # type: ignore[no-untyped-def]
    number_id = f"{application.id}_P-3"  # number 0..255, default 0
    enum_id = f"{application.id}_P-1"  # enum {0, 1}, default 1
    number_ref = _ref_ids_for(application, number_id)[0]
    enum_ref = _ref_ids_for(application, enum_id)[0]

    ui = application.dynamic_ui()
    assert ui is not None
    ui.set_parameter_ref(number_ref, "42")
    ui.set_parameter_ref(enum_ref, "0")
    segments = ui.encode_to_memory()

    recovered = recover_parameters(application, segments)
    assert recovered.values[number_ref] == "42"
    assert recovered.values[enum_ref] == "0"


def test_recover_module_parameters_yields_instance_qualified_refs(application) -> None:  # type: ignore[no-untyped-def]
    # The Gira app is module-heavy; encoding its defaults and recovering must
    # produce instance-qualified module parameter refs (containing "_MI-"), proving
    # the per-instance module decode path runs and maps to qualified refs.
    ui = application.dynamic_ui()
    assert ui is not None
    segments = ui.encode_to_memory()
    recovered = recover_parameters(application, segments)
    module_refs = [ref for ref in recovered.values if "_MI-" in ref]
    assert module_refs, "expected module-instance-qualified parameter refs"


def test_com_object_ref_by_number_is_populated(application) -> None:  # type: ignore[no-untyped-def]
    mapping = com_object_ref_by_number(application)
    assert mapping  # the application defines com objects
    # Every value is a com object reference id of this application.
    assert all(ref_id.startswith(application.id) for ref_id in mapping.values())


def test_seeded_ui_yields_com_object_mapping(application) -> None:  # type: ignore[no-untyped-def]
    from xknxeditor.recover.recover import seed_dynamic_ui

    # Seeding with a recovered structural value must still yield a mapping (module
    # instances materialised from the seeded state, not just the defaults).
    ui = seed_dynamic_ui(application, {f"{application.id}_P-1_R-15": "1"})
    assert ui is not None
    mapping = com_object_ref_by_number(application, ui)
    assert mapping
    assert all(ref_id.startswith(application.id) for ref_id in mapping.values())


def test_com_object_ref_by_number_covers_every_defined_number(application) -> None:  # type: ignore[no-untyped-def]
    """Every defined com object number resolves to a reference id.

    The parameter-driven UI may not expose objects a device can still link (optional
    channels on System B). ``com_object_ref_by_number`` must fall back to the
    application's static com object references so recovered links to those numbers
    are not dropped when rebuilding the group communication tables."""
    from xknxeditor.recover.recover import com_object_ref_by_number

    indexer = ApplicationIndexer(application.program)
    defined = {
        co.number
        for ref in indexer.com_object_refs.values()
        if (co := indexer.com_objects.get(ref.ref_id)) is not None
    }
    mapping = com_object_ref_by_number(application)
    assert defined
    assert defined <= set(mapping), sorted(defined - set(mapping))
