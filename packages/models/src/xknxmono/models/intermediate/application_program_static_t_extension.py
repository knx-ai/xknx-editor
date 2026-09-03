from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.intermediate.application_program_static_t_extension_baggage import (
    ApplicationProgramStaticExtensionBaggage,
)
from xknxmono.models.intermediate.capability_t import Capability


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticExtension:
    class Meta:
        global_type = False

    baggage: list[ApplicationProgramStaticExtensionBaggage] = field(
        default_factory=list,
        metadata={
            "name": "Baggage",
            "type": "Element",
        },
    )
    ets_download_plugin: None | str = field(
        default=None,
        metadata={
            "name": "EtsDownloadPlugin",
            "type": "Attribute",
        },
    )
    ets_ui_plugin: None | str = field(
        default=None,
        metadata={
            "name": "EtsUiPlugin",
            "type": "Attribute",
        },
    )
    ets_data_handler: None | str = field(
        default=None,
        metadata={
            "name": "EtsDataHandler",
            "type": "Attribute",
        },
    )
    ets_data_handler_capabilities: list[Capability] = field(
        default_factory=list,
        metadata={
            "name": "EtsDataHandlerCapabilities",
            "type": "Attribute",
            "tokens": True,
        },
    )
    requires_external_software: bool = field(
        default=False,
        metadata={
            "name": "RequiresExternalSoftware",
            "type": "Attribute",
        },
    )
