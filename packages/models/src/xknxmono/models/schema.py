from __future__ import annotations

import importlib
import re
from types import ModuleType
from typing import Any

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

SUPPORTED_VERSIONS = frozenset({"10", "11", "12", "13", "14", "20", "21", "22", "23"})

VERSION_PATTERN = re.compile(rb'xmlns="http://knx\.org/xml/project/(\d+)"')

VERSION_MODULES: dict[str, ModuleType | None] = {v: None for v in SUPPORTED_VERSIONS}


def _load_version(version: str) -> ModuleType:
    mod = VERSION_MODULES[version]
    if mod is None:
        mod = importlib.import_module(f"xknxmono.models.files.v{version}")
        VERSION_MODULES[version] = mod
    return mod


VERSION_NAMESPACES = {v: f"http://knx.org/xml/project/{v}" for v in SUPPORTED_VERSIONS}

_parser = XmlParser()
_serializer = XmlSerializer(
    config=SerializerConfig(
        xml_declaration=True,
        encoding="UTF-8",
        indent="  ",
    )
)


class VersionError(Exception):
    pass


def detect_version(xml_bytes: bytes) -> str:
    match = VERSION_PATTERN.search(xml_bytes[:2000])
    if match:
        return match.group(1).decode("ascii")
    raise VersionError("Could not detect KNX namespace version")


def get_model_class(version: str) -> type[Any]:
    if version not in SUPPORTED_VERSIONS:
        raise VersionError(
            f"Unsupported KNX version: {version}. Supported: {', '.join(sorted(SUPPORTED_VERSIONS))}"
        )
    return _load_version(version).Knx


def load_xml(source: bytes, version: str | None = None) -> Any:
    if version is None:
        version = detect_version(source)
    model_class = get_model_class(version)
    return _parser.from_bytes(source, model_class)


def serialize_xml(obj: object, version: str) -> bytes:
    ns_map = {"": VERSION_NAMESPACES[version]}
    return _serializer.render(obj, ns_map=ns_map).encode("utf-8")  # type: ignore[reportUnknownMemberType]
