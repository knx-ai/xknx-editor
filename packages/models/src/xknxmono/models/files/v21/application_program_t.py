from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.application_program_dynamic_t import (
    ApplicationProgramDynamic,
)
from xknxmono.models.files.v21.application_program_ipconfig_t import (
    ApplicationProgramIpconfig,
)
from xknxmono.models.files.v21.application_program_static_t import (
    ApplicationProgramStatic,
)
from xknxmono.models.files.v21.application_program_t_module_defs import (
    ApplicationProgramModuleDefs,
)
from xknxmono.models.files.v21.application_program_type_t import ApplicationProgramType
from xknxmono.models.files.v21.load_procedure_style_t import LoadProcedureStyle

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ApplicationProgram:
    """
    :ivar static:
    :ivar module_defs:
    :ivar dynamic:
    :ivar id: registration-relevant
    :ivar application_number: registration-relevant
    :ivar application_version: registration-relevant
    :ivar program_type: registration-relevant
    :ivar mask_version: registration-relevant
    :ivar visible_description:
    :ivar name:
    :ivar load_procedure_style: registration-relevant
    :ivar pei_type: registration-relevant
    :ivar hardware_type: registration-relevant
    :ivar help_topic:
    :ivar help_file:
    :ivar context_help_file:
    :ivar icon_file:
    :ivar default_language:
    :ivar dynamic_table_management: registration-relevant
    :ivar linkable: registration-relevant
    :ivar is_secure_enabled: registration-relevant
    :ivar min_ets_version:
    :ivar original_manufacturer: registration-relevant
    :ivar pre_ets4_style: registration-relevant
    :ivar converted_from_pre_ets4_data: registration-relevant
    :ivar created_from_legacy_schema_version:
    :ivar ipconfig: registration-relevant
    :ivar additional_addresses_count: registration-relevant
    :ivar max_user_entries: registration-relevant
    :ivar max_tunneling_user_entries: registration-relevant
    :ivar max_security_individual_address_entries: registration-relevant
    :ivar max_security_group_key_table_entries: registration-relevant
    :ivar max_security_p2_pkey_table_entries: registration-relevant
    :ivar max_security_proxy_group_key_table_entries: registration-relevant
    :ivar non_reg_relevant_data_version:
    :ivar broken:
    :ivar download_info_incomplete:
    :ivar replaces_versions: registration-relevant
    :ivar hash:
    :ivar internal_description:
    :ivar semantics:
    """

    class Meta:
        name = "ApplicationProgram_t"

    static: ApplicationProgramStatic = field(
        metadata={
            "name": "Static",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        }
    )
    module_defs: None | ApplicationProgramModuleDefs = field(
        default=None,
        metadata={
            "name": "ModuleDefs",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        },
    )
    dynamic: None | ApplicationProgramDynamic = field(
        default=None,
        metadata={
            "name": "Dynamic",
            "type": "Element",
            "namespace": "http://knx.org/xml/project/21",
        },
    )
    id: str = field(
        metadata={
            "name": "Id",
            "type": "Attribute",
        }
    )
    application_number: int = field(
        metadata={
            "name": "ApplicationNumber",
            "type": "Attribute",
        }
    )
    application_version: int = field(
        metadata={
            "name": "ApplicationVersion",
            "type": "Attribute",
        }
    )
    program_type: ApplicationProgramType = field(
        metadata={
            "name": "ProgramType",
            "type": "Attribute",
        }
    )
    mask_version: str = field(
        metadata={
            "name": "MaskVersion",
            "type": "Attribute",
        }
    )
    visible_description: None | str = field(
        default=None,
        metadata={
            "name": "VisibleDescription",
            "type": "Attribute",
        },
    )
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Attribute",
            "max_length": 255,
        }
    )
    load_procedure_style: LoadProcedureStyle = field(
        metadata={
            "name": "LoadProcedureStyle",
            "type": "Attribute",
        }
    )
    pei_type: int = field(
        metadata={
            "name": "PeiType",
            "type": "Attribute",
        }
    )
    hardware_type: None | bytes = field(
        default=None,
        metadata={
            "name": "HardwareType",
            "type": "Attribute",
            "format": "base64",
        },
    )
    help_topic: None | int = field(
        default=None,
        metadata={
            "name": "HelpTopic",
            "type": "Attribute",
        },
    )
    help_file: None | str = field(
        default=None,
        metadata={
            "name": "HelpFile",
            "type": "Attribute",
        },
    )
    context_help_file: None | str = field(
        default=None,
        metadata={
            "name": "ContextHelpFile",
            "type": "Attribute",
        },
    )
    icon_file: None | str = field(
        default=None,
        metadata={
            "name": "IconFile",
            "type": "Attribute",
        },
    )
    default_language: str = field(
        metadata={
            "name": "DefaultLanguage",
            "type": "Attribute",
        }
    )
    dynamic_table_management: bool = field(
        metadata={
            "name": "DynamicTableManagement",
            "type": "Attribute",
        }
    )
    linkable: bool = field(
        metadata={
            "name": "Linkable",
            "type": "Attribute",
        }
    )
    is_secure_enabled: bool = field(
        default=False,
        metadata={
            "name": "IsSecureEnabled",
            "type": "Attribute",
        },
    )
    min_ets_version: None | str = field(
        default=None,
        metadata={
            "name": "MinEtsVersion",
            "type": "Attribute",
        },
    )
    original_manufacturer: None | str = field(
        default=None,
        metadata={
            "name": "OriginalManufacturer",
            "type": "Attribute",
        },
    )
    pre_ets4_style: bool = field(
        default=False,
        metadata={
            "name": "PreEts4Style",
            "type": "Attribute",
        },
    )
    converted_from_pre_ets4_data: bool = field(
        default=False,
        metadata={
            "name": "ConvertedFromPreEts4Data",
            "type": "Attribute",
        },
    )
    created_from_legacy_schema_version: bool = field(
        default=False,
        metadata={
            "name": "CreatedFromLegacySchemaVersion",
            "type": "Attribute",
        },
    )
    ipconfig: ApplicationProgramIpconfig = field(
        default=ApplicationProgramIpconfig.TOOL,
        metadata={
            "name": "IPConfig",
            "type": "Attribute",
        },
    )
    additional_addresses_count: int = field(
        default=0,
        metadata={
            "name": "AdditionalAddressesCount",
            "type": "Attribute",
        },
    )
    max_user_entries: int = field(
        default=0,
        metadata={
            "name": "MaxUserEntries",
            "type": "Attribute",
        },
    )
    max_tunneling_user_entries: int = field(
        default=0,
        metadata={
            "name": "MaxTunnelingUserEntries",
            "type": "Attribute",
        },
    )
    max_security_individual_address_entries: int = field(
        default=0,
        metadata={
            "name": "MaxSecurityIndividualAddressEntries",
            "type": "Attribute",
        },
    )
    max_security_group_key_table_entries: int = field(
        default=0,
        metadata={
            "name": "MaxSecurityGroupKeyTableEntries",
            "type": "Attribute",
        },
    )
    max_security_p2_pkey_table_entries: int = field(
        default=0,
        metadata={
            "name": "MaxSecurityP2PKeyTableEntries",
            "type": "Attribute",
        },
    )
    max_security_proxy_group_key_table_entries: int = field(
        default=0,
        metadata={
            "name": "MaxSecurityProxyGroupKeyTableEntries",
            "type": "Attribute",
        },
    )
    non_reg_relevant_data_version: int = field(
        default=0,
        metadata={
            "name": "NonRegRelevantDataVersion",
            "type": "Attribute",
        },
    )
    broken: bool = field(
        default=False,
        metadata={
            "name": "Broken",
            "type": "Attribute",
        },
    )
    download_info_incomplete: bool = field(
        default=False,
        metadata={
            "name": "DownloadInfoIncomplete",
            "type": "Attribute",
        },
    )
    replaces_versions: list[int] = field(
        default_factory=list,
        metadata={
            "name": "ReplacesVersions",
            "type": "Attribute",
            "tokens": True,
        },
    )
    hash: None | bytes = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Attribute",
            "format": "base64",
        },
    )
    internal_description: None | str = field(
        default=None,
        metadata={
            "name": "InternalDescription",
            "type": "Attribute",
        },
    )
    semantics: None | str = field(
        default=None,
        metadata={
            "name": "Semantics",
            "type": "Attribute",
        },
    )
