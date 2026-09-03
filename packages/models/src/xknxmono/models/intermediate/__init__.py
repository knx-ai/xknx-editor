from __future__ import annotations

from typing import TYPE_CHECKING

_LAZY: dict[str, tuple[str, str]] = {
    "Access": ("xknxmono.models.intermediate.access_t", "Access"),
    "AddinData": ("xknxmono.models.intermediate.addin_data_t", "AddinData"),
    "Allocator": ("xknxmono.models.intermediate.allocator_t", "Allocator"),
    "ApplicationProgramChannel": ("xknxmono.models.intermediate.application_program_channel_t", "ApplicationProgramChannel"),
    "ChannelChoose": ("xknxmono.models.intermediate.application_program_channel_t", "ChannelChoose"),
    "ChannelChooseWhen": ("xknxmono.models.intermediate.application_program_channel_t", "ChannelChooseWhen"),
    "ComObjectParameterBlock": ("xknxmono.models.intermediate.application_program_channel_t", "ComObjectParameterBlock"),
    "ComObjectParameterChoose": ("xknxmono.models.intermediate.application_program_channel_t", "ComObjectParameterChoose"),
    "ComObjectParameterChooseWhen": ("xknxmono.models.intermediate.application_program_channel_t", "ComObjectParameterChooseWhen"),
    "Repeat": ("xknxmono.models.intermediate.application_program_channel_t", "Repeat"),
    "ApplicationProgramDynamic": ("xknxmono.models.intermediate.application_program_dynamic_t", "ApplicationProgramDynamic"),
    "ApplicationProgramIpconfig": ("xknxmono.models.intermediate.application_program_ipconfig_t", "ApplicationProgramIpconfig"),
    "ApplicationProgramRef": ("xknxmono.models.intermediate.application_program_ref_t", "ApplicationProgramRef"),
    "ApplicationProgramStatic": ("xknxmono.models.intermediate.application_program_static_t", "ApplicationProgramStatic"),
    "ApplicationProgramStaticAddressTable": ("xknxmono.models.intermediate.application_program_static_t_address_table", "ApplicationProgramStaticAddressTable"),
    "ApplicationProgramStaticAllocators": ("xknxmono.models.intermediate.application_program_static_t_allocators", "ApplicationProgramStaticAllocators"),
    "ApplicationProgramStaticAssociationTable": ("xknxmono.models.intermediate.application_program_static_t_association_table", "ApplicationProgramStaticAssociationTable"),
    "ApplicationProgramStaticBinaryData": ("xknxmono.models.intermediate.application_program_static_t_binary_data", "ApplicationProgramStaticBinaryData"),
    "ApplicationProgramStaticBusInterfaces": ("xknxmono.models.intermediate.application_program_static_t_bus_interfaces", "ApplicationProgramStaticBusInterfaces"),
    "ApplicationProgramStaticBusInterfacesBusInterface": ("xknxmono.models.intermediate.application_program_static_t_bus_interfaces_bus_interface", "ApplicationProgramStaticBusInterfacesBusInterface"),
    "ApplicationProgramStaticBusInterfacesBusInterfaceAccessType": ("xknxmono.models.intermediate.application_program_static_t_bus_interfaces_bus_interface_access_type", "ApplicationProgramStaticBusInterfacesBusInterfaceAccessType"),
    "ApplicationProgramStaticCode": ("xknxmono.models.intermediate.application_program_static_t_code", "ApplicationProgramStaticCode"),
    "ApplicationProgramStaticCodeAbsoluteSegment": ("xknxmono.models.intermediate.application_program_static_t_code_absolute_segment", "ApplicationProgramStaticCodeAbsoluteSegment"),
    "ApplicationProgramStaticCodeRelativeSegment": ("xknxmono.models.intermediate.application_program_static_t_code_relative_segment", "ApplicationProgramStaticCodeRelativeSegment"),
    "ApplicationProgramStaticComObjectRefs": ("xknxmono.models.intermediate.application_program_static_t_com_object_refs", "ApplicationProgramStaticComObjectRefs"),
    "ApplicationProgramStaticComObjectTable": ("xknxmono.models.intermediate.application_program_static_t_com_object_table", "ApplicationProgramStaticComObjectTable"),
    "ApplicationProgramStaticDeviceCompare": ("xknxmono.models.intermediate.application_program_static_t_device_compare", "ApplicationProgramStaticDeviceCompare"),
    "ApplicationProgramStaticDeviceCompareExcludeMemory": ("xknxmono.models.intermediate.application_program_static_t_device_compare_exclude_memory", "ApplicationProgramStaticDeviceCompareExcludeMemory"),
    "ApplicationProgramStaticDeviceCompareExcludeProperty": ("xknxmono.models.intermediate.application_program_static_t_device_compare_exclude_property", "ApplicationProgramStaticDeviceCompareExcludeProperty"),
    "ApplicationProgramStaticExtension": ("xknxmono.models.intermediate.application_program_static_t_extension", "ApplicationProgramStaticExtension"),
    "ApplicationProgramStaticExtensionBaggage": ("xknxmono.models.intermediate.application_program_static_t_extension_baggage", "ApplicationProgramStaticExtensionBaggage"),
    "ApplicationProgramStaticFixupList": ("xknxmono.models.intermediate.application_program_static_t_fixup_list", "ApplicationProgramStaticFixupList"),
    "ApplicationProgramStaticMessages": ("xknxmono.models.intermediate.application_program_static_t_messages", "ApplicationProgramStaticMessages"),
    "ApplicationProgramStaticMessagesMessage": ("xknxmono.models.intermediate.application_program_static_t_messages_message", "ApplicationProgramStaticMessagesMessage"),
    "ApplicationProgramStaticOptions": ("xknxmono.models.intermediate.application_program_static_t_options", "ApplicationProgramStaticOptions"),
    "ApplicationProgramStaticOptionsCustomerAdjustableParameters": ("xknxmono.models.intermediate.application_program_static_t_options_customer_adjustable_parameters", "ApplicationProgramStaticOptionsCustomerAdjustableParameters"),
    "ApplicationProgramStaticOptionsNotLoadable": ("xknxmono.models.intermediate.application_program_static_t_options_not_loadable", "ApplicationProgramStaticOptionsNotLoadable"),
    "ApplicationProgramStaticOptionsParameterByteOrder": ("xknxmono.models.intermediate.application_program_static_t_options_parameter_byte_order", "ApplicationProgramStaticOptionsParameterByteOrder"),
    "TextEncodingSelector": ("xknxmono.models.intermediate.application_program_static_t_options_text_parameter_encoding_selector", "TextEncodingSelector"),
    "ApplicationProgramStaticParameterCalculations": ("xknxmono.models.intermediate.application_program_static_t_parameter_calculations", "ApplicationProgramStaticParameterCalculations"),
    "ApplicationProgramStaticParameterRefs": ("xknxmono.models.intermediate.application_program_static_t_parameter_refs", "ApplicationProgramStaticParameterRefs"),
    "ApplicationProgramStaticParameterTypes": ("xknxmono.models.intermediate.application_program_static_t_parameter_types", "ApplicationProgramStaticParameterTypes"),
    "ApplicationProgramStaticParameterValidations": ("xknxmono.models.intermediate.application_program_static_t_parameter_validations", "ApplicationProgramStaticParameterValidations"),
    "ApplicationProgramStaticParameters": ("xknxmono.models.intermediate.application_program_static_t_parameters", "ApplicationProgramStaticParameters"),
    "ApplicationProgramStaticParametersParameter": ("xknxmono.models.intermediate.application_program_static_t_parameters_parameter", "ApplicationProgramStaticParametersParameter"),
    "ApplicationProgramStaticParametersUnion": ("xknxmono.models.intermediate.application_program_static_t_parameters_union", "ApplicationProgramStaticParametersUnion"),
    "ApplicationProgramStaticScript": ("xknxmono.models.intermediate.application_program_static_t_script", "ApplicationProgramStaticScript"),
    "ApplicationProgramStaticSecurityRoles": ("xknxmono.models.intermediate.application_program_static_t_security_roles", "ApplicationProgramStaticSecurityRoles"),
    "ApplicationProgramStaticSecurityRolesSecurityRole": ("xknxmono.models.intermediate.application_program_static_t_security_roles_security_role", "ApplicationProgramStaticSecurityRolesSecurityRole"),
    "ApplicationProgram": ("xknxmono.models.intermediate.application_program_t", "ApplicationProgram"),
    "ApplicationProgramCloudConnect": ("xknxmono.models.intermediate.application_program_t_cloud_connect", "ApplicationProgramCloudConnect"),
    "ApplicationProgramMinEtsVersion": ("xknxmono.models.intermediate.application_program_t_min_ets_version", "ApplicationProgramMinEtsVersion"),
    "ApplicationProgramModuleDefs": ("xknxmono.models.intermediate.application_program_t_module_defs", "ApplicationProgramModuleDefs"),
    "ApplicationProgramProfile": ("xknxmono.models.intermediate.application_program_t_profile", "ApplicationProgramProfile"),
    "ApplicationProgramProfileIo": ("xknxmono.models.intermediate.application_program_t_profile_io_t", "ApplicationProgramProfileIo"),
    "ApplicationProgramType": ("xknxmono.models.intermediate.application_program_type_t", "ApplicationProgramType"),
    "Assign": ("xknxmono.models.intermediate.assign_t", "Assign"),
    "BinaryDataRef": ("xknxmono.models.intermediate.binary_data_ref_t", "BinaryDataRef"),
    "BinaryData": ("xknxmono.models.intermediate.binary_data_t", "BinaryData"),
    "BusAccess": ("xknxmono.models.intermediate.bus_access_t", "BusAccess"),
    "BusInterface": ("xknxmono.models.intermediate.bus_interface_t", "BusInterface"),
    "BusInterfaceConnectors": ("xknxmono.models.intermediate.bus_interface_t_connectors", "BusInterfaceConnectors"),
    "BusInterfaceConnectorsConnector": ("xknxmono.models.intermediate.bus_interface_t_connectors_connector", "BusInterfaceConnectorsConnector"),
    "Button": ("xknxmono.models.intermediate.button_t", "Button"),
    "ButtonEventHandlerOnline": ("xknxmono.models.intermediate.button_t_event_handler_online", "ButtonEventHandlerOnline"),
    "CalculationParameterRef": ("xknxmono.models.intermediate.calculation_parameter_ref_t", "CalculationParameterRef"),
    "Capability": ("xknxmono.models.intermediate.capability_t", "Capability"),
    "CatalogSection": ("xknxmono.models.intermediate.catalog_section_t", "CatalogSection"),
    "CatalogSectionCatalogItem": ("xknxmono.models.intermediate.catalog_section_t_catalog_item", "CatalogSectionCatalogItem"),
    "ChannelIndependentBlock": ("xknxmono.models.intermediate.channel_independent_block_t", "ChannelIndependentBlock"),
    "ChannelInstance": ("xknxmono.models.intermediate.channel_instance_t", "ChannelInstance"),
    "ComObjectInstanceRef": ("xknxmono.models.intermediate.com_object_instance_ref_t", "ComObjectInstanceRef"),
    "ComObjectParameterBlockColumns": ("xknxmono.models.intermediate.com_object_parameter_block_t_columns", "ComObjectParameterBlockColumns"),
    "ComObjectParameterBlockColumnsColumn": ("xknxmono.models.intermediate.com_object_parameter_block_t_columns_column", "ComObjectParameterBlockColumnsColumn"),
    "ComObjectParameterBlockRows": ("xknxmono.models.intermediate.com_object_parameter_block_t_rows", "ComObjectParameterBlockRows"),
    "ComObjectParameterBlockRowsRow": ("xknxmono.models.intermediate.com_object_parameter_block_t_rows_row", "ComObjectParameterBlockRowsRow"),
    "ComObjectPriority": ("xknxmono.models.intermediate.com_object_priority_t", "ComObjectPriority"),
    "ComObjectRefRef": ("xknxmono.models.intermediate.com_object_ref_ref_t", "ComObjectRefRef"),
    "ComObjectRef": ("xknxmono.models.intermediate.com_object_ref_t", "ComObjectRef"),
    "ComObjectSecurityRequirements": ("xknxmono.models.intermediate.com_object_security_requirements_t", "ComObjectSecurityRequirements"),
    "ComObjectSize": ("xknxmono.models.intermediate.com_object_size_t", "ComObjectSize"),
    "ComObject": ("xknxmono.models.intermediate.com_object_t", "ComObject"),
    "ComTableExpectation": ("xknxmono.models.intermediate.com_table_expectation_t", "ComTableExpectation"),
    "CompletionStatus": ("xknxmono.models.intermediate.completion_status_t", "CompletionStatus"),
    "CouplerCapability": ("xknxmono.models.intermediate.coupler_capability_t", "CouplerCapability"),
    "DatapointRole": ("xknxmono.models.intermediate.datapoint_role_t", "DatapointRole"),
    "DatapointType": ("xknxmono.models.intermediate.datapoint_type_t", "DatapointType"),
    "DatapointTypeDatapointSubtypes": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes", "DatapointTypeDatapointSubtypes"),
    "DatapointTypeDatapointSubtypesDatapointSubtype": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype", "DatapointTypeDatapointSubtypesDatapointSubtype"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormat": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format", "DatapointTypeDatapointSubtypesDatapointSubtypeFormat"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_bit", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumerationEnumValue": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration_enum_value", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumerationEnumValue"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_float", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_ref_type", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_reserved", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_signed_integer", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatString": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_string", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatString"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger": ("xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_unsigned_integer", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger"),
    "DependentChannelChoose": ("xknxmono.models.intermediate.dependent_channel_choose_t", "DependentChannelChoose"),
    "DependentChannelChooseWhen": ("xknxmono.models.intermediate.dependent_channel_choose_t", "DependentChannelChooseWhen"),
    "DeprecationStatus": ("xknxmono.models.intermediate.deprecation_status_t", "DeprecationStatus"),
    "DeviceCertificate": ("xknxmono.models.intermediate.device_certificate_t", "DeviceCertificate"),
    "DeviceInstanceRef": ("xknxmono.models.intermediate.device_instance_ref_t", "DeviceInstanceRef"),
    "DeviceInstance": ("xknxmono.models.intermediate.device_instance_t", "DeviceInstance"),
    "DeviceInstanceAdditionalAddresses": ("xknxmono.models.intermediate.device_instance_t_additional_addresses", "DeviceInstanceAdditionalAddresses"),
    "DeviceInstanceAdditionalAddressesAddress": ("xknxmono.models.intermediate.device_instance_t_additional_addresses_address", "DeviceInstanceAdditionalAddressesAddress"),
    "DeviceInstanceBinaryData": ("xknxmono.models.intermediate.device_instance_t_binary_data", "DeviceInstanceBinaryData"),
    "DeviceInstanceBinaryDataBinaryData": ("xknxmono.models.intermediate.device_instance_t_binary_data_binary_data", "DeviceInstanceBinaryDataBinaryData"),
    "DeviceInstanceBusInterfaces": ("xknxmono.models.intermediate.device_instance_t_bus_interfaces", "DeviceInstanceBusInterfaces"),
    "DeviceInstanceChannelInstances": ("xknxmono.models.intermediate.device_instance_t_channel_instances", "DeviceInstanceChannelInstances"),
    "DeviceInstanceComObjectInstanceRefs": ("xknxmono.models.intermediate.device_instance_t_com_object_instance_refs", "DeviceInstanceComObjectInstanceRefs"),
    "DeviceInstanceGroupObjectTree": ("xknxmono.models.intermediate.device_instance_t_group_object_tree", "DeviceInstanceGroupObjectTree"),
    "DeviceInstanceGroupObjectTreeNodes": ("xknxmono.models.intermediate.device_instance_t_group_object_tree_nodes", "DeviceInstanceGroupObjectTreeNodes"),
    "DeviceInstanceModuleInstances": ("xknxmono.models.intermediate.device_instance_t_module_instances", "DeviceInstanceModuleInstances"),
    "DeviceInstanceParameterInstanceRefs": ("xknxmono.models.intermediate.device_instance_t_parameter_instance_refs", "DeviceInstanceParameterInstanceRefs"),
    "DeviceInstanceRfFastAckSlots": ("xknxmono.models.intermediate.device_instance_t_rf_fast_ack_slots", "DeviceInstanceRfFastAckSlots"),
    "DeviceInstanceRfFastAckSlotsSlot": ("xknxmono.models.intermediate.device_instance_t_rf_fast_ack_slots_slot", "DeviceInstanceRfFastAckSlotsSlot"),
    "DownloadBehavior": ("xknxmono.models.intermediate.download_behavior_t", "DownloadBehavior"),
    "Enable": ("xknxmono.models.intermediate.enable_t", "Enable"),
    "Fixup": ("xknxmono.models.intermediate.fixup_t", "Fixup"),
    "Function": ("xknxmono.models.intermediate.function_t", "Function"),
    "FunctionType": ("xknxmono.models.intermediate.function_type_t", "FunctionType"),
    "FunctionTypeFunctionPoint": ("xknxmono.models.intermediate.function_type_t_function_point", "FunctionTypeFunctionPoint"),
    "FunctionsGroup": ("xknxmono.models.intermediate.functions_group_t", "FunctionsGroup"),
    "GroupAddressRef": ("xknxmono.models.intermediate.group_address_ref_t", "GroupAddressRef"),
    "GroupAddressStyle": ("xknxmono.models.intermediate.group_address_style_t", "GroupAddressStyle"),
    "GroupAddress": ("xknxmono.models.intermediate.group_address_t", "GroupAddress"),
    "GroupAddresses": ("xknxmono.models.intermediate.group_addresses_t", "GroupAddresses"),
    "GroupAddressesGroupRanges": ("xknxmono.models.intermediate.group_addresses_t_group_ranges", "GroupAddressesGroupRanges"),
    "GroupRange": ("xknxmono.models.intermediate.group_range_t", "GroupRange"),
    "Hardware2Program": ("xknxmono.models.intermediate.hardware2_program_t", "Hardware2Program"),
    "Hardware": ("xknxmono.models.intermediate.hardware_t", "Hardware"),
    "HardwareHardware2Programs": ("xknxmono.models.intermediate.hardware_t_hardware2_programs", "HardwareHardware2Programs"),
    "HardwareProducts": ("xknxmono.models.intermediate.hardware_t_products", "HardwareProducts"),
    "HardwareProductsProduct": ("xknxmono.models.intermediate.hardware_t_products_product", "HardwareProductsProduct"),
    "HardwareProductsProductAttributes": ("xknxmono.models.intermediate.hardware_t_products_product_attributes", "HardwareProductsProductAttributes"),
    "HardwareProductsProductAttributesAttribute": ("xknxmono.models.intermediate.hardware_t_products_product_attributes_attribute", "HardwareProductsProductAttributesAttribute"),
    "HardwareProductsProductAttributesAttributeName": ("xknxmono.models.intermediate.hardware_t_products_product_attributes_attribute_name", "HardwareProductsProductAttributesAttributeName"),
    "HardwareProductsProductBaggages": ("xknxmono.models.intermediate.hardware_t_products_product_baggages", "HardwareProductsProductBaggages"),
    "HardwareProductsProductBaggagesBaggage": ("xknxmono.models.intermediate.hardware_t_products_product_baggages_baggage", "HardwareProductsProductBaggagesBaggage"),
    "HawkConfigurationData": ("xknxmono.models.intermediate.hawk_configuration_data_t", "HawkConfigurationData"),
    "HawkConfigurationDataFeatures": ("xknxmono.models.intermediate.hawk_configuration_data_t_features", "HawkConfigurationDataFeatures"),
    "HawkConfigurationDataFeaturesFeature": ("xknxmono.models.intermediate.hawk_configuration_data_t_features_feature", "HawkConfigurationDataFeaturesFeature"),
    "HawkConfigurationDataFeaturesFeatureName": ("xknxmono.models.intermediate.hawk_configuration_data_t_features_feature_name", "HawkConfigurationDataFeaturesFeatureName"),
    "HawkConfigurationDataInterfaceObjects": ("xknxmono.models.intermediate.hawk_configuration_data_t_interface_objects", "HawkConfigurationDataInterfaceObjects"),
    "HawkConfigurationDataInterfaceObjectsInterfaceObject": ("xknxmono.models.intermediate.hawk_configuration_data_t_interface_objects_interface_object", "HawkConfigurationDataInterfaceObjectsInterfaceObject"),
    "HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty": ("xknxmono.models.intermediate.hawk_configuration_data_t_interface_objects_interface_object_property", "HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty"),
    "HawkConfigurationDataMemorySegments": ("xknxmono.models.intermediate.hawk_configuration_data_t_memory_segments", "HawkConfigurationDataMemorySegments"),
    "HawkConfigurationDataMemorySegmentsMemorySegment": ("xknxmono.models.intermediate.hawk_configuration_data_t_memory_segments_memory_segment", "HawkConfigurationDataMemorySegmentsMemorySegment"),
    "HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights": ("xknxmono.models.intermediate.hawk_configuration_data_t_memory_segments_memory_segment_access_rights", "HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights"),
    "HawkConfigurationDataProcedures": ("xknxmono.models.intermediate.hawk_configuration_data_t_procedures", "HawkConfigurationDataProcedures"),
    "HawkConfigurationDataProceduresProcedure": ("xknxmono.models.intermediate.hawk_configuration_data_t_procedures_procedure", "HawkConfigurationDataProceduresProcedure"),
    "HawkConfigurationDataProceduresProcedureValue": ("xknxmono.models.intermediate.hawk_configuration_data_t_procedures_procedure_value", "HawkConfigurationDataProceduresProcedureValue"),
    "HawkConfigurationDataResources": ("xknxmono.models.intermediate.hawk_configuration_data_t_resources", "HawkConfigurationDataResources"),
    "HawkConfigurationDataResourcesResource": ("xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource", "HawkConfigurationDataResourcesResource"),
    "HawkConfigurationDataResourcesResourceAccessRights": ("xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource_access_rights", "HawkConfigurationDataResourcesResourceAccessRights"),
    "HawkConfigurationDataResourcesResourceResourceType": ("xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource_resource_type", "HawkConfigurationDataResourcesResourceResourceType"),
    "HawkConfigurationDataResourcesResourceResourceTypeFlavour": ("xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource_resource_type_flavour", "HawkConfigurationDataResourcesResourceResourceTypeFlavour"),
    "HorizontalAlignment": ("xknxmono.models.intermediate.horizontal_alignment_t", "HorizontalAlignment"),
    "IoPointParameter": ("xknxmono.models.intermediate.io_tpoint_parameter_t", "IoPointParameter"),
    "IpconfigAssign": ("xknxmono.models.intermediate.ipconfig_assign_t", "IpconfigAssign"),
    "Ipconfig": ("xknxmono.models.intermediate.ipconfig_t", "Ipconfig"),
    "Knx": ("xknxmono.models.intermediate.knx", "Knx"),
    "LanguageData": ("xknxmono.models.intermediate.language_data_t", "LanguageData"),
    "LanguageDataTranslationUnit": ("xknxmono.models.intermediate.language_data_t_translation_unit", "LanguageDataTranslationUnit"),
    "LanguageDataTranslationUnitTranslationElement": ("xknxmono.models.intermediate.language_data_t_translation_unit_translation_element", "LanguageDataTranslationUnitTranslationElement"),
    "LanguageDataTranslationUnitTranslationElementTranslation": ("xknxmono.models.intermediate.language_data_t_translation_unit_translation_element_translation", "LanguageDataTranslationUnitTranslationElementTranslation"),
    "LdCtrlAbsSegment": ("xknxmono.models.intermediate.ld_ctrl_abs_segment_t", "LdCtrlAbsSegment"),
    "LdCtrlBaseChoose": ("xknxmono.models.intermediate.ld_ctrl_base_choose_t", "LdCtrlBaseChoose"),
    "LdCtrlBaseChooseWhen": ("xknxmono.models.intermediate.ld_ctrl_base_choose_t", "LdCtrlBaseChooseWhen"),
    "LdCtrlBase": ("xknxmono.models.intermediate.ld_ctrl_base_t", "LdCtrlBase"),
    "LdCtrlBaseOnError": ("xknxmono.models.intermediate.ld_ctrl_base_t_on_error", "LdCtrlBaseOnError"),
    "LdCtrlClearCachedObjectTypes": ("xknxmono.models.intermediate.ld_ctrl_clear_cached_object_types_t", "LdCtrlClearCachedObjectTypes"),
    "LdCtrlClearLcfilterTable": ("xknxmono.models.intermediate.ld_ctrl_clear_lcfilter_table_t", "LdCtrlClearLcfilterTable"),
    "LdCtrlCompareBase": ("xknxmono.models.intermediate.ld_ctrl_compare_base_t", "LdCtrlCompareBase"),
    "LdCtrlCompareMem": ("xknxmono.models.intermediate.ld_ctrl_compare_mem_t", "LdCtrlCompareMem"),
    "LdCtrlCompareProp": ("xknxmono.models.intermediate.ld_ctrl_compare_prop_t", "LdCtrlCompareProp"),
    "LdCtrlCompareRelMem": ("xknxmono.models.intermediate.ld_ctrl_compare_rel_mem_t", "LdCtrlCompareRelMem"),
    "LdCtrlConnect": ("xknxmono.models.intermediate.ld_ctrl_connect_t", "LdCtrlConnect"),
    "LdCtrlControlVariable": ("xknxmono.models.intermediate.ld_ctrl_control_variable_t", "LdCtrlControlVariable"),
    "LdCtrlDeclarePropDesc": ("xknxmono.models.intermediate.ld_ctrl_declare_prop_desc_t", "LdCtrlDeclarePropDesc"),
    "LdCtrlDelay": ("xknxmono.models.intermediate.ld_ctrl_delay_t", "LdCtrlDelay"),
    "LdCtrlDisconnect": ("xknxmono.models.intermediate.ld_ctrl_disconnect_t", "LdCtrlDisconnect"),
    "LdCtrlErrorCause": ("xknxmono.models.intermediate.ld_ctrl_error_cause_t", "LdCtrlErrorCause"),
    "LdCtrlInvokeFunctionProp": ("xknxmono.models.intermediate.ld_ctrl_invoke_function_prop_t", "LdCtrlInvokeFunctionProp"),
    "LdCtrlLoadCompleted": ("xknxmono.models.intermediate.ld_ctrl_load_completed_t", "LdCtrlLoadCompleted"),
    "LdCtrlLoadImageMem": ("xknxmono.models.intermediate.ld_ctrl_load_image_mem_t", "LdCtrlLoadImageMem"),
    "LdCtrlLoadImageProp": ("xknxmono.models.intermediate.ld_ctrl_load_image_prop_t", "LdCtrlLoadImageProp"),
    "LdCtrlLoadImageRelMem": ("xknxmono.models.intermediate.ld_ctrl_load_image_rel_mem_t", "LdCtrlLoadImageRelMem"),
    "LdCtrlLoad": ("xknxmono.models.intermediate.ld_ctrl_load_t", "LdCtrlLoad"),
    "LdCtrlMapError": ("xknxmono.models.intermediate.ld_ctrl_map_error_t", "LdCtrlMapError"),
    "LdCtrlMasterReset": ("xknxmono.models.intermediate.ld_ctrl_master_reset_t", "LdCtrlMasterReset"),
    "LdCtrlMaxLength": ("xknxmono.models.intermediate.ld_ctrl_max_length_t", "LdCtrlMaxLength"),
    "LdCtrlMemAddrSpace": ("xknxmono.models.intermediate.ld_ctrl_mem_addr_space_t", "LdCtrlMemAddrSpace"),
    "LdCtrlMerge": ("xknxmono.models.intermediate.ld_ctrl_merge_t", "LdCtrlMerge"),
    "LdCtrlProcType": ("xknxmono.models.intermediate.ld_ctrl_proc_type_t", "LdCtrlProcType"),
    "LdCtrlProgressText": ("xknxmono.models.intermediate.ld_ctrl_progress_text_t", "LdCtrlProgressText"),
    "LdCtrlReadFunctionProp": ("xknxmono.models.intermediate.ld_ctrl_read_function_prop_t", "LdCtrlReadFunctionProp"),
    "LdCtrlRelSegment": ("xknxmono.models.intermediate.ld_ctrl_rel_segment_t", "LdCtrlRelSegment"),
    "LdCtrlRestart": ("xknxmono.models.intermediate.ld_ctrl_restart_t", "LdCtrlRestart"),
    "LdCtrlSetControlVariable": ("xknxmono.models.intermediate.ld_ctrl_set_control_variable_t", "LdCtrlSetControlVariable"),
    "LdCtrlTaskCtrl1": ("xknxmono.models.intermediate.ld_ctrl_task_ctrl1_t", "LdCtrlTaskCtrl1"),
    "LdCtrlTaskCtrl2": ("xknxmono.models.intermediate.ld_ctrl_task_ctrl2_t", "LdCtrlTaskCtrl2"),
    "LdCtrlTaskPtr": ("xknxmono.models.intermediate.ld_ctrl_task_ptr_t", "LdCtrlTaskPtr"),
    "LdCtrlTaskSegment": ("xknxmono.models.intermediate.ld_ctrl_task_segment_t", "LdCtrlTaskSegment"),
    "LdCtrlUnload": ("xknxmono.models.intermediate.ld_ctrl_unload_t", "LdCtrlUnload"),
    "LdCtrlWriteMem": ("xknxmono.models.intermediate.ld_ctrl_write_mem_t", "LdCtrlWriteMem"),
    "LdCtrlWriteProp": ("xknxmono.models.intermediate.ld_ctrl_write_prop_t", "LdCtrlWriteProp"),
    "LdCtrlWriteRelMem": ("xknxmono.models.intermediate.ld_ctrl_write_rel_mem_t", "LdCtrlWriteRelMem"),
    "LoadProcedureStyle": ("xknxmono.models.intermediate.load_procedure_style_t", "LoadProcedureStyle"),
    "LoadProcedure": ("xknxmono.models.intermediate.load_procedure_t", "LoadProcedure"),
    "LoadProcedures": ("xknxmono.models.intermediate.load_procedures_t", "LoadProcedures"),
    "LoadProceduresLoadProcedure": ("xknxmono.models.intermediate.load_procedures_t_load_procedure", "LoadProceduresLoadProcedure"),
    "Locations": ("xknxmono.models.intermediate.locations_t", "Locations"),
    "ManufacturerData": ("xknxmono.models.intermediate.manufacturer_data_t", "ManufacturerData"),
    "ManufacturerDataManufacturer": ("xknxmono.models.intermediate.manufacturer_data_t_manufacturer", "ManufacturerDataManufacturer"),
    "ManufacturerDataManufacturerApplicationPrograms": ("xknxmono.models.intermediate.manufacturer_data_t_manufacturer_application_programs", "ManufacturerDataManufacturerApplicationPrograms"),
    "ManufacturerDataManufacturerBaggages": ("xknxmono.models.intermediate.manufacturer_data_t_manufacturer_baggages", "ManufacturerDataManufacturerBaggages"),
    "ManufacturerDataManufacturerBaggagesBaggage": ("xknxmono.models.intermediate.manufacturer_data_t_manufacturer_baggages_baggage", "ManufacturerDataManufacturerBaggagesBaggage"),
    "ManufacturerDataManufacturerBaggagesBaggageFileInfo": ("xknxmono.models.intermediate.manufacturer_data_t_manufacturer_baggages_baggage_file_info", "ManufacturerDataManufacturerBaggagesBaggageFileInfo"),
    "ManufacturerDataManufacturerCatalog": ("xknxmono.models.intermediate.manufacturer_data_t_manufacturer_catalog", "ManufacturerDataManufacturerCatalog"),
    "ManufacturerDataManufacturerHardware": ("xknxmono.models.intermediate.manufacturer_data_t_manufacturer_hardware", "ManufacturerDataManufacturerHardware"),
    "ManufacturerDataManufacturerLanguages": ("xknxmono.models.intermediate.manufacturer_data_t_manufacturer_languages", "ManufacturerDataManufacturerLanguages"),
    "MaskVersion": ("xknxmono.models.intermediate.mask_version_t", "MaskVersion"),
    "MaskVersionDownwardCompatibleMasks": ("xknxmono.models.intermediate.mask_version_t_downward_compatible_masks", "MaskVersionDownwardCompatibleMasks"),
    "MaskVersionDownwardCompatibleMasksDownwardCompatibleMask": ("xknxmono.models.intermediate.mask_version_t_downward_compatible_masks_downward_compatible_mask", "MaskVersionDownwardCompatibleMasksDownwardCompatibleMask"),
    "MaskVersionManagementModel": ("xknxmono.models.intermediate.mask_version_t_management_model", "MaskVersionManagementModel"),
    "MaskVersionMaskEntries": ("xknxmono.models.intermediate.mask_version_t_mask_entries", "MaskVersionMaskEntries"),
    "MaskVersionMaskEntriesMaskEntry": ("xknxmono.models.intermediate.mask_version_t_mask_entries_mask_entry", "MaskVersionMaskEntriesMaskEntry"),
    "MasterData": ("xknxmono.models.intermediate.master_data_t", "MasterData"),
    "MasterDataDatapointRoles": ("xknxmono.models.intermediate.master_data_t_datapoint_roles", "MasterDataDatapointRoles"),
    "MasterDataDatapointTypes": ("xknxmono.models.intermediate.master_data_t_datapoint_types", "MasterDataDatapointTypes"),
    "MasterDataFunctionTypes": ("xknxmono.models.intermediate.master_data_t_function_types", "MasterDataFunctionTypes"),
    "MasterDataFunctionalBlocks": ("xknxmono.models.intermediate.master_data_t_functional_blocks", "MasterDataFunctionalBlocks"),
    "MasterDataFunctionalBlocksFunctionalBlock": ("xknxmono.models.intermediate.master_data_t_functional_blocks_functional_block", "MasterDataFunctionalBlocksFunctionalBlock"),
    "MasterDataFunctionalBlocksFunctionalBlockParameters": ("xknxmono.models.intermediate.master_data_t_functional_blocks_functional_block_parameters", "MasterDataFunctionalBlocksFunctionalBlockParameters"),
    "MasterDataFunctionalBlocksFunctionalBlockParametersParameter": ("xknxmono.models.intermediate.master_data_t_functional_blocks_functional_block_parameters_parameter", "MasterDataFunctionalBlocksFunctionalBlockParametersParameter"),
    "MasterDataInterfaceObjectProperties": ("xknxmono.models.intermediate.master_data_t_interface_object_properties", "MasterDataInterfaceObjectProperties"),
    "MasterDataInterfaceObjectPropertiesInterfaceObjectProperty": ("xknxmono.models.intermediate.master_data_t_interface_object_properties_interface_object_property", "MasterDataInterfaceObjectPropertiesInterfaceObjectProperty"),
    "MasterDataInterfaceObjectTypes": ("xknxmono.models.intermediate.master_data_t_interface_object_types", "MasterDataInterfaceObjectTypes"),
    "MasterDataInterfaceObjectTypesInterfaceObjectType": ("xknxmono.models.intermediate.master_data_t_interface_object_types_interface_object_type", "MasterDataInterfaceObjectTypesInterfaceObjectType"),
    "MasterDataLanguages": ("xknxmono.models.intermediate.master_data_t_languages", "MasterDataLanguages"),
    "MasterDataManufacturers": ("xknxmono.models.intermediate.master_data_t_manufacturers", "MasterDataManufacturers"),
    "MasterDataManufacturersManufacturer": ("xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer", "MasterDataManufacturersManufacturer"),
    "MasterDataManufacturersManufacturerDatapointRoles": ("xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_datapoint_roles", "MasterDataManufacturersManufacturerDatapointRoles"),
    "MasterDataManufacturersManufacturerDatapointTypes": ("xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_datapoint_types", "MasterDataManufacturersManufacturerDatapointTypes"),
    "MasterDataManufacturersManufacturerFunctionTypes": ("xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_function_types", "MasterDataManufacturersManufacturerFunctionTypes"),
    "MasterDataManufacturersManufacturerImportRestriction": ("xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_import_restriction", "MasterDataManufacturersManufacturerImportRestriction"),
    "MasterDataManufacturersManufacturerPublicKeys": ("xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_public_keys", "MasterDataManufacturersManufacturerPublicKeys"),
    "MasterDataManufacturersManufacturerPublicKeysPublicKey": ("xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_public_keys_public_key", "MasterDataManufacturersManufacturerPublicKeysPublicKey"),
    "MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue": ("xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_public_keys_public_key_rsakey_value", "MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue"),
    "MasterDataManufacturersManufacturerSpaceUsages": ("xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_space_usages", "MasterDataManufacturersManufacturerSpaceUsages"),
    "MasterDataMaskVersions": ("xknxmono.models.intermediate.master_data_t_mask_versions", "MasterDataMaskVersions"),
    "MasterDataMediumTypes": ("xknxmono.models.intermediate.master_data_t_medium_types", "MasterDataMediumTypes"),
    "MasterDataMediumTypesMediumType": ("xknxmono.models.intermediate.master_data_t_medium_types_medium_type", "MasterDataMediumTypesMediumType"),
    "MasterDataProductLanguages": ("xknxmono.models.intermediate.master_data_t_product_languages", "MasterDataProductLanguages"),
    "MasterDataProductLanguagesLanguage": ("xknxmono.models.intermediate.master_data_t_product_languages_language", "MasterDataProductLanguagesLanguage"),
    "MasterDataPropertyDataTypes": ("xknxmono.models.intermediate.master_data_t_property_data_types", "MasterDataPropertyDataTypes"),
    "MasterDataPropertyDataTypesPropertyDataType": ("xknxmono.models.intermediate.master_data_t_property_data_types_property_data_type", "MasterDataPropertyDataTypesPropertyDataType"),
    "MasterDataSpaceUsages": ("xknxmono.models.intermediate.master_data_t_space_usages", "MasterDataSpaceUsages"),
    "MemberStatus": ("xknxmono.models.intermediate.member_status_t", "MemberStatus"),
    "MemoryParameter": ("xknxmono.models.intermediate.memory_parameter_t", "MemoryParameter"),
    "MemoryType": ("xknxmono.models.intermediate.memory_type_t", "MemoryType"),
    "MemoryUnion": ("xknxmono.models.intermediate.memory_union_t", "MemoryUnion"),
    "ModuleArg": ("xknxmono.models.intermediate.module_arg_t", "ModuleArg"),
    "ModuleDefArgType": ("xknxmono.models.intermediate.module_def_arg_type_t", "ModuleDefArgType"),
    "ModuleDefDynamic": ("xknxmono.models.intermediate.module_def_dynamic_t", "ModuleDefDynamic"),
    "ModuleDefLdCtrlBaseChoose": ("xknxmono.models.intermediate.module_def_ld_ctrl_base_choose_t", "ModuleDefLdCtrlBaseChoose"),
    "ModuleDefLdCtrlBaseChooseWhen": ("xknxmono.models.intermediate.module_def_ld_ctrl_base_choose_t_when", "ModuleDefLdCtrlBaseChooseWhen"),
    "ModuleDefLdCtrlCompareProp": ("xknxmono.models.intermediate.module_def_ld_ctrl_compare_prop_t", "ModuleDefLdCtrlCompareProp"),
    "ModuleDefLdCtrlInvokeFunctionProp": ("xknxmono.models.intermediate.module_def_ld_ctrl_invoke_function_prop_t", "ModuleDefLdCtrlInvokeFunctionProp"),
    "ModuleDefLdCtrlReadFunctionProp": ("xknxmono.models.intermediate.module_def_ld_ctrl_read_function_prop_t", "ModuleDefLdCtrlReadFunctionProp"),
    "ModuleDefLdCtrlWriteProp": ("xknxmono.models.intermediate.module_def_ld_ctrl_write_prop_t", "ModuleDefLdCtrlWriteProp"),
    "ModuleDefLoadProcedure": ("xknxmono.models.intermediate.module_def_load_procedure_t", "ModuleDefLoadProcedure"),
    "ModuleDefLoadProcedures": ("xknxmono.models.intermediate.module_def_load_procedures_t", "ModuleDefLoadProcedures"),
    "ModuleDefStatic": ("xknxmono.models.intermediate.module_def_static_t", "ModuleDefStatic"),
    "ModuleDefStaticAllocators": ("xknxmono.models.intermediate.module_def_static_t_allocators", "ModuleDefStaticAllocators"),
    "ModuleDefStaticComObjectRefs": ("xknxmono.models.intermediate.module_def_static_t_com_object_refs", "ModuleDefStaticComObjectRefs"),
    "ModuleDefStaticComObjects": ("xknxmono.models.intermediate.module_def_static_t_com_objects", "ModuleDefStaticComObjects"),
    "ModuleDefStaticComObjectsComObject": ("xknxmono.models.intermediate.module_def_static_t_com_objects_com_object", "ModuleDefStaticComObjectsComObject"),
    "ModuleDefStaticParameterCalculations": ("xknxmono.models.intermediate.module_def_static_t_parameter_calculations", "ModuleDefStaticParameterCalculations"),
    "ModuleDefStaticParameterRefs": ("xknxmono.models.intermediate.module_def_static_t_parameter_refs", "ModuleDefStaticParameterRefs"),
    "ModuleDefStaticParameterValidations": ("xknxmono.models.intermediate.module_def_static_t_parameter_validations", "ModuleDefStaticParameterValidations"),
    "ModuleDefStaticParameters": ("xknxmono.models.intermediate.module_def_static_t_parameters", "ModuleDefStaticParameters"),
    "ModuleDefStaticParametersParameter": ("xknxmono.models.intermediate.module_def_static_t_parameters_parameter", "ModuleDefStaticParametersParameter"),
    "ModuleDefStaticParametersParameterMemory": ("xknxmono.models.intermediate.module_def_static_t_parameters_parameter_memory", "ModuleDefStaticParametersParameterMemory"),
    "ModuleDefStaticParametersParameterProperty": ("xknxmono.models.intermediate.module_def_static_t_parameters_parameter_property", "ModuleDefStaticParametersParameterProperty"),
    "ModuleDefStaticParametersUnion": ("xknxmono.models.intermediate.module_def_static_t_parameters_union", "ModuleDefStaticParametersUnion"),
    "ModuleDefStaticParametersUnionMemory": ("xknxmono.models.intermediate.module_def_static_t_parameters_union_memory", "ModuleDefStaticParametersUnionMemory"),
    "ModuleDefStaticParametersUnionProperty": ("xknxmono.models.intermediate.module_def_static_t_parameters_union_property", "ModuleDefStaticParametersUnionProperty"),
    "ModuleDef": ("xknxmono.models.intermediate.module_def_t", "ModuleDef"),
    "ModuleDefSubModuleDefs": ("xknxmono.models.intermediate.module_def_t", "ModuleDefSubModuleDefs"),
    "ModuleDefArguments": ("xknxmono.models.intermediate.module_def_t_arguments", "ModuleDefArguments"),
    "ModuleDefArgumentsArgument": ("xknxmono.models.intermediate.module_def_t_arguments_argument", "ModuleDefArgumentsArgument"),
    "ModuleDefArgumentsArgumentAlignment": ("xknxmono.models.intermediate.module_def_t_arguments_argument_alignment", "ModuleDefArgumentsArgumentAlignment"),
    "ModuleInstance": ("xknxmono.models.intermediate.module_instance_t", "ModuleInstance"),
    "ModuleInstanceArguments": ("xknxmono.models.intermediate.module_instance_t_arguments", "ModuleInstanceArguments"),
    "ModuleInstanceArgumentsArgument": ("xknxmono.models.intermediate.module_instance_t_arguments_argument", "ModuleInstanceArgumentsArgument"),
    "Module": ("xknxmono.models.intermediate.module_t", "Module"),
    "ModuleNumericArg": ("xknxmono.models.intermediate.module_t_numeric_arg", "ModuleNumericArg"),
    "ModuleTextArg": ("xknxmono.models.intermediate.module_t_text_arg", "ModuleTextArg"),
    "Node": ("xknxmono.models.intermediate.node_t", "Node"),
    "NodeNodes": ("xknxmono.models.intermediate.node_t", "NodeNodes"),
    "NodeType": ("xknxmono.models.intermediate.node_t_type", "NodeType"),
    "P2PlinkBusInterfaceEndpoint": ("xknxmono.models.intermediate.p2_plink_bus_interface_endpoint_t", "P2PlinkBusInterfaceEndpoint"),
    "P2PlinkDeviceEndpoint": ("xknxmono.models.intermediate.p2_plink_device_endpoint_t", "P2PlinkDeviceEndpoint"),
    "P2PlinkEndpoint": ("xknxmono.models.intermediate.p2_plink_endpoint_t", "P2PlinkEndpoint"),
    "P2Plinks": ("xknxmono.models.intermediate.p2_plinks_t", "P2Plinks"),
    "P2PlinksP2Plink": ("xknxmono.models.intermediate.p2_plinks_t_p2_plink", "P2PlinksP2Plink"),
    "ParameterBase": ("xknxmono.models.intermediate.parameter_base_t", "ParameterBase"),
    "ParameterBlockLayout": ("xknxmono.models.intermediate.parameter_block_layout_t", "ParameterBlockLayout"),
    "ParameterCalculation": ("xknxmono.models.intermediate.parameter_calculation_t", "ParameterCalculation"),
    "ParameterCalculationLanguage": ("xknxmono.models.intermediate.parameter_calculation_t_language", "ParameterCalculationLanguage"),
    "ParameterCalculationLparameters": ("xknxmono.models.intermediate.parameter_calculation_t_lparameters", "ParameterCalculationLparameters"),
    "ParameterCalculationRparameters": ("xknxmono.models.intermediate.parameter_calculation_t_rparameters", "ParameterCalculationRparameters"),
    "ParameterInstanceRef": ("xknxmono.models.intermediate.parameter_instance_ref_t", "ParameterInstanceRef"),
    "ParameterRefRef": ("xknxmono.models.intermediate.parameter_ref_ref_t", "ParameterRefRef"),
    "ParameterRef": ("xknxmono.models.intermediate.parameter_ref_t", "ParameterRef"),
    "ParameterSeparator": ("xknxmono.models.intermediate.parameter_separator_t", "ParameterSeparator"),
    "ParameterSeparatorUihint": ("xknxmono.models.intermediate.parameter_separator_t_uihint", "ParameterSeparatorUihint"),
    "ParameterType": ("xknxmono.models.intermediate.parameter_type_t", "ParameterType"),
    "ParameterTypeTypeColor": ("xknxmono.models.intermediate.parameter_type_t_type_color", "ParameterTypeTypeColor"),
    "ParameterTypeTypeColorSpace": ("xknxmono.models.intermediate.parameter_type_t_type_color_space", "ParameterTypeTypeColorSpace"),
    "ParameterTypeTypeDate": ("xknxmono.models.intermediate.parameter_type_t_type_date", "ParameterTypeTypeDate"),
    "ParameterTypeTypeDateEncoding": ("xknxmono.models.intermediate.parameter_type_t_type_date_encoding", "ParameterTypeTypeDateEncoding"),
    "ParameterTypeTypeFloat": ("xknxmono.models.intermediate.parameter_type_t_type_float", "ParameterTypeTypeFloat"),
    "ParameterTypeTypeFloatEncoding": ("xknxmono.models.intermediate.parameter_type_t_type_float_encoding", "ParameterTypeTypeFloatEncoding"),
    "ParameterTypeTypeFloatUihint": ("xknxmono.models.intermediate.parameter_type_t_type_float_uihint", "ParameterTypeTypeFloatUihint"),
    "ParameterTypeTypeIpaddress": ("xknxmono.models.intermediate.parameter_type_t_type_ipaddress", "ParameterTypeTypeIpaddress"),
    "ParameterTypeTypeIpaddressAddressType": ("xknxmono.models.intermediate.parameter_type_t_type_ipaddress_address_type", "ParameterTypeTypeIpaddressAddressType"),
    "ParameterTypeTypeIpaddressVersion": ("xknxmono.models.intermediate.parameter_type_t_type_ipaddress_version", "ParameterTypeTypeIpaddressVersion"),
    "ParameterTypeTypeNumber": ("xknxmono.models.intermediate.parameter_type_t_type_number", "ParameterTypeTypeNumber"),
    "ParameterTypeTypeNumberType": ("xknxmono.models.intermediate.parameter_type_t_type_number_type", "ParameterTypeTypeNumberType"),
    "ParameterTypeTypeNumberUihint": ("xknxmono.models.intermediate.parameter_type_t_type_number_uihint", "ParameterTypeTypeNumberUihint"),
    "ParameterTypeTypePicture": ("xknxmono.models.intermediate.parameter_type_t_type_picture", "ParameterTypeTypePicture"),
    "ParameterTypeTypeRawData": ("xknxmono.models.intermediate.parameter_type_t_type_raw_data", "ParameterTypeTypeRawData"),
    "ParameterTypeTypeRestriction": ("xknxmono.models.intermediate.parameter_type_t_type_restriction", "ParameterTypeTypeRestriction"),
    "ParameterTypeTypeRestrictionBase": ("xknxmono.models.intermediate.parameter_type_t_type_restriction_base", "ParameterTypeTypeRestrictionBase"),
    "ParameterTypeTypeRestrictionEnumeration": ("xknxmono.models.intermediate.parameter_type_t_type_restriction_enumeration", "ParameterTypeTypeRestrictionEnumeration"),
    "ParameterTypeTypeRestrictionUihint": ("xknxmono.models.intermediate.parameter_type_t_type_restriction_uihint", "ParameterTypeTypeRestrictionUihint"),
    "ParameterTypeTypeText": ("xknxmono.models.intermediate.parameter_type_t_type_text", "ParameterTypeTypeText"),
    "ParameterTypeTypeTime": ("xknxmono.models.intermediate.parameter_type_t_type_time", "ParameterTypeTypeTime"),
    "ParameterTypeTypeTimeUihint": ("xknxmono.models.intermediate.parameter_type_t_type_time_uihint", "ParameterTypeTypeTimeUihint"),
    "ParameterTypeTypeTimeUnit": ("xknxmono.models.intermediate.parameter_type_t_type_time_unit", "ParameterTypeTypeTimeUnit"),
    "ParameterValidation": ("xknxmono.models.intermediate.parameter_validation_t", "ParameterValidation"),
    "ParameterValidationParameters": ("xknxmono.models.intermediate.parameter_validation_t_parameters", "ParameterValidationParameters"),
    "ProcedureType": ("xknxmono.models.intermediate.procedure_type_t", "ProcedureType"),
    "Project": ("xknxmono.models.intermediate.project_t", "Project"),
    "ProjectAddinData": ("xknxmono.models.intermediate.project_t_addin_data", "ProjectAddinData"),
    "ProjectInstallations": ("xknxmono.models.intermediate.project_t_installations", "ProjectInstallations"),
    "ProjectInstallationsInstallation": ("xknxmono.models.intermediate.project_t_installations_installation", "ProjectInstallationsInstallation"),
    "ProjectInstallationsInstallationSplitType": ("xknxmono.models.intermediate.project_t_installations_installation_split_type", "ProjectInstallationsInstallationSplitType"),
    "ProjectProjectInformation": ("xknxmono.models.intermediate.project_t_project_information", "ProjectProjectInformation"),
    "ProjectProjectInformationDeviceCertificates": ("xknxmono.models.intermediate.project_t_project_information_device_certificates", "ProjectProjectInformationDeviceCertificates"),
    "ProjectProjectInformationHistoryEntries": ("xknxmono.models.intermediate.project_t_project_information_history_entries", "ProjectProjectInformationHistoryEntries"),
    "ProjectProjectInformationHistoryEntriesHistoryEntry": ("xknxmono.models.intermediate.project_t_project_information_history_entries_history_entry", "ProjectProjectInformationHistoryEntriesHistoryEntry"),
    "ProjectProjectInformationProjectTraces": ("xknxmono.models.intermediate.project_t_project_information_project_traces", "ProjectProjectInformationProjectTraces"),
    "ProjectProjectInformationTags": ("xknxmono.models.intermediate.project_t_project_information_tags", "ProjectProjectInformationTags"),
    "ProjectProjectInformationTagsTag": ("xknxmono.models.intermediate.project_t_project_information_tags_tag", "ProjectProjectInformationTagsTag"),
    "ProjectProjectInformationToDoItems": ("xknxmono.models.intermediate.project_t_project_information_to_do_items", "ProjectProjectInformationToDoItems"),
    "ProjectUserFiles": ("xknxmono.models.intermediate.project_t_user_files", "ProjectUserFiles"),
    "ProjectTrace": ("xknxmono.models.intermediate.project_trace_t", "ProjectTrace"),
    "ProjectTracingLevel": ("xknxmono.models.intermediate.project_tracing_level_t", "ProjectTracingLevel"),
    "ProjectType": ("xknxmono.models.intermediate.project_type_t", "ProjectType"),
    "PropType": ("xknxmono.models.intermediate.prop_type_t", "PropType"),
    "PropertyParameter": ("xknxmono.models.intermediate.property_parameter_t", "PropertyParameter"),
    "PropertyUnion": ("xknxmono.models.intermediate.property_union_t", "PropertyUnion"),
    "RegistrationInfo": ("xknxmono.models.intermediate.registration_info_t", "RegistrationInfo"),
    "RegistrationInfoRegistrationKey": ("xknxmono.models.intermediate.registration_info_t_registration_key", "RegistrationInfoRegistrationKey"),
    "RegistrationStatus": ("xknxmono.models.intermediate.registration_status_t", "RegistrationStatus"),
    "Rename": ("xknxmono.models.intermediate.rename_t", "Rename"),
    "ResourceAccessRights": ("xknxmono.models.intermediate.resource_access_rights_t", "ResourceAccessRights"),
    "ResourceAccess": ("xknxmono.models.intermediate.resource_access_t", "ResourceAccess"),
    "ResourceAddrSpace": ("xknxmono.models.intermediate.resource_addr_space_t", "ResourceAddrSpace"),
    "ResourceLocation": ("xknxmono.models.intermediate.resource_location_t", "ResourceLocation"),
    "ResourceMgmtStyle": ("xknxmono.models.intermediate.resource_mgmt_style_t", "ResourceMgmtStyle"),
    "ResourceName": ("xknxmono.models.intermediate.resource_name_t", "ResourceName"),
    "RfdeviceMode": ("xknxmono.models.intermediate.rfdevice_mode_t", "RfdeviceMode"),
    "RfrxCapabilities": ("xknxmono.models.intermediate.rfrx_capabilities_t", "RfrxCapabilities"),
    "RftxCapabilities": ("xknxmono.models.intermediate.rftx_capabilities_t", "RftxCapabilities"),
    "SecurityMode": ("xknxmono.models.intermediate.security_mode_t", "SecurityMode"),
    "Security": ("xknxmono.models.intermediate.security_t", "Security"),
    "SegmentBase": ("xknxmono.models.intermediate.segment_base_t", "SegmentBase"),
    "Space": ("xknxmono.models.intermediate.space_t", "Space"),
    "SpaceType": ("xknxmono.models.intermediate.space_type_t", "SpaceType"),
    "SpaceUsage": ("xknxmono.models.intermediate.space_usage_t", "SpaceUsage"),
    "SplitInfo": ("xknxmono.models.intermediate.split_info_t", "SplitInfo"),
    "SplitInfos": ("xknxmono.models.intermediate.split_infos_t", "SplitInfos"),
    "TextAlignment": ("xknxmono.models.intermediate.text_alignment_t", "TextAlignment"),
    "TextEncoding": ("xknxmono.models.intermediate.text_encoding_t", "TextEncoding"),
    "ToDoItem": ("xknxmono.models.intermediate.to_do_item_t", "ToDoItem"),
    "ToDoStatus": ("xknxmono.models.intermediate.to_do_status_t", "ToDoStatus"),
    "Topology": ("xknxmono.models.intermediate.topology_t", "Topology"),
    "TopologyArea": ("xknxmono.models.intermediate.topology_t_area", "TopologyArea"),
    "TopologyAreaLine": ("xknxmono.models.intermediate.topology_t_area_line", "TopologyAreaLine"),
    "TopologyAreaLineSegment": ("xknxmono.models.intermediate.topology_t_area_line_segment", "TopologyAreaLineSegment"),
    "TopologyAreaLineSegmentAdditionalGroupAddresses": ("xknxmono.models.intermediate.topology_t_area_line_segment_additional_group_addresses", "TopologyAreaLineSegmentAdditionalGroupAddresses"),
    "TopologyAreaLineSegmentAdditionalGroupAddressesGroupAddress": ("xknxmono.models.intermediate.topology_t_area_line_segment_additional_group_addresses_group_address", "TopologyAreaLineSegmentAdditionalGroupAddressesGroupAddress"),
    "TopologyUnassignedDevices": ("xknxmono.models.intermediate.topology_t_unassigned_devices", "TopologyUnassignedDevices"),
    "Trade": ("xknxmono.models.intermediate.trade_t", "Trade"),
    "Trades": ("xknxmono.models.intermediate.trades_t", "Trades"),
    "UnionParameter": ("xknxmono.models.intermediate.union_parameter_t", "UnionParameter"),
    "UserFile": ("xknxmono.models.intermediate.user_file_t", "UserFile"),
    "When": ("xknxmono.models.intermediate.when_t", "When"),
}

