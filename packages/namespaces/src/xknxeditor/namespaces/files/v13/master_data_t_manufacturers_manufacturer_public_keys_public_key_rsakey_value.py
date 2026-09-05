from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/13"


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue:
    class Meta:
        global_type = False

    modulus: bytes = field(
        metadata={
            "name": "Modulus",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
            "format": "base64",
        }
    )
    exponent: bytes = field(
        metadata={
            "name": "Exponent",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/13",
            "format": "base64",
        }
    )
