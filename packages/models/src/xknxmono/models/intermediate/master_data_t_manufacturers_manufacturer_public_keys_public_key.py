from __future__ import annotations
from dataclasses import dataclass, field
from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_public_keys_public_key_rsakey_value import (
    MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue,
)


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturerPublicKeysPublicKey:
    class Meta:
        global_type = False

    rsakey_value: (
        None | MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue
    ) = field(
        default=None,
        metadata={
            "name": "RSAKeyValue",
            "type": "Element",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    number: int = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
        }
    )
    revoked: bool = field(
        default=False,
        metadata={
            "name": "Revoked",
            "type": "Attribute",
        },
    )
    purpose: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Purpose",
            "type": "Attribute",
            "tokens": True,
        },
    )