__all__ = [
    "Access",
    "AddinData",
    "Allocator",
    "ApplicationProgram",
    "ApplicationProgramChannel",
    "ApplicationProgramCloudConnect",
    "ApplicationProgramDynamic",
    "ApplicationProgramIpconfig",
    "ApplicationProgramMinEtsVersion",
    "ApplicationProgramModuleDefs",
    "ApplicationProgramProfile",
    "ApplicationProgramProfileIo",
    "ApplicationProgramRef",
    "ApplicationProgramStatic",
    "ApplicationProgramStaticAddressTable",
    "ApplicationProgramStaticAllocators",
    "ApplicationProgramStaticAssociationTable",
    "ApplicationProgramStaticBinaryData",
    "ApplicationProgramStaticBusInterfaces",
    "ApplicationProgramStaticBusInterfacesBusInterface",
    "ApplicationProgramStaticBusInterfacesBusInterfaceAccessType",
    "ApplicationProgramStaticCode",
    "ApplicationProgramStaticCodeAbsoluteSegment",
    "ApplicationProgramStaticCodeRelativeSegment",
    "ApplicationProgramStaticComObjectRefs",
    "ApplicationProgramStaticComObjectTable",
    "ApplicationProgramStaticDeviceCompare",
    "ApplicationProgramStaticDeviceCompareExcludeMemory",
    "ApplicationProgramStaticDeviceCompareExcludeProperty",
    "ApplicationProgramStaticExtension",
    "ApplicationProgramStaticExtensionBaggage",
    "ApplicationProgramStaticFixupList",
    "ApplicationProgramStaticMessages",
    "ApplicationProgramStaticMessagesMessage",
    "ApplicationProgramStaticOptions",
    "ApplicationProgramStaticOptionsCustomerAdjustableParameters",
    "ApplicationProgramStaticOptionsNotLoadable",
    "ApplicationProgramStaticOptionsParameterByteOrder",
    "ApplicationProgramStaticParameterCalculations",
    "ApplicationProgramStaticParameterRefs",
    "ApplicationProgramStaticParameterTypes",
    "ApplicationProgramStaticParameterValidations",
    "ApplicationProgramStaticParameters",
    "ApplicationProgramStaticParametersParameter",
    "ApplicationProgramStaticParametersUnion",
    "ApplicationProgramStaticScript",
    "ApplicationProgramStaticSecurityRoles",
    "ApplicationProgramStaticSecurityRolesSecurityRole",
    "ApplicationProgramType",
    "Assign",
    "BinaryData",
    "BinaryDataRef",
    "BusAccess",
    "BusInterface",
    "BusInterfaceConnectors",
    "BusInterfaceConnectorsConnector",
    "Button",
    "ButtonEventHandlerOnline",
    "CalculationParameterRef",
    "Capability",
    "CatalogSection",
    "CatalogSectionCatalogItem",
    "ChannelChoose",
    "ChannelChooseWhen",
    "ChannelIndependentBlock",
    "ChannelInstance",
    "ComObject",
    "ComObjectInstanceRef",
    "ComObjectParameterBlock",
    "ComObjectParameterBlockColumns",
    "ComObjectParameterBlockColumnsColumn",
    "ComObjectParameterBlockRows",
    "ComObjectParameterBlockRowsRow",
    "ComObjectParameterChoose",
    "ComObjectParameterChooseWhen",
    "ComObjectPriority",
    "ComObjectRef",
    "ComObjectRefRef",
    "ComObjectSecurityRequirements",
    "ComObjectSize",
    "ComTableExpectation",
    "CompletionStatus",
    "CouplerCapability",
    "DatapointRole",
    "DatapointType",
    "DatapointTypeDatapointSubtypes",
    "DatapointTypeDatapointSubtypesDatapointSubtype",
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormat",
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit",
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration",
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumerationEnumValue",
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat",
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType",
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved",
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger",
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatString",
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger",
    "DependentChannelChoose",
    "DependentChannelChooseWhen",
    "DeprecationStatus",
    "DeviceCertificate",
    "DeviceInstance",
    "DeviceInstanceAdditionalAddresses",
    "DeviceInstanceAdditionalAddressesAddress",
    "DeviceInstanceBinaryData",
    "DeviceInstanceBinaryDataBinaryData",
    "DeviceInstanceBusInterfaces",
    "DeviceInstanceChannelInstances",
    "DeviceInstanceComObjectInstanceRefs",
    "DeviceInstanceGroupObjectTree",
    "DeviceInstanceGroupObjectTreeNodes",
    "DeviceInstanceModuleInstances",
    "DeviceInstanceParameterInstanceRefs",
    "DeviceInstanceRef",
    "DeviceInstanceRfFastAckSlots",
    "DeviceInstanceRfFastAckSlotsSlot",
    "DownloadBehavior",
    "Enable",
    "Fixup",
    "Function",
    "FunctionType",
    "FunctionTypeFunctionPoint",
    "FunctionsGroup",
    "GroupAddress",
    "GroupAddressRef",
    "GroupAddressStyle",
    "GroupAddresses",
    "GroupAddressesGroupRanges",
    "GroupRange",
    "Hardware",
    "Hardware2Program",
    "HardwareHardware2Programs",
    "HardwareProducts",
    "HardwareProductsProduct",
    "HardwareProductsProductAttributes",
    "HardwareProductsProductAttributesAttribute",
    "HardwareProductsProductAttributesAttributeName",
    "HardwareProductsProductBaggages",
    "HardwareProductsProductBaggagesBaggage",
    "HawkConfigurationData",
    "HawkConfigurationDataFeatures",
    "HawkConfigurationDataFeaturesFeature",
    "HawkConfigurationDataFeaturesFeatureName",
    "HawkConfigurationDataInterfaceObjects",
    "HawkConfigurationDataInterfaceObjectsInterfaceObject",
    "HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty",
    "HawkConfigurationDataMemorySegments",
    "HawkConfigurationDataMemorySegmentsMemorySegment",
    "HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights",
    "HawkConfigurationDataProcedures",
    "HawkConfigurationDataProceduresProcedure",
    "HawkConfigurationDataProceduresProcedureValue",
    "HawkConfigurationDataResources",
    "HawkConfigurationDataResourcesResource",
    "HawkConfigurationDataResourcesResourceAccessRights",
    "HawkConfigurationDataResourcesResourceResourceType",
    "HawkConfigurationDataResourcesResourceResourceTypeFlavour",
    "HorizontalAlignment",
    "IoPointParameter",
    "Ipconfig",
    "IpconfigAssign",
    "Knx",
    "LanguageData",
    "LanguageDataTranslationUnit",
    "LanguageDataTranslationUnitTranslationElement",
    "LanguageDataTranslationUnitTranslationElementTranslation",
    "LdCtrlAbsSegment",
    "LdCtrlBase",
    "LdCtrlBaseChoose",
    "LdCtrlBaseChooseWhen",
    "LdCtrlBaseOnError",
    "LdCtrlClearCachedObjectTypes",
    "LdCtrlClearLcfilterTable",
    "LdCtrlCompareBase",
    "LdCtrlCompareMem",
    "LdCtrlCompareProp",
    "LdCtrlCompareRelMem",
    "LdCtrlConnect",
    "LdCtrlControlVariable",
    "LdCtrlDeclarePropDesc",
    "LdCtrlDelay",
    "LdCtrlDisconnect",
    "LdCtrlErrorCause",
    "LdCtrlInvokeFunctionProp",
    "LdCtrlLoad",
    "LdCtrlLoadCompleted",
    "LdCtrlLoadImageMem",
    "LdCtrlLoadImageProp",
    "LdCtrlLoadImageRelMem",
    "LdCtrlMapError",
    "LdCtrlMasterReset",
    "LdCtrlMaxLength",
    "LdCtrlMemAddrSpace",
    "LdCtrlMerge",
    "LdCtrlProcType",
    "LdCtrlProgressText",
    "LdCtrlReadFunctionProp",
    "LdCtrlRelSegment",
    "LdCtrlRestart",
    "LdCtrlSetControlVariable",
    "LdCtrlTaskCtrl1",
    "LdCtrlTaskCtrl2",
    "LdCtrlTaskPtr",
    "LdCtrlTaskSegment",
    "LdCtrlUnload",
    "LdCtrlWriteMem",
    "LdCtrlWriteProp",
    "LdCtrlWriteRelMem",
    "LoadProcedure",
    "LoadProcedureStyle",
    "LoadProcedures",
    "LoadProceduresLoadProcedure",
    "Locations",
    "ManufacturerData",
    "ManufacturerDataManufacturer",
    "ManufacturerDataManufacturerApplicationPrograms",
    "ManufacturerDataManufacturerBaggages",
    "ManufacturerDataManufacturerBaggagesBaggage",
    "ManufacturerDataManufacturerBaggagesBaggageFileInfo",
    "ManufacturerDataManufacturerCatalog",
    "ManufacturerDataManufacturerHardware",
    "ManufacturerDataManufacturerLanguages",
    "MaskVersion",
    "MaskVersionDownwardCompatibleMasks",
    "MaskVersionDownwardCompatibleMasksDownwardCompatibleMask",
    "MaskVersionManagementModel",
    "MaskVersionMaskEntries",
    "MaskVersionMaskEntriesMaskEntry",
    "MasterData",
    "MasterDataDatapointRoles",
    "MasterDataDatapointTypes",
    "MasterDataFunctionTypes",
    "MasterDataFunctionalBlocks",
    "MasterDataFunctionalBlocksFunctionalBlock",
    "MasterDataFunctionalBlocksFunctionalBlockParameters",
    "MasterDataFunctionalBlocksFunctionalBlockParametersParameter",
    "MasterDataInterfaceObjectProperties",
    "MasterDataInterfaceObjectPropertiesInterfaceObjectProperty",
    "MasterDataInterfaceObjectTypes",
    "MasterDataInterfaceObjectTypesInterfaceObjectType",
    "MasterDataLanguages",
    "MasterDataManufacturers",
    "MasterDataManufacturersManufacturer",
    "MasterDataManufacturersManufacturerDatapointRoles",
    "MasterDataManufacturersManufacturerDatapointTypes",
    "MasterDataManufacturersManufacturerFunctionTypes",
    "MasterDataManufacturersManufacturerImportRestriction",
    "MasterDataManufacturersManufacturerPublicKeys",
    "MasterDataManufacturersManufacturerPublicKeysPublicKey",
    "MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue",
    "MasterDataManufacturersManufacturerSpaceUsages",
    "MasterDataMaskVersions",
    "MasterDataMediumTypes",
    "MasterDataMediumTypesMediumType",
    "MasterDataProductLanguages",
    "MasterDataProductLanguagesLanguage",
    "MasterDataPropertyDataTypes",
    "MasterDataPropertyDataTypesPropertyDataType",
    "MasterDataSpaceUsages",
    "MemberStatus",
    "MemoryParameter",
    "MemoryType",
    "MemoryUnion",
    "Module",
    "ModuleArg",
    "ModuleDef",
    "ModuleDefArgType",
    "ModuleDefArguments",
    "ModuleDefArgumentsArgument",
    "ModuleDefArgumentsArgumentAlignment",
    "ModuleDefDynamic",
    "ModuleDefLdCtrlBaseChoose",
    "ModuleDefLdCtrlBaseChooseWhen",
    "ModuleDefLdCtrlCompareProp",
    "ModuleDefLdCtrlInvokeFunctionProp",
    "ModuleDefLdCtrlReadFunctionProp",
    "ModuleDefLdCtrlWriteProp",
    "ModuleDefLoadProcedure",
    "ModuleDefLoadProcedures",
    "ModuleDefStatic",
    "ModuleDefStaticAllocators",
    "ModuleDefStaticComObjectRefs",
    "ModuleDefStaticComObjects",
    "ModuleDefStaticComObjectsComObject",
    "ModuleDefStaticParameterCalculations",
    "ModuleDefStaticParameterRefs",
    "ModuleDefStaticParameterValidations",
    "ModuleDefStaticParameters",
    "ModuleDefStaticParametersParameter",
    "ModuleDefStaticParametersParameterMemory",
    "ModuleDefStaticParametersParameterProperty",
    "ModuleDefStaticParametersUnion",
    "ModuleDefStaticParametersUnionMemory",
    "ModuleDefStaticParametersUnionProperty",
    "ModuleDefSubModuleDefs",
    "ModuleInstance",
    "ModuleInstanceArguments",
    "ModuleInstanceArgumentsArgument",
    "ModuleNumericArg",
    "ModuleTextArg",
    "Node",
    "NodeNodes",
    "NodeType",
    "P2PlinkBusInterfaceEndpoint",
    "P2PlinkDeviceEndpoint",
    "P2PlinkEndpoint",
    "P2Plinks",
    "P2PlinksP2Plink",
    "ParameterBase",
    "ParameterBlockLayout",
    "ParameterCalculation",
    "ParameterCalculationLanguage",
    "ParameterCalculationLparameters",
    "ParameterCalculationRparameters",
    "ParameterInstanceRef",
    "ParameterRef",
    "ParameterRefRef",
    "ParameterSeparator",
    "ParameterSeparatorUihint",
    "ParameterType",
    "ParameterTypeTypeColor",
    "ParameterTypeTypeColorSpace",
    "ParameterTypeTypeDate",
    "ParameterTypeTypeDateEncoding",
    "ParameterTypeTypeFloat",
    "ParameterTypeTypeFloatEncoding",
    "ParameterTypeTypeFloatUihint",
    "ParameterTypeTypeIpaddress",
    "ParameterTypeTypeIpaddressAddressType",
    "ParameterTypeTypeIpaddressVersion",
    "ParameterTypeTypeNumber",
    "ParameterTypeTypeNumberType",
    "ParameterTypeTypeNumberUihint",
    "ParameterTypeTypePicture",
    "ParameterTypeTypeRawData",
    "ParameterTypeTypeRestriction",
    "ParameterTypeTypeRestrictionBase",
    "ParameterTypeTypeRestrictionEnumeration",
    "ParameterTypeTypeRestrictionUihint",
    "ParameterTypeTypeText",
    "ParameterTypeTypeTime",
    "ParameterTypeTypeTimeUihint",
    "ParameterTypeTypeTimeUnit",
    "ParameterValidation",
    "ParameterValidationParameters",
    "ProcedureType",
    "Project",
    "ProjectAddinData",
    "ProjectInstallations",
    "ProjectInstallationsInstallation",
    "ProjectInstallationsInstallationSplitType",
    "ProjectProjectInformation",
    "ProjectProjectInformationDeviceCertificates",
    "ProjectProjectInformationHistoryEntries",
    "ProjectProjectInformationHistoryEntriesHistoryEntry",
    "ProjectProjectInformationProjectTraces",
    "ProjectProjectInformationTags",
    "ProjectProjectInformationTagsTag",
    "ProjectProjectInformationToDoItems",
    "ProjectTrace",
    "ProjectTracingLevel",
    "ProjectType",
    "ProjectUserFiles",
    "PropType",
    "PropertyParameter",
    "PropertyUnion",
    "RegistrationInfo",
    "RegistrationInfoRegistrationKey",
    "RegistrationStatus",
    "Rename",
    "Repeat",
    "ResourceAccess",
    "ResourceAccessRights",
    "ResourceAddrSpace",
    "ResourceLocation",
    "ResourceMgmtStyle",
    "ResourceName",
    "RfdeviceMode",
    "RfrxCapabilities",
    "RftxCapabilities",
    "Security",
    "SecurityMode",
    "SegmentBase",
    "Space",
    "SpaceType",
    "SpaceUsage",
    "SplitInfo",
    "SplitInfos",
    "TextAlignment",
    "TextEncoding",
    "TextEncodingSelector",
    "ToDoItem",
    "ToDoStatus",
    "Topology",
    "TopologyArea",
    "TopologyAreaLine",
    "TopologyAreaLineSegment",
    "TopologyAreaLineSegmentAdditionalGroupAddresses",
    "TopologyAreaLineSegmentAdditionalGroupAddressesGroupAddress",
    "TopologyUnassignedDevices",
    "Trade",
    "Trades",
    "UnionParameter",
    "UserFile",
    "When",
]

