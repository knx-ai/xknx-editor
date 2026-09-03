from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v23.master_data_t_manufacturers_manufacturer_public_keys_public_key_rsakey_value import (
    MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue,
)

__NAMESPACE__ = "http://knx.org/xml/project/23"


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturerPublicKeysPublicKey:
    class Meta:
        global_type = False

    rsakey_value: MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue = (
        field(
            metadata={
                "name": "RSAKeyValue",
                "type": "Element",
                "namespace": "http://knx.org/xml/project/23",
            }
        )
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
