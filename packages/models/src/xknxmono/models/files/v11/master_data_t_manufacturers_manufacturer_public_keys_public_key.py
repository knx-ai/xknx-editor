from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v11.master_data_t_manufacturers_manufacturer_public_keys_public_key_rsakey_value import (
    MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue,
)

__NAMESPACE__ = "http://knx.org/xml/project/11"


@dataclass(slots=True, kw_only=True)
class MasterDataManufacturersManufacturerPublicKeysPublicKey:
    class Meta:
        global_type = False

    rsakey_value: MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue = (
        field(
            metadata={
                "name": "RSAKeyValue",
                "type": "Element",
                "namespace": "http://knx.org/xml/project/11",
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