if TYPE_CHECKING:
    from xknxmono.models.intermediate.access_t import Access
    from xknxmono.models.intermediate.addin_data_t import AddinData
    from xknxmono.models.intermediate.allocator_t import Allocator
    from xknxmono.models.intermediate.application_program_channel_t import ApplicationProgramChannel
    from xknxmono.models.intermediate.application_program_channel_t import ChannelChoose
    from xknxmono.models.intermediate.application_program_channel_t import ChannelChooseWhen
    from xknxmono.models.intermediate.application_program_channel_t import ComObjectParameterBlock
    from xknxmono.models.intermediate.application_program_channel_t import ComObjectParameterChoose
    from xknxmono.models.intermediate.application_program_channel_t import ComObjectParameterChooseWhen
    from xknxmono.models.intermediate.application_program_channel_t import Repeat
    from xknxmono.models.intermediate.application_program_dynamic_t import ApplicationProgramDynamic
    from xknxmono.models.intermediate.application_program_ipconfig_t import ApplicationProgramIpconfig
    from xknxmono.models.intermediate.application_program_ref_t import ApplicationProgramRef
    from xknxmono.models.intermediate.application_program_static_t import ApplicationProgramStatic
    from xknxmono.models.intermediate.application_program_static_t_address_table import ApplicationProgramStaticAddressTable
    from xknxmono.models.intermediate.application_program_static_t_allocators import ApplicationProgramStaticAllocators
    from xknxmono.models.intermediate.application_program_static_t_association_table import ApplicationProgramStaticAssociationTable
    from xknxmono.models.intermediate.application_program_static_t_binary_data import ApplicationProgramStaticBinaryData
    from xknxmono.models.intermediate.application_program_static_t_bus_interfaces import ApplicationProgramStaticBusInterfaces
    from xknxmono.models.intermediate.application_program_static_t_bus_interfaces_bus_interface import ApplicationProgramStaticBusInterfacesBusInterface
    from xknxmono.models.intermediate.application_program_static_t_bus_interfaces_bus_interface_access_type import ApplicationProgramStaticBusInterfacesBusInterfaceAccessType
    from xknxmono.models.intermediate.application_program_static_t_code import ApplicationProgramStaticCode
    from xknxmono.models.intermediate.application_program_static_t_code_absolute_segment import ApplicationProgramStaticCodeAbsoluteSegment
    from xknxmono.models.intermediate.application_program_static_t_code_relative_segment import ApplicationProgramStaticCodeRelativeSegment
    from xknxmono.models.intermediate.application_program_static_t_com_object_refs import ApplicationProgramStaticComObjectRefs
    from xknxmono.models.intermediate.application_program_static_t_com_object_table import ApplicationProgramStaticComObjectTable
    from xknxmono.models.intermediate.application_program_static_t_device_compare import ApplicationProgramStaticDeviceCompare
    from xknxmono.models.intermediate.application_program_static_t_device_compare_exclude_memory import ApplicationProgramStaticDeviceCompareExcludeMemory
    from xknxmono.models.intermediate.application_program_static_t_device_compare_exclude_property import ApplicationProgramStaticDeviceCompareExcludeProperty
    from xknxmono.models.intermediate.application_program_static_t_extension import ApplicationProgramStaticExtension
    from xknxmono.models.intermediate.application_program_static_t_extension_baggage import ApplicationProgramStaticExtensionBaggage
    from xknxmono.models.intermediate.application_program_static_t_fixup_list import ApplicationProgramStaticFixupList
    from xknxmono.models.intermediate.application_program_static_t_messages import ApplicationProgramStaticMessages
    from xknxmono.models.intermediate.application_program_static_t_messages_message import ApplicationProgramStaticMessagesMessage
    from xknxmono.models.intermediate.application_program_static_t_options import ApplicationProgramStaticOptions
    from xknxmono.models.intermediate.application_program_static_t_options_customer_adjustable_parameters import ApplicationProgramStaticOptionsCustomerAdjustableParameters
    from xknxmono.models.intermediate.application_program_static_t_options_not_loadable import ApplicationProgramStaticOptionsNotLoadable
    from xknxmono.models.intermediate.application_program_static_t_options_parameter_byte_order import ApplicationProgramStaticOptionsParameterByteOrder
    from xknxmono.models.intermediate.application_program_static_t_options_text_parameter_encoding_selector import TextEncodingSelector
    from xknxmono.models.intermediate.application_program_static_t_parameter_calculations import ApplicationProgramStaticParameterCalculations
    from xknxmono.models.intermediate.application_program_static_t_parameter_refs import ApplicationProgramStaticParameterRefs
    from xknxmono.models.intermediate.application_program_static_t_parameter_types import ApplicationProgramStaticParameterTypes
    from xknxmono.models.intermediate.application_program_static_t_parameter_validations import ApplicationProgramStaticParameterValidations
    from xknxmono.models.intermediate.application_program_static_t_parameters import ApplicationProgramStaticParameters
    from xknxmono.models.intermediate.application_program_static_t_parameters_parameter import ApplicationProgramStaticParametersParameter
    from xknxmono.models.intermediate.application_program_static_t_parameters_union import ApplicationProgramStaticParametersUnion
    from xknxmono.models.intermediate.application_program_static_t_script import ApplicationProgramStaticScript
    from xknxmono.models.intermediate.application_program_static_t_security_roles import ApplicationProgramStaticSecurityRoles
    from xknxmono.models.intermediate.application_program_static_t_security_roles_security_role import ApplicationProgramStaticSecurityRolesSecurityRole
    from xknxmono.models.intermediate.application_program_t import ApplicationProgram
    from xknxmono.models.intermediate.application_program_t_cloud_connect import ApplicationProgramCloudConnect
    from xknxmono.models.intermediate.application_program_t_min_ets_version import ApplicationProgramMinEtsVersion
    from xknxmono.models.intermediate.application_program_t_module_defs import ApplicationProgramModuleDefs
    from xknxmono.models.intermediate.application_program_t_profile import ApplicationProgramProfile
    from xknxmono.models.intermediate.application_program_t_profile_io_t import ApplicationProgramProfileIo
    from xknxmono.models.intermediate.application_program_type_t import ApplicationProgramType
    from xknxmono.models.intermediate.assign_t import Assign
    from xknxmono.models.intermediate.binary_data_ref_t import BinaryDataRef
    from xknxmono.models.intermediate.binary_data_t import BinaryData
    from xknxmono.models.intermediate.bus_access_t import BusAccess
    from xknxmono.models.intermediate.bus_interface_t import BusInterface
    from xknxmono.models.intermediate.bus_interface_t_connectors import BusInterfaceConnectors
    from xknxmono.models.intermediate.bus_interface_t_connectors_connector import BusInterfaceConnectorsConnector
    from xknxmono.models.intermediate.button_t import Button
    from xknxmono.models.intermediate.button_t_event_handler_online import ButtonEventHandlerOnline
    from xknxmono.models.intermediate.calculation_parameter_ref_t import CalculationParameterRef
    from xknxmono.models.intermediate.capability_t import Capability
    from xknxmono.models.intermediate.catalog_section_t import CatalogSection
    from xknxmono.models.intermediate.catalog_section_t_catalog_item import CatalogSectionCatalogItem
    from xknxmono.models.intermediate.channel_independent_block_t import ChannelIndependentBlock
    from xknxmono.models.intermediate.channel_instance_t import ChannelInstance
    from xknxmono.models.intermediate.com_object_instance_ref_t import ComObjectInstanceRef
    from xknxmono.models.intermediate.com_object_parameter_block_t_columns import ComObjectParameterBlockColumns
    from xknxmono.models.intermediate.com_object_parameter_block_t_columns_column import ComObjectParameterBlockColumnsColumn
    from xknxmono.models.intermediate.com_object_parameter_block_t_rows import ComObjectParameterBlockRows
    from xknxmono.models.intermediate.com_object_parameter_block_t_rows_row import ComObjectParameterBlockRowsRow
    from xknxmono.models.intermediate.com_object_priority_t import ComObjectPriority
    from xknxmono.models.intermediate.com_object_ref_ref_t import ComObjectRefRef
    from xknxmono.models.intermediate.com_object_ref_t import ComObjectRef
    from xknxmono.models.intermediate.com_object_security_requirements_t import ComObjectSecurityRequirements
    from xknxmono.models.intermediate.com_object_size_t import ComObjectSize
    from xknxmono.models.intermediate.com_object_t import ComObject
    from xknxmono.models.intermediate.com_table_expectation_t import ComTableExpectation
    from xknxmono.models.intermediate.completion_status_t import CompletionStatus
    from xknxmono.models.intermediate.coupler_capability_t import CouplerCapability
    from xknxmono.models.intermediate.datapoint_role_t import DatapointRole
    from xknxmono.models.intermediate.datapoint_type_t import DatapointType
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes import DatapointTypeDatapointSubtypes
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype import DatapointTypeDatapointSubtypesDatapointSubtype
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format import DatapointTypeDatapointSubtypesDatapointSubtypeFormat
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_bit import DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration import DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration_enum_value import DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumerationEnumValue
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_float import DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_ref_type import DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_reserved import DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_signed_integer import DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_string import DatapointTypeDatapointSubtypesDatapointSubtypeFormatString
    from xknxmono.models.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_unsigned_integer import DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger
    from xknxmono.models.intermediate.dependent_channel_choose_t import DependentChannelChoose
    from xknxmono.models.intermediate.dependent_channel_choose_t import DependentChannelChooseWhen
    from xknxmono.models.intermediate.deprecation_status_t import DeprecationStatus
    from xknxmono.models.intermediate.device_certificate_t import DeviceCertificate
    from xknxmono.models.intermediate.device_instance_ref_t import DeviceInstanceRef
    from xknxmono.models.intermediate.device_instance_t import DeviceInstance
    from xknxmono.models.intermediate.device_instance_t_additional_addresses import DeviceInstanceAdditionalAddresses
    from xknxmono.models.intermediate.device_instance_t_additional_addresses_address import DeviceInstanceAdditionalAddressesAddress
    from xknxmono.models.intermediate.device_instance_t_binary_data import DeviceInstanceBinaryData
    from xknxmono.models.intermediate.device_instance_t_binary_data_binary_data import DeviceInstanceBinaryDataBinaryData
    from xknxmono.models.intermediate.device_instance_t_bus_interfaces import DeviceInstanceBusInterfaces
    from xknxmono.models.intermediate.device_instance_t_channel_instances import DeviceInstanceChannelInstances
    from xknxmono.models.intermediate.device_instance_t_com_object_instance_refs import DeviceInstanceComObjectInstanceRefs
    from xknxmono.models.intermediate.device_instance_t_group_object_tree import DeviceInstanceGroupObjectTree
    from xknxmono.models.intermediate.device_instance_t_group_object_tree_nodes import DeviceInstanceGroupObjectTreeNodes
    from xknxmono.models.intermediate.device_instance_t_module_instances import DeviceInstanceModuleInstances
    from xknxmono.models.intermediate.device_instance_t_parameter_instance_refs import DeviceInstanceParameterInstanceRefs
    from xknxmono.models.intermediate.device_instance_t_rf_fast_ack_slots import DeviceInstanceRfFastAckSlots
    from xknxmono.models.intermediate.device_instance_t_rf_fast_ack_slots_slot import DeviceInstanceRfFastAckSlotsSlot
    from xknxmono.models.intermediate.download_behavior_t import DownloadBehavior
    from xknxmono.models.intermediate.enable_t import Enable
    from xknxmono.models.intermediate.fixup_t import Fixup
    from xknxmono.models.intermediate.function_t import Function
    from xknxmono.models.intermediate.function_type_t import FunctionType
    from xknxmono.models.intermediate.function_type_t_function_point import FunctionTypeFunctionPoint
    from xknxmono.models.intermediate.functions_group_t import FunctionsGroup
    from xknxmono.models.intermediate.group_address_ref_t import GroupAddressRef
    from xknxmono.models.intermediate.group_address_style_t import GroupAddressStyle
    from xknxmono.models.intermediate.group_address_t import GroupAddress
    from xknxmono.models.intermediate.group_addresses_t import GroupAddresses
    from xknxmono.models.intermediate.group_addresses_t_group_ranges import GroupAddressesGroupRanges
    from xknxmono.models.intermediate.group_range_t import GroupRange
    from xknxmono.models.intermediate.hardware2_program_t import Hardware2Program
    from xknxmono.models.intermediate.hardware_t import Hardware
    from xknxmono.models.intermediate.hardware_t_hardware2_programs import HardwareHardware2Programs
    from xknxmono.models.intermediate.hardware_t_products import HardwareProducts
    from xknxmono.models.intermediate.hardware_t_products_product import HardwareProductsProduct
    from xknxmono.models.intermediate.hardware_t_products_product_attributes import HardwareProductsProductAttributes
    from xknxmono.models.intermediate.hardware_t_products_product_attributes_attribute import HardwareProductsProductAttributesAttribute
    from xknxmono.models.intermediate.hardware_t_products_product_attributes_attribute_name import HardwareProductsProductAttributesAttributeName
    from xknxmono.models.intermediate.hardware_t_products_product_baggages import HardwareProductsProductBaggages
    from xknxmono.models.intermediate.hardware_t_products_product_baggages_baggage import HardwareProductsProductBaggagesBaggage
    from xknxmono.models.intermediate.hawk_configuration_data_t import HawkConfigurationData
    from xknxmono.models.intermediate.hawk_configuration_data_t_features import HawkConfigurationDataFeatures
    from xknxmono.models.intermediate.hawk_configuration_data_t_features_feature import HawkConfigurationDataFeaturesFeature
    from xknxmono.models.intermediate.hawk_configuration_data_t_features_feature_name import HawkConfigurationDataFeaturesFeatureName
    from xknxmono.models.intermediate.hawk_configuration_data_t_interface_objects import HawkConfigurationDataInterfaceObjects
    from xknxmono.models.intermediate.hawk_configuration_data_t_interface_objects_interface_object import HawkConfigurationDataInterfaceObjectsInterfaceObject
    from xknxmono.models.intermediate.hawk_configuration_data_t_interface_objects_interface_object_property import HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty
    from xknxmono.models.intermediate.hawk_configuration_data_t_memory_segments import HawkConfigurationDataMemorySegments
    from xknxmono.models.intermediate.hawk_configuration_data_t_memory_segments_memory_segment import HawkConfigurationDataMemorySegmentsMemorySegment
    from xknxmono.models.intermediate.hawk_configuration_data_t_memory_segments_memory_segment_access_rights import HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights
    from xknxmono.models.intermediate.hawk_configuration_data_t_procedures import HawkConfigurationDataProcedures
    from xknxmono.models.intermediate.hawk_configuration_data_t_procedures_procedure import HawkConfigurationDataProceduresProcedure
    from xknxmono.models.intermediate.hawk_configuration_data_t_procedures_procedure_value import HawkConfigurationDataProceduresProcedureValue
    from xknxmono.models.intermediate.hawk_configuration_data_t_resources import HawkConfigurationDataResources
    from xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource import HawkConfigurationDataResourcesResource
    from xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource_access_rights import HawkConfigurationDataResourcesResourceAccessRights
    from xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource_resource_type import HawkConfigurationDataResourcesResourceResourceType
    from xknxmono.models.intermediate.hawk_configuration_data_t_resources_resource_resource_type_flavour import HawkConfigurationDataResourcesResourceResourceTypeFlavour
    from xknxmono.models.intermediate.horizontal_alignment_t import HorizontalAlignment
    from xknxmono.models.intermediate.io_tpoint_parameter_t import IoPointParameter
    from xknxmono.models.intermediate.ipconfig_assign_t import IpconfigAssign
    from xknxmono.models.intermediate.ipconfig_t import Ipconfig
    from xknxmono.models.intermediate.knx import Knx
    from xknxmono.models.intermediate.language_data_t import LanguageData
    from xknxmono.models.intermediate.language_data_t_translation_unit import LanguageDataTranslationUnit
    from xknxmono.models.intermediate.language_data_t_translation_unit_translation_element import LanguageDataTranslationUnitTranslationElement
    from xknxmono.models.intermediate.language_data_t_translation_unit_translation_element_translation import LanguageDataTranslationUnitTranslationElementTranslation
    from xknxmono.models.intermediate.ld_ctrl_abs_segment_t import LdCtrlAbsSegment
    from xknxmono.models.intermediate.ld_ctrl_base_choose_t import LdCtrlBaseChoose
    from xknxmono.models.intermediate.ld_ctrl_base_choose_t import LdCtrlBaseChooseWhen
    from xknxmono.models.intermediate.ld_ctrl_base_t import LdCtrlBase
    from xknxmono.models.intermediate.ld_ctrl_base_t_on_error import LdCtrlBaseOnError
    from xknxmono.models.intermediate.ld_ctrl_clear_cached_object_types_t import LdCtrlClearCachedObjectTypes
    from xknxmono.models.intermediate.ld_ctrl_clear_lcfilter_table_t import LdCtrlClearLcfilterTable
    from xknxmono.models.intermediate.ld_ctrl_compare_base_t import LdCtrlCompareBase
    from xknxmono.models.intermediate.ld_ctrl_compare_mem_t import LdCtrlCompareMem
    from xknxmono.models.intermediate.ld_ctrl_compare_prop_t import LdCtrlCompareProp
    from xknxmono.models.intermediate.ld_ctrl_compare_rel_mem_t import LdCtrlCompareRelMem
    from xknxmono.models.intermediate.ld_ctrl_connect_t import LdCtrlConnect
    from xknxmono.models.intermediate.ld_ctrl_control_variable_t import LdCtrlControlVariable
    from xknxmono.models.intermediate.ld_ctrl_declare_prop_desc_t import LdCtrlDeclarePropDesc
    from xknxmono.models.intermediate.ld_ctrl_delay_t import LdCtrlDelay
    from xknxmono.models.intermediate.ld_ctrl_disconnect_t import LdCtrlDisconnect
    from xknxmono.models.intermediate.ld_ctrl_error_cause_t import LdCtrlErrorCause
    from xknxmono.models.intermediate.ld_ctrl_invoke_function_prop_t import LdCtrlInvokeFunctionProp
    from xknxmono.models.intermediate.ld_ctrl_load_completed_t import LdCtrlLoadCompleted
    from xknxmono.models.intermediate.ld_ctrl_load_image_mem_t import LdCtrlLoadImageMem
    from xknxmono.models.intermediate.ld_ctrl_load_image_prop_t import LdCtrlLoadImageProp
    from xknxmono.models.intermediate.ld_ctrl_load_image_rel_mem_t import LdCtrlLoadImageRelMem
    from xknxmono.models.intermediate.ld_ctrl_load_t import LdCtrlLoad
    from xknxmono.models.intermediate.ld_ctrl_map_error_t import LdCtrlMapError
    from xknxmono.models.intermediate.ld_ctrl_master_reset_t import LdCtrlMasterReset
    from xknxmono.models.intermediate.ld_ctrl_max_length_t import LdCtrlMaxLength
    from xknxmono.models.intermediate.ld_ctrl_mem_addr_space_t import LdCtrlMemAddrSpace
    from xknxmono.models.intermediate.ld_ctrl_merge_t import LdCtrlMerge
    from xknxmono.models.intermediate.ld_ctrl_proc_type_t import LdCtrlProcType
    from xknxmono.models.intermediate.ld_ctrl_progress_text_t import LdCtrlProgressText
    from xknxmono.models.intermediate.ld_ctrl_read_function_prop_t import LdCtrlReadFunctionProp
    from xknxmono.models.intermediate.ld_ctrl_rel_segment_t import LdCtrlRelSegment
    from xknxmono.models.intermediate.ld_ctrl_restart_t import LdCtrlRestart
    from xknxmono.models.intermediate.ld_ctrl_set_control_variable_t import LdCtrlSetControlVariable
    from xknxmono.models.intermediate.ld_ctrl_task_ctrl1_t import LdCtrlTaskCtrl1
    from xknxmono.models.intermediate.ld_ctrl_task_ctrl2_t import LdCtrlTaskCtrl2
    from xknxmono.models.intermediate.ld_ctrl_task_ptr_t import LdCtrlTaskPtr
    from xknxmono.models.intermediate.ld_ctrl_task_segment_t import LdCtrlTaskSegment
    from xknxmono.models.intermediate.ld_ctrl_unload_t import LdCtrlUnload
    from xknxmono.models.intermediate.ld_ctrl_write_mem_t import LdCtrlWriteMem
    from xknxmono.models.intermediate.ld_ctrl_write_prop_t import LdCtrlWriteProp
    from xknxmono.models.intermediate.ld_ctrl_write_rel_mem_t import LdCtrlWriteRelMem
    from xknxmono.models.intermediate.load_procedure_style_t import LoadProcedureStyle
    from xknxmono.models.intermediate.load_procedure_t import LoadProcedure
    from xknxmono.models.intermediate.load_procedures_t import LoadProcedures
    from xknxmono.models.intermediate.load_procedures_t_load_procedure import LoadProceduresLoadProcedure
    from xknxmono.models.intermediate.locations_t import Locations
    from xknxmono.models.intermediate.manufacturer_data_t import ManufacturerData
    from xknxmono.models.intermediate.manufacturer_data_t_manufacturer import ManufacturerDataManufacturer
    from xknxmono.models.intermediate.manufacturer_data_t_manufacturer_application_programs import ManufacturerDataManufacturerApplicationPrograms
    from xknxmono.models.intermediate.manufacturer_data_t_manufacturer_baggages import ManufacturerDataManufacturerBaggages
    from xknxmono.models.intermediate.manufacturer_data_t_manufacturer_baggages_baggage import ManufacturerDataManufacturerBaggagesBaggage
    from xknxmono.models.intermediate.manufacturer_data_t_manufacturer_baggages_baggage_file_info import ManufacturerDataManufacturerBaggagesBaggageFileInfo
    from xknxmono.models.intermediate.manufacturer_data_t_manufacturer_catalog import ManufacturerDataManufacturerCatalog
    from xknxmono.models.intermediate.manufacturer_data_t_manufacturer_hardware import ManufacturerDataManufacturerHardware
    from xknxmono.models.intermediate.manufacturer_data_t_manufacturer_languages import ManufacturerDataManufacturerLanguages
    from xknxmono.models.intermediate.mask_version_t import MaskVersion
    from xknxmono.models.intermediate.mask_version_t_downward_compatible_masks import MaskVersionDownwardCompatibleMasks
    from xknxmono.models.intermediate.mask_version_t_downward_compatible_masks_downward_compatible_mask import MaskVersionDownwardCompatibleMasksDownwardCompatibleMask
    from xknxmono.models.intermediate.mask_version_t_management_model import MaskVersionManagementModel
    from xknxmono.models.intermediate.mask_version_t_mask_entries import MaskVersionMaskEntries
    from xknxmono.models.intermediate.mask_version_t_mask_entries_mask_entry import MaskVersionMaskEntriesMaskEntry
    from xknxmono.models.intermediate.master_data_t import MasterData
    from xknxmono.models.intermediate.master_data_t_datapoint_roles import MasterDataDatapointRoles
    from xknxmono.models.intermediate.master_data_t_datapoint_types import MasterDataDatapointTypes
    from xknxmono.models.intermediate.master_data_t_function_types import MasterDataFunctionTypes
    from xknxmono.models.intermediate.master_data_t_functional_blocks import MasterDataFunctionalBlocks
    from xknxmono.models.intermediate.master_data_t_functional_blocks_functional_block import MasterDataFunctionalBlocksFunctionalBlock
    from xknxmono.models.intermediate.master_data_t_functional_blocks_functional_block_parameters import MasterDataFunctionalBlocksFunctionalBlockParameters
    from xknxmono.models.intermediate.master_data_t_functional_blocks_functional_block_parameters_parameter import MasterDataFunctionalBlocksFunctionalBlockParametersParameter
    from xknxmono.models.intermediate.master_data_t_interface_object_properties import MasterDataInterfaceObjectProperties
    from xknxmono.models.intermediate.master_data_t_interface_object_properties_interface_object_property import MasterDataInterfaceObjectPropertiesInterfaceObjectProperty
    from xknxmono.models.intermediate.master_data_t_interface_object_types import MasterDataInterfaceObjectTypes
    from xknxmono.models.intermediate.master_data_t_interface_object_types_interface_object_type import MasterDataInterfaceObjectTypesInterfaceObjectType
    from xknxmono.models.intermediate.master_data_t_languages import MasterDataLanguages
    from xknxmono.models.intermediate.master_data_t_manufacturers import MasterDataManufacturers
    from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer import MasterDataManufacturersManufacturer
    from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_datapoint_roles import MasterDataManufacturersManufacturerDatapointRoles
    from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_datapoint_types import MasterDataManufacturersManufacturerDatapointTypes
    from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_function_types import MasterDataManufacturersManufacturerFunctionTypes
    from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_import_restriction import MasterDataManufacturersManufacturerImportRestriction
    from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_public_keys import MasterDataManufacturersManufacturerPublicKeys
    from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_public_keys_public_key import MasterDataManufacturersManufacturerPublicKeysPublicKey
    from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_public_keys_public_key_rsakey_value import MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue
    from xknxmono.models.intermediate.master_data_t_manufacturers_manufacturer_space_usages import MasterDataManufacturersManufacturerSpaceUsages
    from xknxmono.models.intermediate.master_data_t_mask_versions import MasterDataMaskVersions
    from xknxmono.models.intermediate.master_data_t_medium_types import MasterDataMediumTypes
    from xknxmono.models.intermediate.master_data_t_medium_types_medium_type import MasterDataMediumTypesMediumType
    from xknxmono.models.intermediate.master_data_t_product_languages import MasterDataProductLanguages
    from xknxmono.models.intermediate.master_data_t_product_languages_language import MasterDataProductLanguagesLanguage
    from xknxmono.models.intermediate.master_data_t_property_data_types import MasterDataPropertyDataTypes
    from xknxmono.models.intermediate.master_data_t_property_data_types_property_data_type import MasterDataPropertyDataTypesPropertyDataType
    from xknxmono.models.intermediate.master_data_t_space_usages import MasterDataSpaceUsages
    from xknxmono.models.intermediate.member_status_t import MemberStatus
    from xknxmono.models.intermediate.memory_parameter_t import MemoryParameter
    from xknxmono.models.intermediate.memory_type_t import MemoryType
    from xknxmono.models.intermediate.memory_union_t import MemoryUnion
    from xknxmono.models.intermediate.module_arg_t import ModuleArg
    from xknxmono.models.intermediate.module_def_arg_type_t import ModuleDefArgType
    from xknxmono.models.intermediate.module_def_dynamic_t import ModuleDefDynamic
    from xknxmono.models.intermediate.module_def_ld_ctrl_base_choose_t import ModuleDefLdCtrlBaseChoose
    from xknxmono.models.intermediate.module_def_ld_ctrl_base_choose_t_when import ModuleDefLdCtrlBaseChooseWhen
    from xknxmono.models.intermediate.module_def_ld_ctrl_compare_prop_t import ModuleDefLdCtrlCompareProp
    from xknxmono.models.intermediate.module_def_ld_ctrl_invoke_function_prop_t import ModuleDefLdCtrlInvokeFunctionProp
    from xknxmono.models.intermediate.module_def_ld_ctrl_read_function_prop_t import ModuleDefLdCtrlReadFunctionProp
    from xknxmono.models.intermediate.module_def_ld_ctrl_write_prop_t import ModuleDefLdCtrlWriteProp
    from xknxmono.models.intermediate.module_def_load_procedure_t import ModuleDefLoadProcedure
    from xknxmono.models.intermediate.module_def_load_procedures_t import ModuleDefLoadProcedures
    from xknxmono.models.intermediate.module_def_static_t import ModuleDefStatic
    from xknxmono.models.intermediate.module_def_static_t_allocators import ModuleDefStaticAllocators
    from xknxmono.models.intermediate.module_def_static_t_com_object_refs import ModuleDefStaticComObjectRefs
    from xknxmono.models.intermediate.module_def_static_t_com_objects import ModuleDefStaticComObjects
    from xknxmono.models.intermediate.module_def_static_t_com_objects_com_object import ModuleDefStaticComObjectsComObject
    from xknxmono.models.intermediate.module_def_static_t_parameter_calculations import ModuleDefStaticParameterCalculations
    from xknxmono.models.intermediate.module_def_static_t_parameter_refs import ModuleDefStaticParameterRefs
    from xknxmono.models.intermediate.module_def_static_t_parameter_validations import ModuleDefStaticParameterValidations
    from xknxmono.models.intermediate.module_def_static_t_parameters import ModuleDefStaticParameters
    from xknxmono.models.intermediate.module_def_static_t_parameters_parameter import ModuleDefStaticParametersParameter
    from xknxmono.models.intermediate.module_def_static_t_parameters_parameter_memory import ModuleDefStaticParametersParameterMemory
    from xknxmono.models.intermediate.module_def_static_t_parameters_parameter_property import ModuleDefStaticParametersParameterProperty
    from xknxmono.models.intermediate.module_def_static_t_parameters_union import ModuleDefStaticParametersUnion
    from xknxmono.models.intermediate.module_def_static_t_parameters_union_memory import ModuleDefStaticParametersUnionMemory
    from xknxmono.models.intermediate.module_def_static_t_parameters_union_property import ModuleDefStaticParametersUnionProperty
    from xknxmono.models.intermediate.module_def_t import ModuleDef
    from xknxmono.models.intermediate.module_def_t import ModuleDefSubModuleDefs
    from xknxmono.models.intermediate.module_def_t_arguments import ModuleDefArguments
    from xknxmono.models.intermediate.module_def_t_arguments_argument import ModuleDefArgumentsArgument
    from xknxmono.models.intermediate.module_def_t_arguments_argument_alignment import ModuleDefArgumentsArgumentAlignment
    from xknxmono.models.intermediate.module_instance_t import ModuleInstance
    from xknxmono.models.intermediate.module_instance_t_arguments import ModuleInstanceArguments
    from xknxmono.models.intermediate.module_instance_t_arguments_argument import ModuleInstanceArgumentsArgument
    from xknxmono.models.intermediate.module_t import Module
    from xknxmono.models.intermediate.module_t_numeric_arg import ModuleNumericArg
    from xknxmono.models.intermediate.module_t_text_arg import ModuleTextArg
    from xknxmono.models.intermediate.node_t import Node
    from xknxmono.models.intermediate.node_t import NodeNodes
    from xknxmono.models.intermediate.node_t_type import NodeType
    from xknxmono.models.intermediate.p2_plink_bus_interface_endpoint_t import P2PlinkBusInterfaceEndpoint
    from xknxmono.models.intermediate.p2_plink_device_endpoint_t import P2PlinkDeviceEndpoint
    from xknxmono.models.intermediate.p2_plink_endpoint_t import P2PlinkEndpoint
    from xknxmono.models.intermediate.p2_plinks_t import P2Plinks
    from xknxmono.models.intermediate.p2_plinks_t_p2_plink import P2PlinksP2Plink
    from xknxmono.models.intermediate.parameter_base_t import ParameterBase
    from xknxmono.models.intermediate.parameter_block_layout_t import ParameterBlockLayout
    from xknxmono.models.intermediate.parameter_calculation_t import ParameterCalculation
    from xknxmono.models.intermediate.parameter_calculation_t_language import ParameterCalculationLanguage
    from xknxmono.models.intermediate.parameter_calculation_t_lparameters import ParameterCalculationLparameters
    from xknxmono.models.intermediate.parameter_calculation_t_rparameters import ParameterCalculationRparameters
    from xknxmono.models.intermediate.parameter_instance_ref_t import ParameterInstanceRef
    from xknxmono.models.intermediate.parameter_ref_ref_t import ParameterRefRef
    from xknxmono.models.intermediate.parameter_ref_t import ParameterRef
    from xknxmono.models.intermediate.parameter_separator_t import ParameterSeparator
    from xknxmono.models.intermediate.parameter_separator_t_uihint import ParameterSeparatorUihint
    from xknxmono.models.intermediate.parameter_type_t import ParameterType
    from xknxmono.models.intermediate.parameter_type_t_type_color import ParameterTypeTypeColor
    from xknxmono.models.intermediate.parameter_type_t_type_color_space import ParameterTypeTypeColorSpace
    from xknxmono.models.intermediate.parameter_type_t_type_date import ParameterTypeTypeDate
    from xknxmono.models.intermediate.parameter_type_t_type_date_encoding import ParameterTypeTypeDateEncoding
    from xknxmono.models.intermediate.parameter_type_t_type_float import ParameterTypeTypeFloat
    from xknxmono.models.intermediate.parameter_type_t_type_float_encoding import ParameterTypeTypeFloatEncoding
    from xknxmono.models.intermediate.parameter_type_t_type_float_uihint import ParameterTypeTypeFloatUihint
    from xknxmono.models.intermediate.parameter_type_t_type_ipaddress import ParameterTypeTypeIpaddress
    from xknxmono.models.intermediate.parameter_type_t_type_ipaddress_address_type import ParameterTypeTypeIpaddressAddressType
    from xknxmono.models.intermediate.parameter_type_t_type_ipaddress_version import ParameterTypeTypeIpaddressVersion
    from xknxmono.models.intermediate.parameter_type_t_type_number import ParameterTypeTypeNumber
    from xknxmono.models.intermediate.parameter_type_t_type_number_type import ParameterTypeTypeNumberType
    from xknxmono.models.intermediate.parameter_type_t_type_number_uihint import ParameterTypeTypeNumberUihint
    from xknxmono.models.intermediate.parameter_type_t_type_picture import ParameterTypeTypePicture
    from xknxmono.models.intermediate.parameter_type_t_type_raw_data import ParameterTypeTypeRawData
    from xknxmono.models.intermediate.parameter_type_t_type_restriction import ParameterTypeTypeRestriction
    from xknxmono.models.intermediate.parameter_type_t_type_restriction_base import ParameterTypeTypeRestrictionBase
    from xknxmono.models.intermediate.parameter_type_t_type_restriction_enumeration import ParameterTypeTypeRestrictionEnumeration
    from xknxmono.models.intermediate.parameter_type_t_type_restriction_uihint import ParameterTypeTypeRestrictionUihint
    from xknxmono.models.intermediate.parameter_type_t_type_text import ParameterTypeTypeText
    from xknxmono.models.intermediate.parameter_type_t_type_time import ParameterTypeTypeTime
    from xknxmono.models.intermediate.parameter_type_t_type_time_uihint import ParameterTypeTypeTimeUihint
    from xknxmono.models.intermediate.parameter_type_t_type_time_unit import ParameterTypeTypeTimeUnit
    from xknxmono.models.intermediate.parameter_validation_t import ParameterValidation
    from xknxmono.models.intermediate.parameter_validation_t_parameters import ParameterValidationParameters
    from xknxmono.models.intermediate.procedure_type_t import ProcedureType
    from xknxmono.models.intermediate.project_t import Project
    from xknxmono.models.intermediate.project_t_addin_data import ProjectAddinData
    from xknxmono.models.intermediate.project_t_installations import ProjectInstallations
    from xknxmono.models.intermediate.project_t_installations_installation import ProjectInstallationsInstallation
    from xknxmono.models.intermediate.project_t_installations_installation_split_type import ProjectInstallationsInstallationSplitType
    from xknxmono.models.intermediate.project_t_project_information import ProjectProjectInformation
    from xknxmono.models.intermediate.project_t_project_information_device_certificates import ProjectProjectInformationDeviceCertificates
    from xknxmono.models.intermediate.project_t_project_information_history_entries import ProjectProjectInformationHistoryEntries
    from xknxmono.models.intermediate.project_t_project_information_history_entries_history_entry import ProjectProjectInformationHistoryEntriesHistoryEntry
    from xknxmono.models.intermediate.project_t_project_information_project_traces import ProjectProjectInformationProjectTraces
    from xknxmono.models.intermediate.project_t_project_information_tags import ProjectProjectInformationTags
    from xknxmono.models.intermediate.project_t_project_information_tags_tag import ProjectProjectInformationTagsTag
    from xknxmono.models.intermediate.project_t_project_information_to_do_items import ProjectProjectInformationToDoItems
    from xknxmono.models.intermediate.project_t_user_files import ProjectUserFiles
    from xknxmono.models.intermediate.project_trace_t import ProjectTrace
    from xknxmono.models.intermediate.project_tracing_level_t import ProjectTracingLevel
    from xknxmono.models.intermediate.project_type_t import ProjectType
    from xknxmono.models.intermediate.prop_type_t import PropType
    from xknxmono.models.intermediate.property_parameter_t import PropertyParameter
    from xknxmono.models.intermediate.property_union_t import PropertyUnion
    from xknxmono.models.intermediate.registration_info_t import RegistrationInfo
    from xknxmono.models.intermediate.registration_info_t_registration_key import RegistrationInfoRegistrationKey
    from xknxmono.models.intermediate.registration_status_t import RegistrationStatus
    from xknxmono.models.intermediate.rename_t import Rename
    from xknxmono.models.intermediate.resource_access_rights_t import ResourceAccessRights
    from xknxmono.models.intermediate.resource_access_t import ResourceAccess
    from xknxmono.models.intermediate.resource_addr_space_t import ResourceAddrSpace
    from xknxmono.models.intermediate.resource_location_t import ResourceLocation
    from xknxmono.models.intermediate.resource_mgmt_style_t import ResourceMgmtStyle
    from xknxmono.models.intermediate.resource_name_t import ResourceName
    from xknxmono.models.intermediate.rfdevice_mode_t import RfdeviceMode
    from xknxmono.models.intermediate.rfrx_capabilities_t import RfrxCapabilities
    from xknxmono.models.intermediate.rftx_capabilities_t import RftxCapabilities
    from xknxmono.models.intermediate.security_mode_t import SecurityMode
    from xknxmono.models.intermediate.security_t import Security
    from xknxmono.models.intermediate.segment_base_t import SegmentBase
    from xknxmono.models.intermediate.space_t import Space
    from xknxmono.models.intermediate.space_type_t import SpaceType
    from xknxmono.models.intermediate.space_usage_t import SpaceUsage
    from xknxmono.models.intermediate.split_info_t import SplitInfo
    from xknxmono.models.intermediate.split_infos_t import SplitInfos
    from xknxmono.models.intermediate.text_alignment_t import TextAlignment
    from xknxmono.models.intermediate.text_encoding_t import TextEncoding
    from xknxmono.models.intermediate.to_do_item_t import ToDoItem
    from xknxmono.models.intermediate.to_do_status_t import ToDoStatus
    from xknxmono.models.intermediate.topology_t import Topology
    from xknxmono.models.intermediate.topology_t_area import TopologyArea
    from xknxmono.models.intermediate.topology_t_area_line import TopologyAreaLine
    from xknxmono.models.intermediate.topology_t_area_line_segment import TopologyAreaLineSegment
    from xknxmono.models.intermediate.topology_t_area_line_segment_additional_group_addresses import TopologyAreaLineSegmentAdditionalGroupAddresses
    from xknxmono.models.intermediate.topology_t_area_line_segment_additional_group_addresses_group_address import TopologyAreaLineSegmentAdditionalGroupAddressesGroupAddress
    from xknxmono.models.intermediate.topology_t_unassigned_devices import TopologyUnassignedDevices
    from xknxmono.models.intermediate.trade_t import Trade
    from xknxmono.models.intermediate.trades_t import Trades
    from xknxmono.models.intermediate.union_parameter_t import UnionParameter
    from xknxmono.models.intermediate.user_file_t import UserFile
    from xknxmono.models.intermediate.when_t import When


def __getattr__(name: str) -> object:
    if name in _LAZY:
        import importlib
        module_path, attr = _LAZY[name]
        mod = importlib.import_module(module_path)
        value = getattr(mod, attr)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
