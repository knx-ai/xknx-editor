from __future__ import annotations

from pathlib import Path

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from xknxmono.keyring.files.knx_keyring import Keyring

__NAMESPACE__ = "http://knx.org/xml/keyring/1"

_parser = XmlParser()
_serializer = XmlSerializer(
    config=SerializerConfig(
        xml_declaration=True,
        encoding="UTF-8",
        indent="  ",
    )
)


def load_keyring(source: str | Path | bytes) -> Keyring:
    """Parse keyring XML from bytes or file path into a Keyring object."""
    if isinstance(source, bytes):
        return _parser.from_bytes(source, Keyring)
    return _parser.from_path(Path(source), Keyring)


def serialize_keyring(keyring: Keyring) -> bytes:
    """Serialize a Keyring object to XML bytes."""
    ns_map = {"": __NAMESPACE__}
    return _serializer.render(keyring, ns_map=ns_map).encode("utf-8")  # type: ignore[reportUnknownMemberType]
