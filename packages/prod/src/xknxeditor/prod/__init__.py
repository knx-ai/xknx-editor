from __future__ import annotations

from typing import TYPE_CHECKING

__version__ = "0.1.0"

# Public names load lazily through __getattr__ (PEP 562); import them the usual way.
_LAZY: dict[str, tuple[str, str]] = {
    "Application": (".application", "Application"),
    "parse_application_xml": (".application", "parse_application_xml"),
    "Archive": (".archive", "Archive"),
    "CatalogItem": (".catalog", "CatalogItem"),
    "CatalogSection": (".catalog", "CatalogSection"),
    "parse_catalog_xml": (".catalog", "parse_catalog_xml"),
    "DeviceProgram": (".hardware", "DeviceProgram"),
    "Hardware": (".hardware", "Hardware"),
    "HardwareDoc": (".hardware", "HardwareDoc"),
    "Product": (".hardware", "Product"),
    "parse_hardware_xml": (".hardware", "parse_hardware_xml"),
    "load": (".loader", "load"),
    "knxprod_from_source": (".openknx", "knxprod_from_source"),
    "monolithic_to_knxprod": (".openknx", "monolithic_to_knxprod"),
    "openknx_release_to_knxprod": (".openknx", "openknx_release_to_knxprod"),
    "MasterData": (".master", "MasterData"),
    "parse_master_xml": (".master", "parse_master_xml"),
    "ParamTypeKind": (".types", "ParamTypeKind"),
    "Registry": (".registry", "Registry"),
}

__all__ = [
    "Application",
    "Archive",
    "CatalogItem",
    "CatalogSection",
    "DeviceProgram",
    "Hardware",
    "HardwareDoc",
    "MasterData",
    "ParamTypeKind",
    "Product",
    "Registry",
    "knxprod_from_source",
    "load",
    "monolithic_to_knxprod",
    "openknx_release_to_knxprod",
    "parse_application_xml",
    "parse_catalog_xml",
    "parse_hardware_xml",
    "parse_master_xml",
]

if TYPE_CHECKING:
    from .application import Application, parse_application_xml
    from .archive import Archive
    from .catalog import CatalogItem, CatalogSection, parse_catalog_xml
    from .hardware import (
        DeviceProgram,
        Hardware,
        HardwareDoc,
        Product,
        parse_hardware_xml,
    )
    from .loader import load
    from .master import MasterData, parse_master_xml
    from .openknx import (
        knxprod_from_source,
        monolithic_to_knxprod,
        openknx_release_to_knxprod,
    )
    from .registry import Registry
    from .types import ParamTypeKind


def __getattr__(name: str) -> object:
    if name in _LAZY:
        import importlib

        module_path, attr = _LAZY[name]
        mod = importlib.import_module(module_path, __package__)
        value = getattr(mod, attr)
        # memoize so later lookups skip the import
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
