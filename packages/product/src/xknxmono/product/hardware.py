"""Hardware entities — flat records holding only ids/ref-ids (no resolved links).

`parse_hardware_xml` returns a `HardwareDoc`: the flat `Hardware`/`Product`/`DeviceProgram` records
plus the intra-file edges (which products / programs belong to which hardware). Cross-file edges
(program → application) and resolution live in the Registry.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

from xknxmono.models import detect_version

from .data import to_ir

if TYPE_CHECKING:
    from xknxmono.models import intermediate as ir


@dataclass(frozen=True, slots=True)
class Product:
    """An orderable variant (SKU) of a hardware."""

    id: str
    order_number: str | None
    name: str | None
    width_mm: float | None
    rail_mounted: bool
    raw: ir.HardwareProductsProduct


@dataclass(frozen=True, slots=True)
class DeviceProgram:
    """A Hardware2Program binding. `application_ref_ids` are the firmware program(s) it references;
    resolve them against the Registry."""

    id: str
    application_ref_ids: list[str]
    raw: ir.Hardware2Program


@dataclass(frozen=True, slots=True)
class Hardware:
    """A physical device. Its products and programs are reached through the Registry edges."""

    id: str
    name: str | None
    raw: ir.Hardware


@dataclass(frozen=True, slots=True)
class HardwareDoc:
    """The result of parsing one Hardware XML: dict stores (by id) and id-list edges."""

    hardware: dict[str, Hardware]
    products: dict[str, Product]
    programs: dict[str, DeviceProgram]
    hardware_to_product: dict[str, list[str]]
    hardware_to_program: dict[str, list[str]]


def _hardware(knx: ir.Knx) -> Iterator[ir.Hardware]:
    if knx.manufacturer_data is None:
        return
    for manufacturer in knx.manufacturer_data.manufacturer:
        if manufacturer.hardware is not None:
            yield from manufacturer.hardware.hardware


def parse_hardware_xml(xml_bytes: bytes) -> HardwareDoc:
    knx = to_ir(xml_bytes, detect_version(xml_bytes))
    hardware: dict[str, Hardware] = {}
    products: dict[str, Product] = {}
    programs: dict[str, DeviceProgram] = {}
    hw_to_product: dict[str, list[str]] = {}
    hw_to_program: dict[str, list[str]] = {}

    for hw in _hardware(knx):
        hardware[hw.id] = Hardware(id=hw.id, name=hw.name, raw=hw)

        hw_products = {
            p.id: Product(
                id=p.id,
                order_number=p.order_number,
                name=p.text,
                width_mm=p.width_in_millimeter,
                rail_mounted=bool(p.is_rail_mounted),
                raw=p,
            )
            for p in (hw.products.product if hw.products else [])
        }
        products.update(hw_products)
        hw_to_product[hw.id] = list(hw_products)

        hw_programs = {
            h2p.id: DeviceProgram(
                id=h2p.id,
                application_ref_ids=[
                    ref.ref_id for ref in h2p.application_program_ref if ref.ref_id
                ],
                raw=h2p,
            )
            for h2p in (
                hw.hardware2_programs.hardware2_program if hw.hardware2_programs else []
            )
        }
        programs.update(hw_programs)
        hw_to_program[hw.id] = list(hw_programs)

    return HardwareDoc(
        hardware=hardware,
        products=products,
        programs=programs,
        hardware_to_product=hw_to_product,
        hardware_to_program=hw_to_program,
    )
