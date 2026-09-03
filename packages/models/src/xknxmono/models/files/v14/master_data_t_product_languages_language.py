from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://knx.org/xml/project/14"


@dataclass(slots=True, kw_only=True)
class MasterDataProductLanguagesLanguage:
    class Meta:
        global_type = False

    identifier: None | str = field(
        default=None,
        metadata={
            "name": "Identifier",
            "type": "Attribute",
        },
    )
