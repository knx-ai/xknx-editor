"""Health checks for com-object linking, exercised with a lightweight fake project.

``HealthService`` only reads a small surface of ``ProjectService`` (devices, their visible com
objects, and the links per com object), so we feed it fakes instead of a real project/DB."""

from __future__ import annotations

from types import SimpleNamespace

from editor_gui.plugins.health.service import HealthService, Severity


def _co(
    db_id: int, *, communication: bool = True, transmit: bool = True
) -> SimpleNamespace:
    return SimpleNamespace(
        db_id=db_id,
        flags=SimpleNamespace(communication=communication, transmit=transmit),
    )


def _device(
    name: str, node_id: int, com_objects: list[SimpleNamespace]
) -> SimpleNamespace:
    return SimpleNamespace(
        name=name,
        node_id=node_id,
        individual_address=f"1.1.{node_id}",
        get_visible_com_objects=lambda: com_objects,
    )


class _FakeProject:
    def __init__(
        self, devices: list[SimpleNamespace], links: dict[int, list[SimpleNamespace]]
    ) -> None:
        self.devices = devices
        self._links = links
        self.revision = 1
        self.is_open = True
        self.group_addresses: list[object] = []

    def missing_program_refs(self) -> list[str]:
        return []

    def get_links_for_com_object(self, db_id: int) -> list[SimpleNamespace]:
        return self._links.get(db_id, [])

    def get_assignments_for_ga(self, ga_id: int) -> list[object]:
        return []


def _com_object_findings(project: _FakeProject) -> list[str]:
    svc = HealthService(project)  # type: ignore[arg-type]
    return [f.message for f in svc.findings() if f.category == "com-object"]


def _link(is_sending: bool) -> SimpleNamespace:
    return SimpleNamespace(is_sending=is_sending)


def test_transmit_object_linked_only_receiving_is_flagged() -> None:
    # A push-button/sensor object (transmit) linked without a sending group address never sends.
    dev = _device("Taster", 58, [_co(1)])
    project = _FakeProject([dev], {1: [_link(is_sending=False)]})
    svc = HealthService(project)  # type: ignore[arg-type]
    findings = [f for f in svc.findings() if f.category == "com-object"]
    assert any(
        f.severity is Severity.WARNING and "never send" in f.message for f in findings
    )
    assert findings[0].device_node_id == 58


def test_transmit_object_with_a_sending_link_is_ok() -> None:
    dev = _device("Taster", 58, [_co(1)])
    project = _FakeProject([dev], {1: [_link(is_sending=True)]})
    assert not any("never send" in m for m in _com_object_findings(project))


def test_receive_only_object_is_not_flagged() -> None:
    # A receive-only object (no transmit) linked as receiving is correct, not a defect.
    dev = _device("Aktor", 59, [_co(1, transmit=False)])
    project = _FakeProject([dev], {1: [_link(is_sending=False)]})
    assert not any("never send" in m for m in _com_object_findings(project))


def test_unlinked_object_is_not_reported_as_never_sending() -> None:
    # No links at all -> the existing "unlinked" info, not the "never send" warning.
    dev = _device("Taster", 58, [_co(1)])
    project = _FakeProject([dev], {1: []})
    messages = _com_object_findings(project)
    assert any("unlinked" in m for m in messages)
    assert not any("never send" in m for m in messages)
