from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class LanguageDataTranslationUnitTranslationElementTranslation:
    class Meta:
        global_type = False

    attribute_name: str = field(
        metadata={
            "name": "AttributeName",
            "type": "Attribute",
        }
    )
    text: str = field(
        metadata={
            "name": "Text",
            "type": "Attribute",
        }
    )
