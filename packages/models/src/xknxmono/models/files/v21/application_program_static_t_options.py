from __future__ import annotations

from dataclasses import dataclass, field

from xknxmono.models.files.v21.application_program_static_t_options_customer_adjustable_parameters import (
    ApplicationProgramStaticOptionsCustomerAdjustableParameters,
)
from xknxmono.models.files.v21.application_program_static_t_options_not_loadable import (
    ApplicationProgramStaticOptionsNotLoadable,
)
from xknxmono.models.files.v21.application_program_static_t_options_parameter_byte_order import (
    ApplicationProgramStaticOptionsParameterByteOrder,
)
from xknxmono.models.files.v21.application_program_static_t_options_text_parameter_encoding_selector import (
    ApplicationProgramStaticOptionsTextParameterEncodingSelector,
)
from xknxmono.models.files.v21.download_behavior_t import DownloadBehavior
from xknxmono.models.files.v21.text_encoding_t import TextEncoding

__NAMESPACE__ = "http://knx.org/xml/project/21"


@dataclass(slots=True, kw_only=True)
class ApplicationProgramStaticOptions:
    """
    :ivar prefer_partial_download_if_application_loaded:
    :ivar easy_ctrl_mode_mode_style_empty_group_com_tables:
    :ivar set_object_table_length_always_to_one:
    :ivar text_parameter_encoding:
    :ivar text_parameter_encoding_selector:
    :ivar text_parameter_zero_terminate:
    :ivar parameter_byte_order:
    :ivar partial_download_only_visible_parameters:
    :ivar legacy_no_partial_download:
    :ivar legacy_no_memory_verify_mode:
    :ivar legacy_no_optimistic_write:
    :ivar legacy_do_not_report_property_write_errors:
    :ivar legacy_no_background_download:
    :ivar legacy_do_not_check_manufacturer_id:
    :ivar legacy_always_reload_app_if_co_visibility_changed:
    :ivar legacy_never_reload_app_if_co_visibility_changed:
    :ivar legacy_do_not_support_undo_delete:
    :ivar legacy_allow_partial_download_if_ap2_mismatch:
    :ivar legacy_keep_object_table_gaps:
    :ivar legacy_proxy_communication_objects:
    :ivar device_info_ignore_run_state:
    :ivar device_info_ignore_loaded_state:
    :ivar device_compare_allow_compatible_manufacturer_id:
    :ivar line_coupler0912_new_programming_style: registration-relevant
    :ivar max_routing_apdu_length: registration-relevant
    :ivar comparable:
    :ivar reconstructable:
    :ivar download_invisible_parameters:
    :ivar supports_extended_memory_services: registration-relevant
    :ivar supports_extended_property_services: registration-relevant
    :ivar supports_ip_system_broadcast: registration-relevant
    :ivar not_loadable: registration-relevant
    :ivar not_loadable_message_ref:
    :ivar customer_adjustable_parameters: registration-relevant
    :ivar master_reset_on_crcmismatch: registration-relevant
    :ivar prompt_before_full_download:
    :ivar legacy_patch_manufacturer_id_in_task_segment: registration-relevant
    """

    class Meta:
        global_type = False

    prefer_partial_download_if_application_loaded: bool = field(
        default=False,
        metadata={
            "name": "PreferPartialDownloadIfApplicationLoaded",
            "type": "Attribute",
        },
    )
    easy_ctrl_mode_mode_style_empty_group_com_tables: bool = field(
        default=False,
        metadata={
            "name": "EasyCtrlModeModeStyleEmptyGroupComTables",
            "type": "Attribute",
        },
    )
    set_object_table_length_always_to_one: bool = field(
        default=False,
        metadata={
            "name": "SetObjectTableLengthAlwaysToOne",
            "type": "Attribute",
        },
    )
    text_parameter_encoding: None | TextEncoding = field(
        default=None,
        metadata={
            "name": "TextParameterEncoding",
            "type": "Attribute",
        },
    )
    text_parameter_encoding_selector: ApplicationProgramStaticOptionsTextParameterEncodingSelector = field(
        default=ApplicationProgramStaticOptionsTextParameterEncodingSelector.USE_TEXT_PARAMETER_ENCODING_CODE_PAGE,
        metadata={
            "name": "TextParameterEncodingSelector",
            "type": "Attribute",
        },
    )
    text_parameter_zero_terminate: bool = field(
        default=False,
        metadata={
            "name": "TextParameterZeroTerminate",
            "type": "Attribute",
        },
    )
    parameter_byte_order: ApplicationProgramStaticOptionsParameterByteOrder = field(
        default=ApplicationProgramStaticOptionsParameterByteOrder.BIG_ENDIAN,
        metadata={
            "name": "ParameterByteOrder",
            "type": "Attribute",
        },
    )
    partial_download_only_visible_parameters: bool = field(
        default=False,
        metadata={
            "name": "PartialDownloadOnlyVisibleParameters",
            "type": "Attribute",
        },
    )
    legacy_no_partial_download: bool = field(
        default=False,
        metadata={
            "name": "LegacyNoPartialDownload",
            "type": "Attribute",
        },
    )
    legacy_no_memory_verify_mode: bool = field(
        default=False,
        metadata={
            "name": "LegacyNoMemoryVerifyMode",
            "type": "Attribute",
        },
    )
    legacy_no_optimistic_write: bool = field(
        default=False,
        metadata={
            "name": "LegacyNoOptimisticWrite",
            "type": "Attribute",
        },
    )
    legacy_do_not_report_property_write_errors: bool = field(
        default=False,
        metadata={
            "name": "LegacyDoNotReportPropertyWriteErrors",
            "type": "Attribute",
        },
    )
    legacy_no_background_download: bool = field(
        default=False,
        metadata={
            "name": "LegacyNoBackgroundDownload",
            "type": "Attribute",
        },
    )
    legacy_do_not_check_manufacturer_id: bool = field(
        default=False,
        metadata={
            "name": "LegacyDoNotCheckManufacturerId",
            "type": "Attribute",
        },
    )
    legacy_always_reload_app_if_co_visibility_changed: bool = field(
        default=False,
        metadata={
            "name": "LegacyAlwaysReloadAppIfCoVisibilityChanged",
            "type": "Attribute",
        },
    )
    legacy_never_reload_app_if_co_visibility_changed: bool = field(
        default=False,
        metadata={
            "name": "LegacyNeverReloadAppIfCoVisibilityChanged",
            "type": "Attribute",
        },
    )
    legacy_do_not_support_undo_delete: bool = field(
        default=False,
        metadata={
            "name": "LegacyDoNotSupportUndoDelete",
            "type": "Attribute",
        },
    )
    legacy_allow_partial_download_if_ap2_mismatch: bool = field(
        default=False,
        metadata={
            "name": "LegacyAllowPartialDownloadIfAp2Mismatch",
            "type": "Attribute",
        },
    )
    legacy_keep_object_table_gaps: bool = field(
        default=False,
        metadata={
            "name": "LegacyKeepObjectTableGaps",
            "type": "Attribute",
        },
    )
    legacy_proxy_communication_objects: bool = field(
        default=False,
        metadata={
            "name": "LegacyProxyCommunicationObjects",
            "type": "Attribute",
        },
    )
    device_info_ignore_run_state: bool = field(
        default=False,
        metadata={
            "name": "DeviceInfoIgnoreRunState",
            "type": "Attribute",
        },
    )
    device_info_ignore_loaded_state: bool = field(
        default=False,
        metadata={
            "name": "DeviceInfoIgnoreLoadedState",
            "type": "Attribute",
        },
    )
    device_compare_allow_compatible_manufacturer_id: bool = field(
        default=False,
        metadata={
            "name": "DeviceCompareAllowCompatibleManufacturerId",
            "type": "Attribute",
        },
    )
    line_coupler0912_new_programming_style: bool = field(
        default=False,
        metadata={
            "name": "LineCoupler0912NewProgrammingStyle",
            "type": "Attribute",
        },
    )
    max_routing_apdu_length: None | int = field(
        default=None,
        metadata={
            "name": "MaxRoutingApduLength",
            "type": "Attribute",
        },
    )
    comparable: None | bool = field(
        default=None,
        metadata={
            "name": "Comparable",
            "type": "Attribute",
        },
    )
    reconstructable: None | bool = field(
        default=None,
        metadata={
            "name": "Reconstructable",
            "type": "Attribute",
        },
    )
    download_invisible_parameters: DownloadBehavior = field(
        default=DownloadBehavior.DEFAULT_VALUE,
        metadata={
            "name": "DownloadInvisibleParameters",
            "type": "Attribute",
        },
    )
    supports_extended_memory_services: bool = field(
        default=False,
        metadata={
            "name": "SupportsExtendedMemoryServices",
            "type": "Attribute",
        },
    )
    supports_extended_property_services: bool = field(
        default=False,
        metadata={
            "name": "SupportsExtendedPropertyServices",
            "type": "Attribute",
        },
    )
    supports_ip_system_broadcast: bool = field(
        default=False,
        metadata={
            "name": "SupportsIpSystemBroadcast",
            "type": "Attribute",
        },
    )
    not_loadable: None | ApplicationProgramStaticOptionsNotLoadable = field(
        default=None,
        metadata={
            "name": "NotLoadable",
            "type": "Attribute",
        },
    )
    not_loadable_message_ref: None | str = field(
        default=None,
        metadata={
            "name": "NotLoadableMessageRef",
            "type": "Attribute",
        },
    )
    customer_adjustable_parameters: (
        None | ApplicationProgramStaticOptionsCustomerAdjustableParameters
    ) = field(
        default=None,
        metadata={
            "name": "CustomerAdjustableParameters",
            "type": "Attribute",
        },
    )
    master_reset_on_crcmismatch: bool = field(
        default=False,
        metadata={
            "name": "MasterResetOnCRCMismatch",
            "type": "Attribute",
        },
    )
    prompt_before_full_download: bool = field(
        default=False,
        metadata={
            "name": "PromptBeforeFullDownload",
            "type": "Attribute",
        },
    )
    legacy_patch_manufacturer_id_in_task_segment: bool = field(
        default=False,
        metadata={
            "name": "LegacyPatchManufacturerIdInTaskSegment",
            "type": "Attribute",
        },
    )
