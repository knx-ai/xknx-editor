from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue:
    class Meta:
        global_type = False

    modulus: None | bytes = field(
        default=None,
        metadata={
            "name": "Modulus",
            "type": "Element",
            "format": "base64",
        },
    )
    exponent: None | bytes = field(
        default=None,
        metadata={
            "name": "Exponent",
            "type": "Element",
            "format": "base64",
        },
    )
