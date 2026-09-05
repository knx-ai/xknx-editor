from __future__ import annotations

from typing import TYPE_CHECKING

_LAZY: dict[str, tuple[str, str]] = {
    "Access": ("xknxeditor.namespaces.intermediate.access_t", "Access"),
    "AddinData": ("xknxeditor.namespaces.intermediate.addin_data_t", "AddinData"),
    "Allocator": ("xknxeditor.namespaces.intermediate.allocator_t", "Allocator"),
    "ApplicationProgramChannel": ("xknxeditor.namespaces.intermediate.application_program_channel_t", "ApplicationProgramChannel"),
    "ChannelChoose": ("xknxeditor.namespaces.intermediate.application_program_channel_t", "ChannelChoose"),
    "ChannelChooseWhen": ("xknxeditor.namespaces.intermediate.application_program_channel_t", "ChannelChooseWhen"),
    "ComObjectParameterBlock": ("xknxeditor.namespaces.intermediate.application_program_channel_t", "ComObjectParameterBlock"),
    "ComObjectParameterChoose": ("xknxeditor.namespaces.intermediate.application_program_channel_t", "ComObjectParameterChoose"),
    "ComObjectParameterChooseWhen": ("xknxeditor.namespaces.intermediate.application_program_channel_t", "ComObjectParameterChooseWhen"),
    "Repeat": ("xknxeditor.namespaces.intermediate.application_program_channel_t", "Repeat"),
    "ApplicationProgramDynamic": ("xknxeditor.namespaces.intermediate.application_program_dynamic_t", "ApplicationProgramDynamic"),
    "ApplicationProgramIpconfig": ("xknxeditor.namespaces.intermediate.application_program_ipconfig_t", "ApplicationProgramIpconfig"),
    "ApplicationProgramRef": ("xknxeditor.namespaces.intermediate.application_program_ref_t", "ApplicationProgramRef"),
    "ApplicationProgramStatic": ("xknxeditor.namespaces.intermediate.application_program_static_t", "ApplicationProgramStatic"),
    "ApplicationProgramStaticAddressTable": ("xknxeditor.namespaces.intermediate.application_program_static_t_address_table", "ApplicationProgramStaticAddressTable"),
    "ApplicationProgramStaticAllocators": ("xknxeditor.namespaces.intermediate.application_program_static_t_allocators", "ApplicationProgramStaticAllocators"),
    "ApplicationProgramStaticAssociationTable": ("xknxeditor.namespaces.intermediate.application_program_static_t_association_table", "ApplicationProgramStaticAssociationTable"),
    "ApplicationProgramStaticBinaryData": ("xknxeditor.namespaces.intermediate.application_program_static_t_binary_data", "ApplicationProgramStaticBinaryData"),
    "ApplicationProgramStaticBusInterfaces": ("xknxeditor.namespaces.intermediate.application_program_static_t_bus_interfaces", "ApplicationProgramStaticBusInterfaces"),
    "ApplicationProgramStaticBusInterfacesBusInterface": ("xknxeditor.namespaces.intermediate.application_program_static_t_bus_interfaces_bus_interface", "ApplicationProgramStaticBusInterfacesBusInterface"),
    "ApplicationProgramStaticBusInterfacesBusInterfaceAccessType": ("xknxeditor.namespaces.intermediate.application_program_static_t_bus_interfaces_bus_interface_access_type", "ApplicationProgramStaticBusInterfacesBusInterfaceAccessType"),
    "ApplicationProgramStaticCode": ("xknxeditor.namespaces.intermediate.application_program_static_t_code", "ApplicationProgramStaticCode"),
    "ApplicationProgramStaticCodeAbsoluteSegment": ("xknxeditor.namespaces.intermediate.application_program_static_t_code_absolute_segment", "ApplicationProgramStaticCodeAbsoluteSegment"),
    "ApplicationProgramStaticCodeRelativeSegment": ("xknxeditor.namespaces.intermediate.application_program_static_t_code_relative_segment", "ApplicationProgramStaticCodeRelativeSegment"),
    "ApplicationProgramStaticComObjectRefs": ("xknxeditor.namespaces.intermediate.application_program_static_t_com_object_refs", "ApplicationProgramStaticComObjectRefs"),
    "ApplicationProgramStaticComObjectTable": ("xknxeditor.namespaces.intermediate.application_program_static_t_com_object_table", "ApplicationProgramStaticComObjectTable"),
    "ApplicationProgramStaticDeviceCompare": ("xknxeditor.namespaces.intermediate.application_program_static_t_device_compare", "ApplicationProgramStaticDeviceCompare"),
    "ApplicationProgramStaticDeviceCompareExcludeMemory": ("xknxeditor.namespaces.intermediate.application_program_static_t_device_compare_exclude_memory", "ApplicationProgramStaticDeviceCompareExcludeMemory"),
    "ApplicationProgramStaticDeviceCompareExcludeProperty": ("xknxeditor.namespaces.intermediate.application_program_static_t_device_compare_exclude_property", "ApplicationProgramStaticDeviceCompareExcludeProperty"),
    "ApplicationProgramStaticExtension": ("xknxeditor.namespaces.intermediate.application_program_static_t_extension", "ApplicationProgramStaticExtension"),
    "ApplicationProgramStaticExtensionBaggage": ("xknxeditor.namespaces.intermediate.application_program_static_t_extension_baggage", "ApplicationProgramStaticExtensionBaggage"),
    "ApplicationProgramStaticFixupList": ("xknxeditor.namespaces.intermediate.application_program_static_t_fixup_list", "ApplicationProgramStaticFixupList"),
    "ApplicationProgramStaticMessages": ("xknxeditor.namespaces.intermediate.application_program_static_t_messages", "ApplicationProgramStaticMessages"),
    "ApplicationProgramStaticMessagesMessage": ("xknxeditor.namespaces.intermediate.application_program_static_t_messages_message", "ApplicationProgramStaticMessagesMessage"),
    "ApplicationProgramStaticOptions": ("xknxeditor.namespaces.intermediate.application_program_static_t_options", "ApplicationProgramStaticOptions"),
    "ApplicationProgramStaticOptionsCustomerAdjustableParameters": ("xknxeditor.namespaces.intermediate.application_program_static_t_options_customer_adjustable_parameters", "ApplicationProgramStaticOptionsCustomerAdjustableParameters"),
    "ApplicationProgramStaticOptionsNotLoadable": ("xknxeditor.namespaces.intermediate.application_program_static_t_options_not_loadable", "ApplicationProgramStaticOptionsNotLoadable"),
    "ApplicationProgramStaticOptionsParameterByteOrder": ("xknxeditor.namespaces.intermediate.application_program_static_t_options_parameter_byte_order", "ApplicationProgramStaticOptionsParameterByteOrder"),
    "TextEncodingSelector": ("xknxeditor.namespaces.intermediate.application_program_static_t_options_text_parameter_encoding_selector", "TextEncodingSelector"),
    "ApplicationProgramStaticParameterCalculations": ("xknxeditor.namespaces.intermediate.application_program_static_t_parameter_calculations", "ApplicationProgramStaticParameterCalculations"),
    "ApplicationProgramStaticParameterRefs": ("xknxeditor.namespaces.intermediate.application_program_static_t_parameter_refs", "ApplicationProgramStaticParameterRefs"),
    "ApplicationProgramStaticParameterTypes": ("xknxeditor.namespaces.intermediate.application_program_static_t_parameter_types", "ApplicationProgramStaticParameterTypes"),
    "ApplicationProgramStaticParameterValidations": ("xknxeditor.namespaces.intermediate.application_program_static_t_parameter_validations", "ApplicationProgramStaticParameterValidations"),
    "ApplicationProgramStaticParameters": ("xknxeditor.namespaces.intermediate.application_program_static_t_parameters", "ApplicationProgramStaticParameters"),
    "ApplicationProgramStaticParametersParameter": ("xknxeditor.namespaces.intermediate.application_program_static_t_parameters_parameter", "ApplicationProgramStaticParametersParameter"),
    "ApplicationProgramStaticParametersUnion": ("xknxeditor.namespaces.intermediate.application_program_static_t_parameters_union", "ApplicationProgramStaticParametersUnion"),
    "ApplicationProgramStaticScript": ("xknxeditor.namespaces.intermediate.application_program_static_t_script", "ApplicationProgramStaticScript"),
    "ApplicationProgramStaticSecurityRoles": ("xknxeditor.namespaces.intermediate.application_program_static_t_security_roles", "ApplicationProgramStaticSecurityRoles"),
    "ApplicationProgramStaticSecurityRolesSecurityRole": ("xknxeditor.namespaces.intermediate.application_program_static_t_security_roles_security_role", "ApplicationProgramStaticSecurityRolesSecurityRole"),
    "ApplicationProgram": ("xknxeditor.namespaces.intermediate.application_program_t", "ApplicationProgram"),
    "ApplicationProgramCloudConnect": ("xknxeditor.namespaces.intermediate.application_program_t_cloud_connect", "ApplicationProgramCloudConnect"),
    "ApplicationProgramMinEtsVersion": ("xknxeditor.namespaces.intermediate.application_program_t_min_ets_version", "ApplicationProgramMinEtsVersion"),
    "ApplicationProgramModuleDefs": ("xknxeditor.namespaces.intermediate.application_program_t_module_defs", "ApplicationProgramModuleDefs"),
    "ApplicationProgramProfile": ("xknxeditor.namespaces.intermediate.application_program_t_profile", "ApplicationProgramProfile"),
    "ApplicationProgramProfileIo": ("xknxeditor.namespaces.intermediate.application_program_t_profile_io_t", "ApplicationProgramProfileIo"),
    "ApplicationProgramType": ("xknxeditor.namespaces.intermediate.application_program_type_t", "ApplicationProgramType"),
    "Assign": ("xknxeditor.namespaces.intermediate.assign_t", "Assign"),
    "BinaryDataRef": ("xknxeditor.namespaces.intermediate.binary_data_ref_t", "BinaryDataRef"),
    "BinaryData": ("xknxeditor.namespaces.intermediate.binary_data_t", "BinaryData"),
    "BusAccess": ("xknxeditor.namespaces.intermediate.bus_access_t", "BusAccess"),
    "BusInterface": ("xknxeditor.namespaces.intermediate.bus_interface_t", "BusInterface"),
    "BusInterfaceConnectors": ("xknxeditor.namespaces.intermediate.bus_interface_t_connectors", "BusInterfaceConnectors"),
    "BusInterfaceConnectorsConnector": ("xknxeditor.namespaces.intermediate.bus_interface_t_connectors_connector", "BusInterfaceConnectorsConnector"),
    "Button": ("xknxeditor.namespaces.intermediate.button_t", "Button"),
    "ButtonEventHandlerOnline": ("xknxeditor.namespaces.intermediate.button_t_event_handler_online", "ButtonEventHandlerOnline"),
    "CalculationParameterRef": ("xknxeditor.namespaces.intermediate.calculation_parameter_ref_t", "CalculationParameterRef"),
    "Capability": ("xknxeditor.namespaces.intermediate.capability_t", "Capability"),
    "CatalogSection": ("xknxeditor.namespaces.intermediate.catalog_section_t", "CatalogSection"),
    "CatalogSectionCatalogItem": ("xknxeditor.namespaces.intermediate.catalog_section_t_catalog_item", "CatalogSectionCatalogItem"),
    "ChannelIndependentBlock": ("xknxeditor.namespaces.intermediate.channel_independent_block_t", "ChannelIndependentBlock"),
    "ChannelInstance": ("xknxeditor.namespaces.intermediate.channel_instance_t", "ChannelInstance"),
    "ComObjectInstanceRef": ("xknxeditor.namespaces.intermediate.com_object_instance_ref_t", "ComObjectInstanceRef"),
    "ComObjectParameterBlockColumns": ("xknxeditor.namespaces.intermediate.com_object_parameter_block_t_columns", "ComObjectParameterBlockColumns"),
    "ComObjectParameterBlockColumnsColumn": ("xknxeditor.namespaces.intermediate.com_object_parameter_block_t_columns_column", "ComObjectParameterBlockColumnsColumn"),
    "ComObjectParameterBlockRows": ("xknxeditor.namespaces.intermediate.com_object_parameter_block_t_rows", "ComObjectParameterBlockRows"),
    "ComObjectParameterBlockRowsRow": ("xknxeditor.namespaces.intermediate.com_object_parameter_block_t_rows_row", "ComObjectParameterBlockRowsRow"),
    "ComObjectPriority": ("xknxeditor.namespaces.intermediate.com_object_priority_t", "ComObjectPriority"),
    "ComObjectRefRef": ("xknxeditor.namespaces.intermediate.com_object_ref_ref_t", "ComObjectRefRef"),
    "ComObjectRef": ("xknxeditor.namespaces.intermediate.com_object_ref_t", "ComObjectRef"),
    "ComObjectSecurityRequirements": ("xknxeditor.namespaces.intermediate.com_object_security_requirements_t", "ComObjectSecurityRequirements"),
    "ComObjectSize": ("xknxeditor.namespaces.intermediate.com_object_size_t", "ComObjectSize"),
    "ComObject": ("xknxeditor.namespaces.intermediate.com_object_t", "ComObject"),
    "ComTableExpectation": ("xknxeditor.namespaces.intermediate.com_table_expectation_t", "ComTableExpectation"),
    "CompletionStatus": ("xknxeditor.namespaces.intermediate.completion_status_t", "CompletionStatus"),
    "CouplerCapability": ("xknxeditor.namespaces.intermediate.coupler_capability_t", "CouplerCapability"),
    "DatapointRole": ("xknxeditor.namespaces.intermediate.datapoint_role_t", "DatapointRole"),
    "DatapointType": ("xknxeditor.namespaces.intermediate.datapoint_type_t", "DatapointType"),
    "DatapointTypeDatapointSubtypes": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes", "DatapointTypeDatapointSubtypes"),
    "DatapointTypeDatapointSubtypesDatapointSubtype": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype", "DatapointTypeDatapointSubtypesDatapointSubtype"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormat": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format", "DatapointTypeDatapointSubtypesDatapointSubtypeFormat"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_bit", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumerationEnumValue": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration_enum_value", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumerationEnumValue"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_float", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_ref_type", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_reserved", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_signed_integer", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatString": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_string", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatString"),
    "DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger": ("xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_unsigned_integer", "DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger"),
    "DependentChannelChoose": ("xknxeditor.namespaces.intermediate.dependent_channel_choose_t", "DependentChannelChoose"),
    "DependentChannelChooseWhen": ("xknxeditor.namespaces.intermediate.dependent_channel_choose_t", "DependentChannelChooseWhen"),
    "DeprecationStatus": ("xknxeditor.namespaces.intermediate.deprecation_status_t", "DeprecationStatus"),
    "DeviceCertificate": ("xknxeditor.namespaces.intermediate.device_certificate_t", "DeviceCertificate"),
    "DeviceInstanceRef": ("xknxeditor.namespaces.intermediate.device_instance_ref_t", "DeviceInstanceRef"),
    "DeviceInstance": ("xknxeditor.namespaces.intermediate.device_instance_t", "DeviceInstance"),
    "DeviceInstanceAdditionalAddresses": ("xknxeditor.namespaces.intermediate.device_instance_t_additional_addresses", "DeviceInstanceAdditionalAddresses"),
    "DeviceInstanceAdditionalAddressesAddress": ("xknxeditor.namespaces.intermediate.device_instance_t_additional_addresses_address", "DeviceInstanceAdditionalAddressesAddress"),
    "DeviceInstanceBinaryData": ("xknxeditor.namespaces.intermediate.device_instance_t_binary_data", "DeviceInstanceBinaryData"),
    "DeviceInstanceBinaryDataBinaryData": ("xknxeditor.namespaces.intermediate.device_instance_t_binary_data_binary_data", "DeviceInstanceBinaryDataBinaryData"),
    "DeviceInstanceBusInterfaces": ("xknxeditor.namespaces.intermediate.device_instance_t_bus_interfaces", "DeviceInstanceBusInterfaces"),
    "DeviceInstanceChannelInstances": ("xknxeditor.namespaces.intermediate.device_instance_t_channel_instances", "DeviceInstanceChannelInstances"),
    "DeviceInstanceComObjectInstanceRefs": ("xknxeditor.namespaces.intermediate.device_instance_t_com_object_instance_refs", "DeviceInstanceComObjectInstanceRefs"),
    "DeviceInstanceGroupObjectTree": ("xknxeditor.namespaces.intermediate.device_instance_t_group_object_tree", "DeviceInstanceGroupObjectTree"),
    "DeviceInstanceGroupObjectTreeNodes": ("xknxeditor.namespaces.intermediate.device_instance_t_group_object_tree_nodes", "DeviceInstanceGroupObjectTreeNodes"),
    "DeviceInstanceModuleInstances": ("xknxeditor.namespaces.intermediate.device_instance_t_module_instances", "DeviceInstanceModuleInstances"),
    "DeviceInstanceParameterInstanceRefs": ("xknxeditor.namespaces.intermediate.device_instance_t_parameter_instance_refs", "DeviceInstanceParameterInstanceRefs"),
    "DeviceInstanceRfFastAckSlots": ("xknxeditor.namespaces.intermediate.device_instance_t_rf_fast_ack_slots", "DeviceInstanceRfFastAckSlots"),
    "DeviceInstanceRfFastAckSlotsSlot": ("xknxeditor.namespaces.intermediate.device_instance_t_rf_fast_ack_slots_slot", "DeviceInstanceRfFastAckSlotsSlot"),
    "DownloadBehavior": ("xknxeditor.namespaces.intermediate.download_behavior_t", "DownloadBehavior"),
    "Enable": ("xknxeditor.namespaces.intermediate.enable_t", "Enable"),
    "Fixup": ("xknxeditor.namespaces.intermediate.fixup_t", "Fixup"),
    "Function": ("xknxeditor.namespaces.intermediate.function_t", "Function"),
    "FunctionType": ("xknxeditor.namespaces.intermediate.function_type_t", "FunctionType"),
    "FunctionTypeFunctionPoint": ("xknxeditor.namespaces.intermediate.function_type_t_function_point", "FunctionTypeFunctionPoint"),
    "FunctionsGroup": ("xknxeditor.namespaces.intermediate.functions_group_t", "FunctionsGroup"),
    "GroupAddressRef": ("xknxeditor.namespaces.intermediate.group_address_ref_t", "GroupAddressRef"),
    "GroupAddressStyle": ("xknxeditor.namespaces.intermediate.group_address_style_t", "GroupAddressStyle"),
    "GroupAddress": ("xknxeditor.namespaces.intermediate.group_address_t", "GroupAddress"),
    "GroupAddresses": ("xknxeditor.namespaces.intermediate.group_addresses_t", "GroupAddresses"),
    "GroupAddressesGroupRanges": ("xknxeditor.namespaces.intermediate.group_addresses_t_group_ranges", "GroupAddressesGroupRanges"),
    "GroupRange": ("xknxeditor.namespaces.intermediate.group_range_t", "GroupRange"),
    "Hardware2Program": ("xknxeditor.namespaces.intermediate.hardware2_program_t", "Hardware2Program"),
    "Hardware": ("xknxeditor.namespaces.intermediate.hardware_t", "Hardware"),
    "HardwareHardware2Programs": ("xknxeditor.namespaces.intermediate.hardware_t_hardware2_programs", "HardwareHardware2Programs"),
    "HardwareProducts": ("xknxeditor.namespaces.intermediate.hardware_t_products", "HardwareProducts"),
    "HardwareProductsProduct": ("xknxeditor.namespaces.intermediate.hardware_t_products_product", "HardwareProductsProduct"),
    "HardwareProductsProductAttributes": ("xknxeditor.namespaces.intermediate.hardware_t_products_product_attributes", "HardwareProductsProductAttributes"),
    "HardwareProductsProductAttributesAttribute": ("xknxeditor.namespaces.intermediate.hardware_t_products_product_attributes_attribute", "HardwareProductsProductAttributesAttribute"),
    "HardwareProductsProductAttributesAttributeName": ("xknxeditor.namespaces.intermediate.hardware_t_products_product_attributes_attribute_name", "HardwareProductsProductAttributesAttributeName"),
    "HardwareProductsProductBaggages": ("xknxeditor.namespaces.intermediate.hardware_t_products_product_baggages", "HardwareProductsProductBaggages"),
    "HardwareProductsProductBaggagesBaggage": ("xknxeditor.namespaces.intermediate.hardware_t_products_product_baggages_baggage", "HardwareProductsProductBaggagesBaggage"),
    "HawkConfigurationData": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t", "HawkConfigurationData"),
    "HawkConfigurationDataFeatures": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_features", "HawkConfigurationDataFeatures"),
    "HawkConfigurationDataFeaturesFeature": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_features_feature", "HawkConfigurationDataFeaturesFeature"),
    "HawkConfigurationDataFeaturesFeatureName": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_features_feature_name", "HawkConfigurationDataFeaturesFeatureName"),
    "HawkConfigurationDataInterfaceObjects": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_interface_objects", "HawkConfigurationDataInterfaceObjects"),
    "HawkConfigurationDataInterfaceObjectsInterfaceObject": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_interface_objects_interface_object", "HawkConfigurationDataInterfaceObjectsInterfaceObject"),
    "HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_interface_objects_interface_object_property", "HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty"),
    "HawkConfigurationDataMemorySegments": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_memory_segments", "HawkConfigurationDataMemorySegments"),
    "HawkConfigurationDataMemorySegmentsMemorySegment": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_memory_segments_memory_segment", "HawkConfigurationDataMemorySegmentsMemorySegment"),
    "HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_memory_segments_memory_segment_access_rights", "HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights"),
    "HawkConfigurationDataProcedures": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_procedures", "HawkConfigurationDataProcedures"),
    "HawkConfigurationDataProceduresProcedure": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_procedures_procedure", "HawkConfigurationDataProceduresProcedure"),
    "HawkConfigurationDataProceduresProcedureValue": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_procedures_procedure_value", "HawkConfigurationDataProceduresProcedureValue"),
    "HawkConfigurationDataResources": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_resources", "HawkConfigurationDataResources"),
    "HawkConfigurationDataResourcesResource": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_resources_resource", "HawkConfigurationDataResourcesResource"),
    "HawkConfigurationDataResourcesResourceAccessRights": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_resources_resource_access_rights", "HawkConfigurationDataResourcesResourceAccessRights"),
    "HawkConfigurationDataResourcesResourceResourceType": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_resources_resource_resource_type", "HawkConfigurationDataResourcesResourceResourceType"),
    "HawkConfigurationDataResourcesResourceResourceTypeFlavour": ("xknxeditor.namespaces.intermediate.hawk_configuration_data_t_resources_resource_resource_type_flavour", "HawkConfigurationDataResourcesResourceResourceTypeFlavour"),
    "HorizontalAlignment": ("xknxeditor.namespaces.intermediate.horizontal_alignment_t", "HorizontalAlignment"),
    "IoPointParameter": ("xknxeditor.namespaces.intermediate.io_tpoint_parameter_t", "IoPointParameter"),
    "IpconfigAssign": ("xknxeditor.namespaces.intermediate.ipconfig_assign_t", "IpconfigAssign"),
    "Ipconfig": ("xknxeditor.namespaces.intermediate.ipconfig_t", "Ipconfig"),
    "Knx": ("xknxeditor.namespaces.intermediate.knx", "Knx"),
    "LanguageData": ("xknxeditor.namespaces.intermediate.language_data_t", "LanguageData"),
    "LanguageDataTranslationUnit": ("xknxeditor.namespaces.intermediate.language_data_t_translation_unit", "LanguageDataTranslationUnit"),
    "LanguageDataTranslationUnitTranslationElement": ("xknxeditor.namespaces.intermediate.language_data_t_translation_unit_translation_element", "LanguageDataTranslationUnitTranslationElement"),
    "LanguageDataTranslationUnitTranslationElementTranslation": ("xknxeditor.namespaces.intermediate.language_data_t_translation_unit_translation_element_translation", "LanguageDataTranslationUnitTranslationElementTranslation"),
    "LdCtrlAbsSegment": ("xknxeditor.namespaces.intermediate.ld_ctrl_abs_segment_t", "LdCtrlAbsSegment"),
    "LdCtrlBaseChoose": ("xknxeditor.namespaces.intermediate.ld_ctrl_base_choose_t", "LdCtrlBaseChoose"),
    "LdCtrlBaseChooseWhen": ("xknxeditor.namespaces.intermediate.ld_ctrl_base_choose_t", "LdCtrlBaseChooseWhen"),
    "LdCtrlBase": ("xknxeditor.namespaces.intermediate.ld_ctrl_base_t", "LdCtrlBase"),
    "LdCtrlBaseOnError": ("xknxeditor.namespaces.intermediate.ld_ctrl_base_t_on_error", "LdCtrlBaseOnError"),
    "LdCtrlClearCachedObjectTypes": ("xknxeditor.namespaces.intermediate.ld_ctrl_clear_cached_object_types_t", "LdCtrlClearCachedObjectTypes"),
    "LdCtrlClearLcfilterTable": ("xknxeditor.namespaces.intermediate.ld_ctrl_clear_lcfilter_table_t", "LdCtrlClearLcfilterTable"),
    "LdCtrlCompareBase": ("xknxeditor.namespaces.intermediate.ld_ctrl_compare_base_t", "LdCtrlCompareBase"),
    "LdCtrlCompareMem": ("xknxeditor.namespaces.intermediate.ld_ctrl_compare_mem_t", "LdCtrlCompareMem"),
    "LdCtrlCompareProp": ("xknxeditor.namespaces.intermediate.ld_ctrl_compare_prop_t", "LdCtrlCompareProp"),
    "LdCtrlCompareRelMem": ("xknxeditor.namespaces.intermediate.ld_ctrl_compare_rel_mem_t", "LdCtrlCompareRelMem"),
    "LdCtrlConnect": ("xknxeditor.namespaces.intermediate.ld_ctrl_connect_t", "LdCtrlConnect"),
    "LdCtrlControlVariable": ("xknxeditor.namespaces.intermediate.ld_ctrl_control_variable_t", "LdCtrlControlVariable"),
    "LdCtrlDeclarePropDesc": ("xknxeditor.namespaces.intermediate.ld_ctrl_declare_prop_desc_t", "LdCtrlDeclarePropDesc"),
    "LdCtrlDelay": ("xknxeditor.namespaces.intermediate.ld_ctrl_delay_t", "LdCtrlDelay"),
    "LdCtrlDisconnect": ("xknxeditor.namespaces.intermediate.ld_ctrl_disconnect_t", "LdCtrlDisconnect"),
    "LdCtrlErrorCause": ("xknxeditor.namespaces.intermediate.ld_ctrl_error_cause_t", "LdCtrlErrorCause"),
    "LdCtrlInvokeFunctionProp": ("xknxeditor.namespaces.intermediate.ld_ctrl_invoke_function_prop_t", "LdCtrlInvokeFunctionProp"),
    "LdCtrlLoadCompleted": ("xknxeditor.namespaces.intermediate.ld_ctrl_load_completed_t", "LdCtrlLoadCompleted"),
    "LdCtrlLoadImageMem": ("xknxeditor.namespaces.intermediate.ld_ctrl_load_image_mem_t", "LdCtrlLoadImageMem"),
    "LdCtrlLoadImageProp": ("xknxeditor.namespaces.intermediate.ld_ctrl_load_image_prop_t", "LdCtrlLoadImageProp"),
    "LdCtrlLoadImageRelMem": ("xknxeditor.namespaces.intermediate.ld_ctrl_load_image_rel_mem_t", "LdCtrlLoadImageRelMem"),
    "LdCtrlLoad": ("xknxeditor.namespaces.intermediate.ld_ctrl_load_t", "LdCtrlLoad"),
    "LdCtrlMapError": ("xknxeditor.namespaces.intermediate.ld_ctrl_map_error_t", "LdCtrlMapError"),
    "LdCtrlMasterReset": ("xknxeditor.namespaces.intermediate.ld_ctrl_master_reset_t", "LdCtrlMasterReset"),
    "LdCtrlMaxLength": ("xknxeditor.namespaces.intermediate.ld_ctrl_max_length_t", "LdCtrlMaxLength"),
    "LdCtrlMemAddrSpace": ("xknxeditor.namespaces.intermediate.ld_ctrl_mem_addr_space_t", "LdCtrlMemAddrSpace"),
    "LdCtrlMerge": ("xknxeditor.namespaces.intermediate.ld_ctrl_merge_t", "LdCtrlMerge"),
    "LdCtrlProcType": ("xknxeditor.namespaces.intermediate.ld_ctrl_proc_type_t", "LdCtrlProcType"),
    "LdCtrlProgressText": ("xknxeditor.namespaces.intermediate.ld_ctrl_progress_text_t", "LdCtrlProgressText"),
    "LdCtrlReadFunctionProp": ("xknxeditor.namespaces.intermediate.ld_ctrl_read_function_prop_t", "LdCtrlReadFunctionProp"),
    "LdCtrlRelSegment": ("xknxeditor.namespaces.intermediate.ld_ctrl_rel_segment_t", "LdCtrlRelSegment"),
    "LdCtrlRestart": ("xknxeditor.namespaces.intermediate.ld_ctrl_restart_t", "LdCtrlRestart"),
    "LdCtrlSetControlVariable": ("xknxeditor.namespaces.intermediate.ld_ctrl_set_control_variable_t", "LdCtrlSetControlVariable"),
    "LdCtrlTaskCtrl1": ("xknxeditor.namespaces.intermediate.ld_ctrl_task_ctrl1_t", "LdCtrlTaskCtrl1"),
    "LdCtrlTaskCtrl2": ("xknxeditor.namespaces.intermediate.ld_ctrl_task_ctrl2_t", "LdCtrlTaskCtrl2"),
    "LdCtrlTaskPtr": ("xknxeditor.namespaces.intermediate.ld_ctrl_task_ptr_t", "LdCtrlTaskPtr"),
    "LdCtrlTaskSegment": ("xknxeditor.namespaces.intermediate.ld_ctrl_task_segment_t", "LdCtrlTaskSegment"),
    "LdCtrlUnload": ("xknxeditor.namespaces.intermediate.ld_ctrl_unload_t", "LdCtrlUnload"),
    "LdCtrlWriteMem": ("xknxeditor.namespaces.intermediate.ld_ctrl_write_mem_t", "LdCtrlWriteMem"),
    "LdCtrlWriteProp": ("xknxeditor.namespaces.intermediate.ld_ctrl_write_prop_t", "LdCtrlWriteProp"),
    "LdCtrlWriteRelMem": ("xknxeditor.namespaces.intermediate.ld_ctrl_write_rel_mem_t", "LdCtrlWriteRelMem"),
    "LoadProcedureStyle": ("xknxeditor.namespaces.intermediate.load_procedure_style_t", "LoadProcedureStyle"),
    "LoadProcedure": ("xknxeditor.namespaces.intermediate.load_procedure_t", "LoadProcedure"),
    "LoadProcedures": ("xknxeditor.namespaces.intermediate.load_procedures_t", "LoadProcedures"),
    "LoadProceduresLoadProcedure": ("xknxeditor.namespaces.intermediate.load_procedures_t_load_procedure", "LoadProceduresLoadProcedure"),
    "Locations": ("xknxeditor.namespaces.intermediate.locations_t", "Locations"),
    "ManufacturerData": ("xknxeditor.namespaces.intermediate.manufacturer_data_t", "ManufacturerData"),
    "ManufacturerDataManufacturer": ("xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer", "ManufacturerDataManufacturer"),
    "ManufacturerDataManufacturerApplicationPrograms": ("xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_application_programs", "ManufacturerDataManufacturerApplicationPrograms"),
    "ManufacturerDataManufacturerBaggages": ("xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_baggages", "ManufacturerDataManufacturerBaggages"),
    "ManufacturerDataManufacturerBaggagesBaggage": ("xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_baggages_baggage", "ManufacturerDataManufacturerBaggagesBaggage"),
    "ManufacturerDataManufacturerBaggagesBaggageFileInfo": ("xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_baggages_baggage_file_info", "ManufacturerDataManufacturerBaggagesBaggageFileInfo"),
    "ManufacturerDataManufacturerCatalog": ("xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_catalog", "ManufacturerDataManufacturerCatalog"),
    "ManufacturerDataManufacturerHardware": ("xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_hardware", "ManufacturerDataManufacturerHardware"),
    "ManufacturerDataManufacturerLanguages": ("xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_languages", "ManufacturerDataManufacturerLanguages"),
    "MaskVersion": ("xknxeditor.namespaces.intermediate.mask_version_t", "MaskVersion"),
    "MaskVersionDownwardCompatibleMasks": ("xknxeditor.namespaces.intermediate.mask_version_t_downward_compatible_masks", "MaskVersionDownwardCompatibleMasks"),
    "MaskVersionDownwardCompatibleMasksDownwardCompatibleMask": ("xknxeditor.namespaces.intermediate.mask_version_t_downward_compatible_masks_downward_compatible_mask", "MaskVersionDownwardCompatibleMasksDownwardCompatibleMask"),
    "MaskVersionManagementModel": ("xknxeditor.namespaces.intermediate.mask_version_t_management_model", "MaskVersionManagementModel"),
    "MaskVersionMaskEntries": ("xknxeditor.namespaces.intermediate.mask_version_t_mask_entries", "MaskVersionMaskEntries"),
    "MaskVersionMaskEntriesMaskEntry": ("xknxeditor.namespaces.intermediate.mask_version_t_mask_entries_mask_entry", "MaskVersionMaskEntriesMaskEntry"),
    "MasterData": ("xknxeditor.namespaces.intermediate.master_data_t", "MasterData"),
    "MasterDataDatapointRoles": ("xknxeditor.namespaces.intermediate.master_data_t_datapoint_roles", "MasterDataDatapointRoles"),
    "MasterDataDatapointTypes": ("xknxeditor.namespaces.intermediate.master_data_t_datapoint_types", "MasterDataDatapointTypes"),
    "MasterDataFunctionTypes": ("xknxeditor.namespaces.intermediate.master_data_t_function_types", "MasterDataFunctionTypes"),
    "MasterDataFunctionalBlocks": ("xknxeditor.namespaces.intermediate.master_data_t_functional_blocks", "MasterDataFunctionalBlocks"),
    "MasterDataFunctionalBlocksFunctionalBlock": ("xknxeditor.namespaces.intermediate.master_data_t_functional_blocks_functional_block", "MasterDataFunctionalBlocksFunctionalBlock"),
    "MasterDataFunctionalBlocksFunctionalBlockParameters": ("xknxeditor.namespaces.intermediate.master_data_t_functional_blocks_functional_block_parameters", "MasterDataFunctionalBlocksFunctionalBlockParameters"),
    "MasterDataFunctionalBlocksFunctionalBlockParametersParameter": ("xknxeditor.namespaces.intermediate.master_data_t_functional_blocks_functional_block_parameters_parameter", "MasterDataFunctionalBlocksFunctionalBlockParametersParameter"),
    "MasterDataInterfaceObjectProperties": ("xknxeditor.namespaces.intermediate.master_data_t_interface_object_properties", "MasterDataInterfaceObjectProperties"),
    "MasterDataInterfaceObjectPropertiesInterfaceObjectProperty": ("xknxeditor.namespaces.intermediate.master_data_t_interface_object_properties_interface_object_property", "MasterDataInterfaceObjectPropertiesInterfaceObjectProperty"),
    "MasterDataInterfaceObjectTypes": ("xknxeditor.namespaces.intermediate.master_data_t_interface_object_types", "MasterDataInterfaceObjectTypes"),
    "MasterDataInterfaceObjectTypesInterfaceObjectType": ("xknxeditor.namespaces.intermediate.master_data_t_interface_object_types_interface_object_type", "MasterDataInterfaceObjectTypesInterfaceObjectType"),
    "MasterDataLanguages": ("xknxeditor.namespaces.intermediate.master_data_t_languages", "MasterDataLanguages"),
    "MasterDataManufacturers": ("xknxeditor.namespaces.intermediate.master_data_t_manufacturers", "MasterDataManufacturers"),
    "MasterDataManufacturersManufacturer": ("xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer", "MasterDataManufacturersManufacturer"),
    "MasterDataManufacturersManufacturerDatapointRoles": ("xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_datapoint_roles", "MasterDataManufacturersManufacturerDatapointRoles"),
    "MasterDataManufacturersManufacturerDatapointTypes": ("xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_datapoint_types", "MasterDataManufacturersManufacturerDatapointTypes"),
    "MasterDataManufacturersManufacturerFunctionTypes": ("xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_function_types", "MasterDataManufacturersManufacturerFunctionTypes"),
    "MasterDataManufacturersManufacturerImportRestriction": ("xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_import_restriction", "MasterDataManufacturersManufacturerImportRestriction"),
    "MasterDataManufacturersManufacturerPublicKeys": ("xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_public_keys", "MasterDataManufacturersManufacturerPublicKeys"),
    "MasterDataManufacturersManufacturerPublicKeysPublicKey": ("xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_public_keys_public_key", "MasterDataManufacturersManufacturerPublicKeysPublicKey"),
    "MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue": ("xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_public_keys_public_key_rsakey_value", "MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue"),
    "MasterDataManufacturersManufacturerSpaceUsages": ("xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_space_usages", "MasterDataManufacturersManufacturerSpaceUsages"),
    "MasterDataMaskVersions": ("xknxeditor.namespaces.intermediate.master_data_t_mask_versions", "MasterDataMaskVersions"),
    "MasterDataMediumTypes": ("xknxeditor.namespaces.intermediate.master_data_t_medium_types", "MasterDataMediumTypes"),
    "MasterDataMediumTypesMediumType": ("xknxeditor.namespaces.intermediate.master_data_t_medium_types_medium_type", "MasterDataMediumTypesMediumType"),
    "MasterDataProductLanguages": ("xknxeditor.namespaces.intermediate.master_data_t_product_languages", "MasterDataProductLanguages"),
    "MasterDataProductLanguagesLanguage": ("xknxeditor.namespaces.intermediate.master_data_t_product_languages_language", "MasterDataProductLanguagesLanguage"),
    "MasterDataPropertyDataTypes": ("xknxeditor.namespaces.intermediate.master_data_t_property_data_types", "MasterDataPropertyDataTypes"),
    "MasterDataPropertyDataTypesPropertyDataType": ("xknxeditor.namespaces.intermediate.master_data_t_property_data_types_property_data_type", "MasterDataPropertyDataTypesPropertyDataType"),
    "MasterDataSpaceUsages": ("xknxeditor.namespaces.intermediate.master_data_t_space_usages", "MasterDataSpaceUsages"),
    "MemberStatus": ("xknxeditor.namespaces.intermediate.member_status_t", "MemberStatus"),
    "MemoryParameter": ("xknxeditor.namespaces.intermediate.memory_parameter_t", "MemoryParameter"),
    "MemoryType": ("xknxeditor.namespaces.intermediate.memory_type_t", "MemoryType"),
    "MemoryUnion": ("xknxeditor.namespaces.intermediate.memory_union_t", "MemoryUnion"),
    "ModuleArg": ("xknxeditor.namespaces.intermediate.module_arg_t", "ModuleArg"),
    "ModuleDefArgType": ("xknxeditor.namespaces.intermediate.module_def_arg_type_t", "ModuleDefArgType"),
    "ModuleDefDynamic": ("xknxeditor.namespaces.intermediate.module_def_dynamic_t", "ModuleDefDynamic"),
    "ModuleDefLdCtrlBaseChoose": ("xknxeditor.namespaces.intermediate.module_def_ld_ctrl_base_choose_t", "ModuleDefLdCtrlBaseChoose"),
    "ModuleDefLdCtrlBaseChooseWhen": ("xknxeditor.namespaces.intermediate.module_def_ld_ctrl_base_choose_t_when", "ModuleDefLdCtrlBaseChooseWhen"),
    "ModuleDefLdCtrlCompareProp": ("xknxeditor.namespaces.intermediate.module_def_ld_ctrl_compare_prop_t", "ModuleDefLdCtrlCompareProp"),
    "ModuleDefLdCtrlInvokeFunctionProp": ("xknxeditor.namespaces.intermediate.module_def_ld_ctrl_invoke_function_prop_t", "ModuleDefLdCtrlInvokeFunctionProp"),
    "ModuleDefLdCtrlReadFunctionProp": ("xknxeditor.namespaces.intermediate.module_def_ld_ctrl_read_function_prop_t", "ModuleDefLdCtrlReadFunctionProp"),
    "ModuleDefLdCtrlWriteProp": ("xknxeditor.namespaces.intermediate.module_def_ld_ctrl_write_prop_t", "ModuleDefLdCtrlWriteProp"),
    "ModuleDefLoadProcedure": ("xknxeditor.namespaces.intermediate.module_def_load_procedure_t", "ModuleDefLoadProcedure"),
    "ModuleDefLoadProcedures": ("xknxeditor.namespaces.intermediate.module_def_load_procedures_t", "ModuleDefLoadProcedures"),
    "ModuleDefStatic": ("xknxeditor.namespaces.intermediate.module_def_static_t", "ModuleDefStatic"),
    "ModuleDefStaticAllocators": ("xknxeditor.namespaces.intermediate.module_def_static_t_allocators", "ModuleDefStaticAllocators"),
    "ModuleDefStaticComObjectRefs": ("xknxeditor.namespaces.intermediate.module_def_static_t_com_object_refs", "ModuleDefStaticComObjectRefs"),
    "ModuleDefStaticComObjects": ("xknxeditor.namespaces.intermediate.module_def_static_t_com_objects", "ModuleDefStaticComObjects"),
    "ModuleDefStaticComObjectsComObject": ("xknxeditor.namespaces.intermediate.module_def_static_t_com_objects_com_object", "ModuleDefStaticComObjectsComObject"),
    "ModuleDefStaticParameterCalculations": ("xknxeditor.namespaces.intermediate.module_def_static_t_parameter_calculations", "ModuleDefStaticParameterCalculations"),
    "ModuleDefStaticParameterRefs": ("xknxeditor.namespaces.intermediate.module_def_static_t_parameter_refs", "ModuleDefStaticParameterRefs"),
    "ModuleDefStaticParameterValidations": ("xknxeditor.namespaces.intermediate.module_def_static_t_parameter_validations", "ModuleDefStaticParameterValidations"),
    "ModuleDefStaticParameters": ("xknxeditor.namespaces.intermediate.module_def_static_t_parameters", "ModuleDefStaticParameters"),
    "ModuleDefStaticParametersParameter": ("xknxeditor.namespaces.intermediate.module_def_static_t_parameters_parameter", "ModuleDefStaticParametersParameter"),
    "ModuleDefStaticParametersParameterMemory": ("xknxeditor.namespaces.intermediate.module_def_static_t_parameters_parameter_memory", "ModuleDefStaticParametersParameterMemory"),
    "ModuleDefStaticParametersParameterProperty": ("xknxeditor.namespaces.intermediate.module_def_static_t_parameters_parameter_property", "ModuleDefStaticParametersParameterProperty"),
    "ModuleDefStaticParametersUnion": ("xknxeditor.namespaces.intermediate.module_def_static_t_parameters_union", "ModuleDefStaticParametersUnion"),
    "ModuleDefStaticParametersUnionMemory": ("xknxeditor.namespaces.intermediate.module_def_static_t_parameters_union_memory", "ModuleDefStaticParametersUnionMemory"),
    "ModuleDefStaticParametersUnionProperty": ("xknxeditor.namespaces.intermediate.module_def_static_t_parameters_union_property", "ModuleDefStaticParametersUnionProperty"),
    "ModuleDef": ("xknxeditor.namespaces.intermediate.module_def_t", "ModuleDef"),
    "ModuleDefSubModuleDefs": ("xknxeditor.namespaces.intermediate.module_def_t", "ModuleDefSubModuleDefs"),
    "ModuleDefArguments": ("xknxeditor.namespaces.intermediate.module_def_t_arguments", "ModuleDefArguments"),
    "ModuleDefArgumentsArgument": ("xknxeditor.namespaces.intermediate.module_def_t_arguments_argument", "ModuleDefArgumentsArgument"),
    "ModuleDefArgumentsArgumentAlignment": ("xknxeditor.namespaces.intermediate.module_def_t_arguments_argument_alignment", "ModuleDefArgumentsArgumentAlignment"),
    "ModuleInstance": ("xknxeditor.namespaces.intermediate.module_instance_t", "ModuleInstance"),
    "ModuleInstanceArguments": ("xknxeditor.namespaces.intermediate.module_instance_t_arguments", "ModuleInstanceArguments"),
    "ModuleInstanceArgumentsArgument": ("xknxeditor.namespaces.intermediate.module_instance_t_arguments_argument", "ModuleInstanceArgumentsArgument"),
    "Module": ("xknxeditor.namespaces.intermediate.module_t", "Module"),
    "ModuleNumericArg": ("xknxeditor.namespaces.intermediate.module_t_numeric_arg", "ModuleNumericArg"),
    "ModuleTextArg": ("xknxeditor.namespaces.intermediate.module_t_text_arg", "ModuleTextArg"),
    "Node": ("xknxeditor.namespaces.intermediate.node_t", "Node"),
    "NodeNodes": ("xknxeditor.namespaces.intermediate.node_t", "NodeNodes"),
    "NodeType": ("xknxeditor.namespaces.intermediate.node_t_type", "NodeType"),
    "P2PlinkBusInterfaceEndpoint": ("xknxeditor.namespaces.intermediate.p2_plink_bus_interface_endpoint_t", "P2PlinkBusInterfaceEndpoint"),
    "P2PlinkDeviceEndpoint": ("xknxeditor.namespaces.intermediate.p2_plink_device_endpoint_t", "P2PlinkDeviceEndpoint"),
    "P2PlinkEndpoint": ("xknxeditor.namespaces.intermediate.p2_plink_endpoint_t", "P2PlinkEndpoint"),
    "P2Plinks": ("xknxeditor.namespaces.intermediate.p2_plinks_t", "P2Plinks"),
    "P2PlinksP2Plink": ("xknxeditor.namespaces.intermediate.p2_plinks_t_p2_plink", "P2PlinksP2Plink"),
    "ParameterBase": ("xknxeditor.namespaces.intermediate.parameter_base_t", "ParameterBase"),
    "ParameterBlockLayout": ("xknxeditor.namespaces.intermediate.parameter_block_layout_t", "ParameterBlockLayout"),
    "ParameterCalculation": ("xknxeditor.namespaces.intermediate.parameter_calculation_t", "ParameterCalculation"),
    "ParameterCalculationLanguage": ("xknxeditor.namespaces.intermediate.parameter_calculation_t_language", "ParameterCalculationLanguage"),
    "ParameterCalculationLparameters": ("xknxeditor.namespaces.intermediate.parameter_calculation_t_lparameters", "ParameterCalculationLparameters"),
    "ParameterCalculationRparameters": ("xknxeditor.namespaces.intermediate.parameter_calculation_t_rparameters", "ParameterCalculationRparameters"),
    "ParameterInstanceRef": ("xknxeditor.namespaces.intermediate.parameter_instance_ref_t", "ParameterInstanceRef"),
    "ParameterRefRef": ("xknxeditor.namespaces.intermediate.parameter_ref_ref_t", "ParameterRefRef"),
    "ParameterRef": ("xknxeditor.namespaces.intermediate.parameter_ref_t", "ParameterRef"),
    "ParameterSeparator": ("xknxeditor.namespaces.intermediate.parameter_separator_t", "ParameterSeparator"),
    "ParameterSeparatorUihint": ("xknxeditor.namespaces.intermediate.parameter_separator_t_uihint", "ParameterSeparatorUihint"),
    "ParameterType": ("xknxeditor.namespaces.intermediate.parameter_type_t", "ParameterType"),
    "ParameterTypeTypeColor": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_color", "ParameterTypeTypeColor"),
    "ParameterTypeTypeColorSpace": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_color_space", "ParameterTypeTypeColorSpace"),
    "ParameterTypeTypeDate": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_date", "ParameterTypeTypeDate"),
    "ParameterTypeTypeDateEncoding": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_date_encoding", "ParameterTypeTypeDateEncoding"),
    "ParameterTypeTypeFloat": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_float", "ParameterTypeTypeFloat"),
    "ParameterTypeTypeFloatEncoding": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_float_encoding", "ParameterTypeTypeFloatEncoding"),
    "ParameterTypeTypeFloatUihint": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_float_uihint", "ParameterTypeTypeFloatUihint"),
    "ParameterTypeTypeIpaddress": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_ipaddress", "ParameterTypeTypeIpaddress"),
    "ParameterTypeTypeIpaddressAddressType": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_ipaddress_address_type", "ParameterTypeTypeIpaddressAddressType"),
    "ParameterTypeTypeIpaddressVersion": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_ipaddress_version", "ParameterTypeTypeIpaddressVersion"),
    "ParameterTypeTypeNumber": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_number", "ParameterTypeTypeNumber"),
    "ParameterTypeTypeNumberType": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_number_type", "ParameterTypeTypeNumberType"),
    "ParameterTypeTypeNumberUihint": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_number_uihint", "ParameterTypeTypeNumberUihint"),
    "ParameterTypeTypePicture": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_picture", "ParameterTypeTypePicture"),
    "ParameterTypeTypeRawData": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_raw_data", "ParameterTypeTypeRawData"),
    "ParameterTypeTypeRestriction": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_restriction", "ParameterTypeTypeRestriction"),
    "ParameterTypeTypeRestrictionBase": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_restriction_base", "ParameterTypeTypeRestrictionBase"),
    "ParameterTypeTypeRestrictionEnumeration": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_restriction_enumeration", "ParameterTypeTypeRestrictionEnumeration"),
    "ParameterTypeTypeRestrictionUihint": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_restriction_uihint", "ParameterTypeTypeRestrictionUihint"),
    "ParameterTypeTypeText": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_text", "ParameterTypeTypeText"),
    "ParameterTypeTypeTime": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_time", "ParameterTypeTypeTime"),
    "ParameterTypeTypeTimeUihint": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_time_uihint", "ParameterTypeTypeTimeUihint"),
    "ParameterTypeTypeTimeUnit": ("xknxeditor.namespaces.intermediate.parameter_type_t_type_time_unit", "ParameterTypeTypeTimeUnit"),
    "ParameterValidation": ("xknxeditor.namespaces.intermediate.parameter_validation_t", "ParameterValidation"),
    "ParameterValidationParameters": ("xknxeditor.namespaces.intermediate.parameter_validation_t_parameters", "ParameterValidationParameters"),
    "ProcedureType": ("xknxeditor.namespaces.intermediate.procedure_type_t", "ProcedureType"),
    "Project": ("xknxeditor.namespaces.intermediate.project_t", "Project"),
    "ProjectAddinData": ("xknxeditor.namespaces.intermediate.project_t_addin_data", "ProjectAddinData"),
    "ProjectInstallations": ("xknxeditor.namespaces.intermediate.project_t_installations", "ProjectInstallations"),
    "ProjectInstallationsInstallation": ("xknxeditor.namespaces.intermediate.project_t_installations_installation", "ProjectInstallationsInstallation"),
    "ProjectInstallationsInstallationSplitType": ("xknxeditor.namespaces.intermediate.project_t_installations_installation_split_type", "ProjectInstallationsInstallationSplitType"),
    "ProjectProjectInformation": ("xknxeditor.namespaces.intermediate.project_t_project_information", "ProjectProjectInformation"),
    "ProjectProjectInformationDeviceCertificates": ("xknxeditor.namespaces.intermediate.project_t_project_information_device_certificates", "ProjectProjectInformationDeviceCertificates"),
    "ProjectProjectInformationHistoryEntries": ("xknxeditor.namespaces.intermediate.project_t_project_information_history_entries", "ProjectProjectInformationHistoryEntries"),
    "ProjectProjectInformationHistoryEntriesHistoryEntry": ("xknxeditor.namespaces.intermediate.project_t_project_information_history_entries_history_entry", "ProjectProjectInformationHistoryEntriesHistoryEntry"),
    "ProjectProjectInformationProjectTraces": ("xknxeditor.namespaces.intermediate.project_t_project_information_project_traces", "ProjectProjectInformationProjectTraces"),
    "ProjectProjectInformationTags": ("xknxeditor.namespaces.intermediate.project_t_project_information_tags", "ProjectProjectInformationTags"),
    "ProjectProjectInformationTagsTag": ("xknxeditor.namespaces.intermediate.project_t_project_information_tags_tag", "ProjectProjectInformationTagsTag"),
    "ProjectProjectInformationToDoItems": ("xknxeditor.namespaces.intermediate.project_t_project_information_to_do_items", "ProjectProjectInformationToDoItems"),
    "ProjectUserFiles": ("xknxeditor.namespaces.intermediate.project_t_user_files", "ProjectUserFiles"),
    "ProjectTrace": ("xknxeditor.namespaces.intermediate.project_trace_t", "ProjectTrace"),
    "ProjectTracingLevel": ("xknxeditor.namespaces.intermediate.project_tracing_level_t", "ProjectTracingLevel"),
    "ProjectType": ("xknxeditor.namespaces.intermediate.project_type_t", "ProjectType"),
    "PropType": ("xknxeditor.namespaces.intermediate.prop_type_t", "PropType"),
    "PropertyParameter": ("xknxeditor.namespaces.intermediate.property_parameter_t", "PropertyParameter"),
    "PropertyUnion": ("xknxeditor.namespaces.intermediate.property_union_t", "PropertyUnion"),
    "RegistrationInfo": ("xknxeditor.namespaces.intermediate.registration_info_t", "RegistrationInfo"),
    "RegistrationInfoRegistrationKey": ("xknxeditor.namespaces.intermediate.registration_info_t_registration_key", "RegistrationInfoRegistrationKey"),
    "RegistrationStatus": ("xknxeditor.namespaces.intermediate.registration_status_t", "RegistrationStatus"),
    "Rename": ("xknxeditor.namespaces.intermediate.rename_t", "Rename"),
    "ResourceAccessRights": ("xknxeditor.namespaces.intermediate.resource_access_rights_t", "ResourceAccessRights"),
    "ResourceAccess": ("xknxeditor.namespaces.intermediate.resource_access_t", "ResourceAccess"),
    "ResourceAddrSpace": ("xknxeditor.namespaces.intermediate.resource_addr_space_t", "ResourceAddrSpace"),
    "ResourceLocation": ("xknxeditor.namespaces.intermediate.resource_location_t", "ResourceLocation"),
    "ResourceMgmtStyle": ("xknxeditor.namespaces.intermediate.resource_mgmt_style_t", "ResourceMgmtStyle"),
    "ResourceName": ("xknxeditor.namespaces.intermediate.resource_name_t", "ResourceName"),
    "RfdeviceMode": ("xknxeditor.namespaces.intermediate.rfdevice_mode_t", "RfdeviceMode"),
    "RfrxCapabilities": ("xknxeditor.namespaces.intermediate.rfrx_capabilities_t", "RfrxCapabilities"),
    "RftxCapabilities": ("xknxeditor.namespaces.intermediate.rftx_capabilities_t", "RftxCapabilities"),
    "SecurityMode": ("xknxeditor.namespaces.intermediate.security_mode_t", "SecurityMode"),
    "Security": ("xknxeditor.namespaces.intermediate.security_t", "Security"),
    "SegmentBase": ("xknxeditor.namespaces.intermediate.segment_base_t", "SegmentBase"),
    "Space": ("xknxeditor.namespaces.intermediate.space_t", "Space"),
    "SpaceType": ("xknxeditor.namespaces.intermediate.space_type_t", "SpaceType"),
    "SpaceUsage": ("xknxeditor.namespaces.intermediate.space_usage_t", "SpaceUsage"),
    "SplitInfo": ("xknxeditor.namespaces.intermediate.split_info_t", "SplitInfo"),
    "SplitInfos": ("xknxeditor.namespaces.intermediate.split_infos_t", "SplitInfos"),
    "TextAlignment": ("xknxeditor.namespaces.intermediate.text_alignment_t", "TextAlignment"),
    "TextEncoding": ("xknxeditor.namespaces.intermediate.text_encoding_t", "TextEncoding"),
    "ToDoItem": ("xknxeditor.namespaces.intermediate.to_do_item_t", "ToDoItem"),
    "ToDoStatus": ("xknxeditor.namespaces.intermediate.to_do_status_t", "ToDoStatus"),
    "Topology": ("xknxeditor.namespaces.intermediate.topology_t", "Topology"),
    "TopologyArea": ("xknxeditor.namespaces.intermediate.topology_t_area", "TopologyArea"),
    "TopologyAreaLine": ("xknxeditor.namespaces.intermediate.topology_t_area_line", "TopologyAreaLine"),
    "TopologyAreaLineSegment": ("xknxeditor.namespaces.intermediate.topology_t_area_line_segment", "TopologyAreaLineSegment"),
    "TopologyAreaLineSegmentAdditionalGroupAddresses": ("xknxeditor.namespaces.intermediate.topology_t_area_line_segment_additional_group_addresses", "TopologyAreaLineSegmentAdditionalGroupAddresses"),
    "TopologyAreaLineSegmentAdditionalGroupAddressesGroupAddress": ("xknxeditor.namespaces.intermediate.topology_t_area_line_segment_additional_group_addresses_group_address", "TopologyAreaLineSegmentAdditionalGroupAddressesGroupAddress"),
    "TopologyUnassignedDevices": ("xknxeditor.namespaces.intermediate.topology_t_unassigned_devices", "TopologyUnassignedDevices"),
    "Trade": ("xknxeditor.namespaces.intermediate.trade_t", "Trade"),
    "Trades": ("xknxeditor.namespaces.intermediate.trades_t", "Trades"),
    "UnionParameter": ("xknxeditor.namespaces.intermediate.union_parameter_t", "UnionParameter"),
    "UserFile": ("xknxeditor.namespaces.intermediate.user_file_t", "UserFile"),
    "When": ("xknxeditor.namespaces.intermediate.when_t", "When"),
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
    from xknxeditor.namespaces.intermediate.access_t import Access
    from xknxeditor.namespaces.intermediate.addin_data_t import AddinData
    from xknxeditor.namespaces.intermediate.allocator_t import Allocator
    from xknxeditor.namespaces.intermediate.application_program_channel_t import ApplicationProgramChannel
    from xknxeditor.namespaces.intermediate.application_program_channel_t import ChannelChoose
    from xknxeditor.namespaces.intermediate.application_program_channel_t import ChannelChooseWhen
    from xknxeditor.namespaces.intermediate.application_program_channel_t import ComObjectParameterBlock
    from xknxeditor.namespaces.intermediate.application_program_channel_t import ComObjectParameterChoose
    from xknxeditor.namespaces.intermediate.application_program_channel_t import ComObjectParameterChooseWhen
    from xknxeditor.namespaces.intermediate.application_program_channel_t import Repeat
    from xknxeditor.namespaces.intermediate.application_program_dynamic_t import ApplicationProgramDynamic
    from xknxeditor.namespaces.intermediate.application_program_ipconfig_t import ApplicationProgramIpconfig
    from xknxeditor.namespaces.intermediate.application_program_ref_t import ApplicationProgramRef
    from xknxeditor.namespaces.intermediate.application_program_static_t import ApplicationProgramStatic
    from xknxeditor.namespaces.intermediate.application_program_static_t_address_table import ApplicationProgramStaticAddressTable
    from xknxeditor.namespaces.intermediate.application_program_static_t_allocators import ApplicationProgramStaticAllocators
    from xknxeditor.namespaces.intermediate.application_program_static_t_association_table import ApplicationProgramStaticAssociationTable
    from xknxeditor.namespaces.intermediate.application_program_static_t_binary_data import ApplicationProgramStaticBinaryData
    from xknxeditor.namespaces.intermediate.application_program_static_t_bus_interfaces import ApplicationProgramStaticBusInterfaces
    from xknxeditor.namespaces.intermediate.application_program_static_t_bus_interfaces_bus_interface import ApplicationProgramStaticBusInterfacesBusInterface
    from xknxeditor.namespaces.intermediate.application_program_static_t_bus_interfaces_bus_interface_access_type import ApplicationProgramStaticBusInterfacesBusInterfaceAccessType
    from xknxeditor.namespaces.intermediate.application_program_static_t_code import ApplicationProgramStaticCode
    from xknxeditor.namespaces.intermediate.application_program_static_t_code_absolute_segment import ApplicationProgramStaticCodeAbsoluteSegment
    from xknxeditor.namespaces.intermediate.application_program_static_t_code_relative_segment import ApplicationProgramStaticCodeRelativeSegment
    from xknxeditor.namespaces.intermediate.application_program_static_t_com_object_refs import ApplicationProgramStaticComObjectRefs
    from xknxeditor.namespaces.intermediate.application_program_static_t_com_object_table import ApplicationProgramStaticComObjectTable
    from xknxeditor.namespaces.intermediate.application_program_static_t_device_compare import ApplicationProgramStaticDeviceCompare
    from xknxeditor.namespaces.intermediate.application_program_static_t_device_compare_exclude_memory import ApplicationProgramStaticDeviceCompareExcludeMemory
    from xknxeditor.namespaces.intermediate.application_program_static_t_device_compare_exclude_property import ApplicationProgramStaticDeviceCompareExcludeProperty
    from xknxeditor.namespaces.intermediate.application_program_static_t_extension import ApplicationProgramStaticExtension
    from xknxeditor.namespaces.intermediate.application_program_static_t_extension_baggage import ApplicationProgramStaticExtensionBaggage
    from xknxeditor.namespaces.intermediate.application_program_static_t_fixup_list import ApplicationProgramStaticFixupList
    from xknxeditor.namespaces.intermediate.application_program_static_t_messages import ApplicationProgramStaticMessages
    from xknxeditor.namespaces.intermediate.application_program_static_t_messages_message import ApplicationProgramStaticMessagesMessage
    from xknxeditor.namespaces.intermediate.application_program_static_t_options import ApplicationProgramStaticOptions
    from xknxeditor.namespaces.intermediate.application_program_static_t_options_customer_adjustable_parameters import ApplicationProgramStaticOptionsCustomerAdjustableParameters
    from xknxeditor.namespaces.intermediate.application_program_static_t_options_not_loadable import ApplicationProgramStaticOptionsNotLoadable
    from xknxeditor.namespaces.intermediate.application_program_static_t_options_parameter_byte_order import ApplicationProgramStaticOptionsParameterByteOrder
    from xknxeditor.namespaces.intermediate.application_program_static_t_options_text_parameter_encoding_selector import TextEncodingSelector
    from xknxeditor.namespaces.intermediate.application_program_static_t_parameter_calculations import ApplicationProgramStaticParameterCalculations
    from xknxeditor.namespaces.intermediate.application_program_static_t_parameter_refs import ApplicationProgramStaticParameterRefs
    from xknxeditor.namespaces.intermediate.application_program_static_t_parameter_types import ApplicationProgramStaticParameterTypes
    from xknxeditor.namespaces.intermediate.application_program_static_t_parameter_validations import ApplicationProgramStaticParameterValidations
    from xknxeditor.namespaces.intermediate.application_program_static_t_parameters import ApplicationProgramStaticParameters
    from xknxeditor.namespaces.intermediate.application_program_static_t_parameters_parameter import ApplicationProgramStaticParametersParameter
    from xknxeditor.namespaces.intermediate.application_program_static_t_parameters_union import ApplicationProgramStaticParametersUnion
    from xknxeditor.namespaces.intermediate.application_program_static_t_script import ApplicationProgramStaticScript
    from xknxeditor.namespaces.intermediate.application_program_static_t_security_roles import ApplicationProgramStaticSecurityRoles
    from xknxeditor.namespaces.intermediate.application_program_static_t_security_roles_security_role import ApplicationProgramStaticSecurityRolesSecurityRole
    from xknxeditor.namespaces.intermediate.application_program_t import ApplicationProgram
    from xknxeditor.namespaces.intermediate.application_program_t_cloud_connect import ApplicationProgramCloudConnect
    from xknxeditor.namespaces.intermediate.application_program_t_min_ets_version import ApplicationProgramMinEtsVersion
    from xknxeditor.namespaces.intermediate.application_program_t_module_defs import ApplicationProgramModuleDefs
    from xknxeditor.namespaces.intermediate.application_program_t_profile import ApplicationProgramProfile
    from xknxeditor.namespaces.intermediate.application_program_t_profile_io_t import ApplicationProgramProfileIo
    from xknxeditor.namespaces.intermediate.application_program_type_t import ApplicationProgramType
    from xknxeditor.namespaces.intermediate.assign_t import Assign
    from xknxeditor.namespaces.intermediate.binary_data_ref_t import BinaryDataRef
    from xknxeditor.namespaces.intermediate.binary_data_t import BinaryData
    from xknxeditor.namespaces.intermediate.bus_access_t import BusAccess
    from xknxeditor.namespaces.intermediate.bus_interface_t import BusInterface
    from xknxeditor.namespaces.intermediate.bus_interface_t_connectors import BusInterfaceConnectors
    from xknxeditor.namespaces.intermediate.bus_interface_t_connectors_connector import BusInterfaceConnectorsConnector
    from xknxeditor.namespaces.intermediate.button_t import Button
    from xknxeditor.namespaces.intermediate.button_t_event_handler_online import ButtonEventHandlerOnline
    from xknxeditor.namespaces.intermediate.calculation_parameter_ref_t import CalculationParameterRef
    from xknxeditor.namespaces.intermediate.capability_t import Capability
    from xknxeditor.namespaces.intermediate.catalog_section_t import CatalogSection
    from xknxeditor.namespaces.intermediate.catalog_section_t_catalog_item import CatalogSectionCatalogItem
    from xknxeditor.namespaces.intermediate.channel_independent_block_t import ChannelIndependentBlock
    from xknxeditor.namespaces.intermediate.channel_instance_t import ChannelInstance
    from xknxeditor.namespaces.intermediate.com_object_instance_ref_t import ComObjectInstanceRef
    from xknxeditor.namespaces.intermediate.com_object_parameter_block_t_columns import ComObjectParameterBlockColumns
    from xknxeditor.namespaces.intermediate.com_object_parameter_block_t_columns_column import ComObjectParameterBlockColumnsColumn
    from xknxeditor.namespaces.intermediate.com_object_parameter_block_t_rows import ComObjectParameterBlockRows
    from xknxeditor.namespaces.intermediate.com_object_parameter_block_t_rows_row import ComObjectParameterBlockRowsRow
    from xknxeditor.namespaces.intermediate.com_object_priority_t import ComObjectPriority
    from xknxeditor.namespaces.intermediate.com_object_ref_ref_t import ComObjectRefRef
    from xknxeditor.namespaces.intermediate.com_object_ref_t import ComObjectRef
    from xknxeditor.namespaces.intermediate.com_object_security_requirements_t import ComObjectSecurityRequirements
    from xknxeditor.namespaces.intermediate.com_object_size_t import ComObjectSize
    from xknxeditor.namespaces.intermediate.com_object_t import ComObject
    from xknxeditor.namespaces.intermediate.com_table_expectation_t import ComTableExpectation
    from xknxeditor.namespaces.intermediate.completion_status_t import CompletionStatus
    from xknxeditor.namespaces.intermediate.coupler_capability_t import CouplerCapability
    from xknxeditor.namespaces.intermediate.datapoint_role_t import DatapointRole
    from xknxeditor.namespaces.intermediate.datapoint_type_t import DatapointType
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes import DatapointTypeDatapointSubtypes
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype import DatapointTypeDatapointSubtypesDatapointSubtype
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format import DatapointTypeDatapointSubtypesDatapointSubtypeFormat
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_bit import DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration import DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration_enum_value import DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumerationEnumValue
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_float import DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_ref_type import DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_reserved import DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_signed_integer import DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_string import DatapointTypeDatapointSubtypesDatapointSubtypeFormatString
    from xknxeditor.namespaces.intermediate.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_unsigned_integer import DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger
    from xknxeditor.namespaces.intermediate.dependent_channel_choose_t import DependentChannelChoose
    from xknxeditor.namespaces.intermediate.dependent_channel_choose_t import DependentChannelChooseWhen
    from xknxeditor.namespaces.intermediate.deprecation_status_t import DeprecationStatus
    from xknxeditor.namespaces.intermediate.device_certificate_t import DeviceCertificate
    from xknxeditor.namespaces.intermediate.device_instance_ref_t import DeviceInstanceRef
    from xknxeditor.namespaces.intermediate.device_instance_t import DeviceInstance
    from xknxeditor.namespaces.intermediate.device_instance_t_additional_addresses import DeviceInstanceAdditionalAddresses
    from xknxeditor.namespaces.intermediate.device_instance_t_additional_addresses_address import DeviceInstanceAdditionalAddressesAddress
    from xknxeditor.namespaces.intermediate.device_instance_t_binary_data import DeviceInstanceBinaryData
    from xknxeditor.namespaces.intermediate.device_instance_t_binary_data_binary_data import DeviceInstanceBinaryDataBinaryData
    from xknxeditor.namespaces.intermediate.device_instance_t_bus_interfaces import DeviceInstanceBusInterfaces
    from xknxeditor.namespaces.intermediate.device_instance_t_channel_instances import DeviceInstanceChannelInstances
    from xknxeditor.namespaces.intermediate.device_instance_t_com_object_instance_refs import DeviceInstanceComObjectInstanceRefs
    from xknxeditor.namespaces.intermediate.device_instance_t_group_object_tree import DeviceInstanceGroupObjectTree
    from xknxeditor.namespaces.intermediate.device_instance_t_group_object_tree_nodes import DeviceInstanceGroupObjectTreeNodes
    from xknxeditor.namespaces.intermediate.device_instance_t_module_instances import DeviceInstanceModuleInstances
    from xknxeditor.namespaces.intermediate.device_instance_t_parameter_instance_refs import DeviceInstanceParameterInstanceRefs
    from xknxeditor.namespaces.intermediate.device_instance_t_rf_fast_ack_slots import DeviceInstanceRfFastAckSlots
    from xknxeditor.namespaces.intermediate.device_instance_t_rf_fast_ack_slots_slot import DeviceInstanceRfFastAckSlotsSlot
    from xknxeditor.namespaces.intermediate.download_behavior_t import DownloadBehavior
    from xknxeditor.namespaces.intermediate.enable_t import Enable
    from xknxeditor.namespaces.intermediate.fixup_t import Fixup
    from xknxeditor.namespaces.intermediate.function_t import Function
    from xknxeditor.namespaces.intermediate.function_type_t import FunctionType
    from xknxeditor.namespaces.intermediate.function_type_t_function_point import FunctionTypeFunctionPoint
    from xknxeditor.namespaces.intermediate.functions_group_t import FunctionsGroup
    from xknxeditor.namespaces.intermediate.group_address_ref_t import GroupAddressRef
    from xknxeditor.namespaces.intermediate.group_address_style_t import GroupAddressStyle
    from xknxeditor.namespaces.intermediate.group_address_t import GroupAddress
    from xknxeditor.namespaces.intermediate.group_addresses_t import GroupAddresses
    from xknxeditor.namespaces.intermediate.group_addresses_t_group_ranges import GroupAddressesGroupRanges
    from xknxeditor.namespaces.intermediate.group_range_t import GroupRange
    from xknxeditor.namespaces.intermediate.hardware2_program_t import Hardware2Program
    from xknxeditor.namespaces.intermediate.hardware_t import Hardware
    from xknxeditor.namespaces.intermediate.hardware_t_hardware2_programs import HardwareHardware2Programs
    from xknxeditor.namespaces.intermediate.hardware_t_products import HardwareProducts
    from xknxeditor.namespaces.intermediate.hardware_t_products_product import HardwareProductsProduct
    from xknxeditor.namespaces.intermediate.hardware_t_products_product_attributes import HardwareProductsProductAttributes
    from xknxeditor.namespaces.intermediate.hardware_t_products_product_attributes_attribute import HardwareProductsProductAttributesAttribute
    from xknxeditor.namespaces.intermediate.hardware_t_products_product_attributes_attribute_name import HardwareProductsProductAttributesAttributeName
    from xknxeditor.namespaces.intermediate.hardware_t_products_product_baggages import HardwareProductsProductBaggages
    from xknxeditor.namespaces.intermediate.hardware_t_products_product_baggages_baggage import HardwareProductsProductBaggagesBaggage
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t import HawkConfigurationData
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_features import HawkConfigurationDataFeatures
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_features_feature import HawkConfigurationDataFeaturesFeature
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_features_feature_name import HawkConfigurationDataFeaturesFeatureName
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_interface_objects import HawkConfigurationDataInterfaceObjects
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_interface_objects_interface_object import HawkConfigurationDataInterfaceObjectsInterfaceObject
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_interface_objects_interface_object_property import HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_memory_segments import HawkConfigurationDataMemorySegments
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_memory_segments_memory_segment import HawkConfigurationDataMemorySegmentsMemorySegment
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_memory_segments_memory_segment_access_rights import HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_procedures import HawkConfigurationDataProcedures
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_procedures_procedure import HawkConfigurationDataProceduresProcedure
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_procedures_procedure_value import HawkConfigurationDataProceduresProcedureValue
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_resources import HawkConfigurationDataResources
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_resources_resource import HawkConfigurationDataResourcesResource
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_resources_resource_access_rights import HawkConfigurationDataResourcesResourceAccessRights
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_resources_resource_resource_type import HawkConfigurationDataResourcesResourceResourceType
    from xknxeditor.namespaces.intermediate.hawk_configuration_data_t_resources_resource_resource_type_flavour import HawkConfigurationDataResourcesResourceResourceTypeFlavour
    from xknxeditor.namespaces.intermediate.horizontal_alignment_t import HorizontalAlignment
    from xknxeditor.namespaces.intermediate.io_tpoint_parameter_t import IoPointParameter
    from xknxeditor.namespaces.intermediate.ipconfig_assign_t import IpconfigAssign
    from xknxeditor.namespaces.intermediate.ipconfig_t import Ipconfig
    from xknxeditor.namespaces.intermediate.knx import Knx
    from xknxeditor.namespaces.intermediate.language_data_t import LanguageData
    from xknxeditor.namespaces.intermediate.language_data_t_translation_unit import LanguageDataTranslationUnit
    from xknxeditor.namespaces.intermediate.language_data_t_translation_unit_translation_element import LanguageDataTranslationUnitTranslationElement
    from xknxeditor.namespaces.intermediate.language_data_t_translation_unit_translation_element_translation import LanguageDataTranslationUnitTranslationElementTranslation
    from xknxeditor.namespaces.intermediate.ld_ctrl_abs_segment_t import LdCtrlAbsSegment
    from xknxeditor.namespaces.intermediate.ld_ctrl_base_choose_t import LdCtrlBaseChoose
    from xknxeditor.namespaces.intermediate.ld_ctrl_base_choose_t import LdCtrlBaseChooseWhen
    from xknxeditor.namespaces.intermediate.ld_ctrl_base_t import LdCtrlBase
    from xknxeditor.namespaces.intermediate.ld_ctrl_base_t_on_error import LdCtrlBaseOnError
    from xknxeditor.namespaces.intermediate.ld_ctrl_clear_cached_object_types_t import LdCtrlClearCachedObjectTypes
    from xknxeditor.namespaces.intermediate.ld_ctrl_clear_lcfilter_table_t import LdCtrlClearLcfilterTable
    from xknxeditor.namespaces.intermediate.ld_ctrl_compare_base_t import LdCtrlCompareBase
    from xknxeditor.namespaces.intermediate.ld_ctrl_compare_mem_t import LdCtrlCompareMem
    from xknxeditor.namespaces.intermediate.ld_ctrl_compare_prop_t import LdCtrlCompareProp
    from xknxeditor.namespaces.intermediate.ld_ctrl_compare_rel_mem_t import LdCtrlCompareRelMem
    from xknxeditor.namespaces.intermediate.ld_ctrl_connect_t import LdCtrlConnect
    from xknxeditor.namespaces.intermediate.ld_ctrl_control_variable_t import LdCtrlControlVariable
    from xknxeditor.namespaces.intermediate.ld_ctrl_declare_prop_desc_t import LdCtrlDeclarePropDesc
    from xknxeditor.namespaces.intermediate.ld_ctrl_delay_t import LdCtrlDelay
    from xknxeditor.namespaces.intermediate.ld_ctrl_disconnect_t import LdCtrlDisconnect
    from xknxeditor.namespaces.intermediate.ld_ctrl_error_cause_t import LdCtrlErrorCause
    from xknxeditor.namespaces.intermediate.ld_ctrl_invoke_function_prop_t import LdCtrlInvokeFunctionProp
    from xknxeditor.namespaces.intermediate.ld_ctrl_load_completed_t import LdCtrlLoadCompleted
    from xknxeditor.namespaces.intermediate.ld_ctrl_load_image_mem_t import LdCtrlLoadImageMem
    from xknxeditor.namespaces.intermediate.ld_ctrl_load_image_prop_t import LdCtrlLoadImageProp
    from xknxeditor.namespaces.intermediate.ld_ctrl_load_image_rel_mem_t import LdCtrlLoadImageRelMem
    from xknxeditor.namespaces.intermediate.ld_ctrl_load_t import LdCtrlLoad
    from xknxeditor.namespaces.intermediate.ld_ctrl_map_error_t import LdCtrlMapError
    from xknxeditor.namespaces.intermediate.ld_ctrl_master_reset_t import LdCtrlMasterReset
    from xknxeditor.namespaces.intermediate.ld_ctrl_max_length_t import LdCtrlMaxLength
    from xknxeditor.namespaces.intermediate.ld_ctrl_mem_addr_space_t import LdCtrlMemAddrSpace
    from xknxeditor.namespaces.intermediate.ld_ctrl_merge_t import LdCtrlMerge
    from xknxeditor.namespaces.intermediate.ld_ctrl_proc_type_t import LdCtrlProcType
    from xknxeditor.namespaces.intermediate.ld_ctrl_progress_text_t import LdCtrlProgressText
    from xknxeditor.namespaces.intermediate.ld_ctrl_read_function_prop_t import LdCtrlReadFunctionProp
    from xknxeditor.namespaces.intermediate.ld_ctrl_rel_segment_t import LdCtrlRelSegment
    from xknxeditor.namespaces.intermediate.ld_ctrl_restart_t import LdCtrlRestart
    from xknxeditor.namespaces.intermediate.ld_ctrl_set_control_variable_t import LdCtrlSetControlVariable
    from xknxeditor.namespaces.intermediate.ld_ctrl_task_ctrl1_t import LdCtrlTaskCtrl1
    from xknxeditor.namespaces.intermediate.ld_ctrl_task_ctrl2_t import LdCtrlTaskCtrl2
    from xknxeditor.namespaces.intermediate.ld_ctrl_task_ptr_t import LdCtrlTaskPtr
    from xknxeditor.namespaces.intermediate.ld_ctrl_task_segment_t import LdCtrlTaskSegment
    from xknxeditor.namespaces.intermediate.ld_ctrl_unload_t import LdCtrlUnload
    from xknxeditor.namespaces.intermediate.ld_ctrl_write_mem_t import LdCtrlWriteMem
    from xknxeditor.namespaces.intermediate.ld_ctrl_write_prop_t import LdCtrlWriteProp
    from xknxeditor.namespaces.intermediate.ld_ctrl_write_rel_mem_t import LdCtrlWriteRelMem
    from xknxeditor.namespaces.intermediate.load_procedure_style_t import LoadProcedureStyle
    from xknxeditor.namespaces.intermediate.load_procedure_t import LoadProcedure
    from xknxeditor.namespaces.intermediate.load_procedures_t import LoadProcedures
    from xknxeditor.namespaces.intermediate.load_procedures_t_load_procedure import LoadProceduresLoadProcedure
    from xknxeditor.namespaces.intermediate.locations_t import Locations
    from xknxeditor.namespaces.intermediate.manufacturer_data_t import ManufacturerData
    from xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer import ManufacturerDataManufacturer
    from xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_application_programs import ManufacturerDataManufacturerApplicationPrograms
    from xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_baggages import ManufacturerDataManufacturerBaggages
    from xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_baggages_baggage import ManufacturerDataManufacturerBaggagesBaggage
    from xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_baggages_baggage_file_info import ManufacturerDataManufacturerBaggagesBaggageFileInfo
    from xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_catalog import ManufacturerDataManufacturerCatalog
    from xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_hardware import ManufacturerDataManufacturerHardware
    from xknxeditor.namespaces.intermediate.manufacturer_data_t_manufacturer_languages import ManufacturerDataManufacturerLanguages
    from xknxeditor.namespaces.intermediate.mask_version_t import MaskVersion
    from xknxeditor.namespaces.intermediate.mask_version_t_downward_compatible_masks import MaskVersionDownwardCompatibleMasks
    from xknxeditor.namespaces.intermediate.mask_version_t_downward_compatible_masks_downward_compatible_mask import MaskVersionDownwardCompatibleMasksDownwardCompatibleMask
    from xknxeditor.namespaces.intermediate.mask_version_t_management_model import MaskVersionManagementModel
    from xknxeditor.namespaces.intermediate.mask_version_t_mask_entries import MaskVersionMaskEntries
    from xknxeditor.namespaces.intermediate.mask_version_t_mask_entries_mask_entry import MaskVersionMaskEntriesMaskEntry
    from xknxeditor.namespaces.intermediate.master_data_t import MasterData
    from xknxeditor.namespaces.intermediate.master_data_t_datapoint_roles import MasterDataDatapointRoles
    from xknxeditor.namespaces.intermediate.master_data_t_datapoint_types import MasterDataDatapointTypes
    from xknxeditor.namespaces.intermediate.master_data_t_function_types import MasterDataFunctionTypes
    from xknxeditor.namespaces.intermediate.master_data_t_functional_blocks import MasterDataFunctionalBlocks
    from xknxeditor.namespaces.intermediate.master_data_t_functional_blocks_functional_block import MasterDataFunctionalBlocksFunctionalBlock
    from xknxeditor.namespaces.intermediate.master_data_t_functional_blocks_functional_block_parameters import MasterDataFunctionalBlocksFunctionalBlockParameters
    from xknxeditor.namespaces.intermediate.master_data_t_functional_blocks_functional_block_parameters_parameter import MasterDataFunctionalBlocksFunctionalBlockParametersParameter
    from xknxeditor.namespaces.intermediate.master_data_t_interface_object_properties import MasterDataInterfaceObjectProperties
    from xknxeditor.namespaces.intermediate.master_data_t_interface_object_properties_interface_object_property import MasterDataInterfaceObjectPropertiesInterfaceObjectProperty
    from xknxeditor.namespaces.intermediate.master_data_t_interface_object_types import MasterDataInterfaceObjectTypes
    from xknxeditor.namespaces.intermediate.master_data_t_interface_object_types_interface_object_type import MasterDataInterfaceObjectTypesInterfaceObjectType
    from xknxeditor.namespaces.intermediate.master_data_t_languages import MasterDataLanguages
    from xknxeditor.namespaces.intermediate.master_data_t_manufacturers import MasterDataManufacturers
    from xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer import MasterDataManufacturersManufacturer
    from xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_datapoint_roles import MasterDataManufacturersManufacturerDatapointRoles
    from xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_datapoint_types import MasterDataManufacturersManufacturerDatapointTypes
    from xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_function_types import MasterDataManufacturersManufacturerFunctionTypes
    from xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_import_restriction import MasterDataManufacturersManufacturerImportRestriction
    from xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_public_keys import MasterDataManufacturersManufacturerPublicKeys
    from xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_public_keys_public_key import MasterDataManufacturersManufacturerPublicKeysPublicKey
    from xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_public_keys_public_key_rsakey_value import MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue
    from xknxeditor.namespaces.intermediate.master_data_t_manufacturers_manufacturer_space_usages import MasterDataManufacturersManufacturerSpaceUsages
    from xknxeditor.namespaces.intermediate.master_data_t_mask_versions import MasterDataMaskVersions
    from xknxeditor.namespaces.intermediate.master_data_t_medium_types import MasterDataMediumTypes
    from xknxeditor.namespaces.intermediate.master_data_t_medium_types_medium_type import MasterDataMediumTypesMediumType
    from xknxeditor.namespaces.intermediate.master_data_t_product_languages import MasterDataProductLanguages
    from xknxeditor.namespaces.intermediate.master_data_t_product_languages_language import MasterDataProductLanguagesLanguage
    from xknxeditor.namespaces.intermediate.master_data_t_property_data_types import MasterDataPropertyDataTypes
    from xknxeditor.namespaces.intermediate.master_data_t_property_data_types_property_data_type import MasterDataPropertyDataTypesPropertyDataType
    from xknxeditor.namespaces.intermediate.master_data_t_space_usages import MasterDataSpaceUsages
    from xknxeditor.namespaces.intermediate.member_status_t import MemberStatus
    from xknxeditor.namespaces.intermediate.memory_parameter_t import MemoryParameter
    from xknxeditor.namespaces.intermediate.memory_type_t import MemoryType
    from xknxeditor.namespaces.intermediate.memory_union_t import MemoryUnion
    from xknxeditor.namespaces.intermediate.module_arg_t import ModuleArg
    from xknxeditor.namespaces.intermediate.module_def_arg_type_t import ModuleDefArgType
    from xknxeditor.namespaces.intermediate.module_def_dynamic_t import ModuleDefDynamic
    from xknxeditor.namespaces.intermediate.module_def_ld_ctrl_base_choose_t import ModuleDefLdCtrlBaseChoose
    from xknxeditor.namespaces.intermediate.module_def_ld_ctrl_base_choose_t_when import ModuleDefLdCtrlBaseChooseWhen
    from xknxeditor.namespaces.intermediate.module_def_ld_ctrl_compare_prop_t import ModuleDefLdCtrlCompareProp
    from xknxeditor.namespaces.intermediate.module_def_ld_ctrl_invoke_function_prop_t import ModuleDefLdCtrlInvokeFunctionProp
    from xknxeditor.namespaces.intermediate.module_def_ld_ctrl_read_function_prop_t import ModuleDefLdCtrlReadFunctionProp
    from xknxeditor.namespaces.intermediate.module_def_ld_ctrl_write_prop_t import ModuleDefLdCtrlWriteProp
    from xknxeditor.namespaces.intermediate.module_def_load_procedure_t import ModuleDefLoadProcedure
    from xknxeditor.namespaces.intermediate.module_def_load_procedures_t import ModuleDefLoadProcedures
    from xknxeditor.namespaces.intermediate.module_def_static_t import ModuleDefStatic
    from xknxeditor.namespaces.intermediate.module_def_static_t_allocators import ModuleDefStaticAllocators
    from xknxeditor.namespaces.intermediate.module_def_static_t_com_object_refs import ModuleDefStaticComObjectRefs
    from xknxeditor.namespaces.intermediate.module_def_static_t_com_objects import ModuleDefStaticComObjects
    from xknxeditor.namespaces.intermediate.module_def_static_t_com_objects_com_object import ModuleDefStaticComObjectsComObject
    from xknxeditor.namespaces.intermediate.module_def_static_t_parameter_calculations import ModuleDefStaticParameterCalculations
    from xknxeditor.namespaces.intermediate.module_def_static_t_parameter_refs import ModuleDefStaticParameterRefs
    from xknxeditor.namespaces.intermediate.module_def_static_t_parameter_validations import ModuleDefStaticParameterValidations
    from xknxeditor.namespaces.intermediate.module_def_static_t_parameters import ModuleDefStaticParameters
    from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_parameter import ModuleDefStaticParametersParameter
    from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_parameter_memory import ModuleDefStaticParametersParameterMemory
    from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_parameter_property import ModuleDefStaticParametersParameterProperty
    from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_union import ModuleDefStaticParametersUnion
    from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_union_memory import ModuleDefStaticParametersUnionMemory
    from xknxeditor.namespaces.intermediate.module_def_static_t_parameters_union_property import ModuleDefStaticParametersUnionProperty
    from xknxeditor.namespaces.intermediate.module_def_t import ModuleDef
    from xknxeditor.namespaces.intermediate.module_def_t import ModuleDefSubModuleDefs
    from xknxeditor.namespaces.intermediate.module_def_t_arguments import ModuleDefArguments
    from xknxeditor.namespaces.intermediate.module_def_t_arguments_argument import ModuleDefArgumentsArgument
    from xknxeditor.namespaces.intermediate.module_def_t_arguments_argument_alignment import ModuleDefArgumentsArgumentAlignment
    from xknxeditor.namespaces.intermediate.module_instance_t import ModuleInstance
    from xknxeditor.namespaces.intermediate.module_instance_t_arguments import ModuleInstanceArguments
    from xknxeditor.namespaces.intermediate.module_instance_t_arguments_argument import ModuleInstanceArgumentsArgument
    from xknxeditor.namespaces.intermediate.module_t import Module
    from xknxeditor.namespaces.intermediate.module_t_numeric_arg import ModuleNumericArg
    from xknxeditor.namespaces.intermediate.module_t_text_arg import ModuleTextArg
    from xknxeditor.namespaces.intermediate.node_t import Node
    from xknxeditor.namespaces.intermediate.node_t import NodeNodes
    from xknxeditor.namespaces.intermediate.node_t_type import NodeType
    from xknxeditor.namespaces.intermediate.p2_plink_bus_interface_endpoint_t import P2PlinkBusInterfaceEndpoint
    from xknxeditor.namespaces.intermediate.p2_plink_device_endpoint_t import P2PlinkDeviceEndpoint
    from xknxeditor.namespaces.intermediate.p2_plink_endpoint_t import P2PlinkEndpoint
    from xknxeditor.namespaces.intermediate.p2_plinks_t import P2Plinks
    from xknxeditor.namespaces.intermediate.p2_plinks_t_p2_plink import P2PlinksP2Plink
    from xknxeditor.namespaces.intermediate.parameter_base_t import ParameterBase
    from xknxeditor.namespaces.intermediate.parameter_block_layout_t import ParameterBlockLayout
    from xknxeditor.namespaces.intermediate.parameter_calculation_t import ParameterCalculation
    from xknxeditor.namespaces.intermediate.parameter_calculation_t_language import ParameterCalculationLanguage
    from xknxeditor.namespaces.intermediate.parameter_calculation_t_lparameters import ParameterCalculationLparameters
    from xknxeditor.namespaces.intermediate.parameter_calculation_t_rparameters import ParameterCalculationRparameters
    from xknxeditor.namespaces.intermediate.parameter_instance_ref_t import ParameterInstanceRef
    from xknxeditor.namespaces.intermediate.parameter_ref_ref_t import ParameterRefRef
    from xknxeditor.namespaces.intermediate.parameter_ref_t import ParameterRef
    from xknxeditor.namespaces.intermediate.parameter_separator_t import ParameterSeparator
    from xknxeditor.namespaces.intermediate.parameter_separator_t_uihint import ParameterSeparatorUihint
    from xknxeditor.namespaces.intermediate.parameter_type_t import ParameterType
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_color import ParameterTypeTypeColor
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_color_space import ParameterTypeTypeColorSpace
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_date import ParameterTypeTypeDate
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_date_encoding import ParameterTypeTypeDateEncoding
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_float import ParameterTypeTypeFloat
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_float_encoding import ParameterTypeTypeFloatEncoding
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_float_uihint import ParameterTypeTypeFloatUihint
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_ipaddress import ParameterTypeTypeIpaddress
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_ipaddress_address_type import ParameterTypeTypeIpaddressAddressType
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_ipaddress_version import ParameterTypeTypeIpaddressVersion
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_number import ParameterTypeTypeNumber
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_number_type import ParameterTypeTypeNumberType
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_number_uihint import ParameterTypeTypeNumberUihint
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_picture import ParameterTypeTypePicture
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_raw_data import ParameterTypeTypeRawData
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_restriction import ParameterTypeTypeRestriction
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_restriction_base import ParameterTypeTypeRestrictionBase
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_restriction_enumeration import ParameterTypeTypeRestrictionEnumeration
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_restriction_uihint import ParameterTypeTypeRestrictionUihint
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_text import ParameterTypeTypeText
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_time import ParameterTypeTypeTime
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_time_uihint import ParameterTypeTypeTimeUihint
    from xknxeditor.namespaces.intermediate.parameter_type_t_type_time_unit import ParameterTypeTypeTimeUnit
    from xknxeditor.namespaces.intermediate.parameter_validation_t import ParameterValidation
    from xknxeditor.namespaces.intermediate.parameter_validation_t_parameters import ParameterValidationParameters
    from xknxeditor.namespaces.intermediate.procedure_type_t import ProcedureType
    from xknxeditor.namespaces.intermediate.project_t import Project
    from xknxeditor.namespaces.intermediate.project_t_addin_data import ProjectAddinData
    from xknxeditor.namespaces.intermediate.project_t_installations import ProjectInstallations
    from xknxeditor.namespaces.intermediate.project_t_installations_installation import ProjectInstallationsInstallation
    from xknxeditor.namespaces.intermediate.project_t_installations_installation_split_type import ProjectInstallationsInstallationSplitType
    from xknxeditor.namespaces.intermediate.project_t_project_information import ProjectProjectInformation
    from xknxeditor.namespaces.intermediate.project_t_project_information_device_certificates import ProjectProjectInformationDeviceCertificates
    from xknxeditor.namespaces.intermediate.project_t_project_information_history_entries import ProjectProjectInformationHistoryEntries
    from xknxeditor.namespaces.intermediate.project_t_project_information_history_entries_history_entry import ProjectProjectInformationHistoryEntriesHistoryEntry
    from xknxeditor.namespaces.intermediate.project_t_project_information_project_traces import ProjectProjectInformationProjectTraces
    from xknxeditor.namespaces.intermediate.project_t_project_information_tags import ProjectProjectInformationTags
    from xknxeditor.namespaces.intermediate.project_t_project_information_tags_tag import ProjectProjectInformationTagsTag
    from xknxeditor.namespaces.intermediate.project_t_project_information_to_do_items import ProjectProjectInformationToDoItems
    from xknxeditor.namespaces.intermediate.project_t_user_files import ProjectUserFiles
    from xknxeditor.namespaces.intermediate.project_trace_t import ProjectTrace
    from xknxeditor.namespaces.intermediate.project_tracing_level_t import ProjectTracingLevel
    from xknxeditor.namespaces.intermediate.project_type_t import ProjectType
    from xknxeditor.namespaces.intermediate.prop_type_t import PropType
    from xknxeditor.namespaces.intermediate.property_parameter_t import PropertyParameter
    from xknxeditor.namespaces.intermediate.property_union_t import PropertyUnion
    from xknxeditor.namespaces.intermediate.registration_info_t import RegistrationInfo
    from xknxeditor.namespaces.intermediate.registration_info_t_registration_key import RegistrationInfoRegistrationKey
    from xknxeditor.namespaces.intermediate.registration_status_t import RegistrationStatus
    from xknxeditor.namespaces.intermediate.rename_t import Rename
    from xknxeditor.namespaces.intermediate.resource_access_rights_t import ResourceAccessRights
    from xknxeditor.namespaces.intermediate.resource_access_t import ResourceAccess
    from xknxeditor.namespaces.intermediate.resource_addr_space_t import ResourceAddrSpace
    from xknxeditor.namespaces.intermediate.resource_location_t import ResourceLocation
    from xknxeditor.namespaces.intermediate.resource_mgmt_style_t import ResourceMgmtStyle
    from xknxeditor.namespaces.intermediate.resource_name_t import ResourceName
    from xknxeditor.namespaces.intermediate.rfdevice_mode_t import RfdeviceMode
    from xknxeditor.namespaces.intermediate.rfrx_capabilities_t import RfrxCapabilities
    from xknxeditor.namespaces.intermediate.rftx_capabilities_t import RftxCapabilities
    from xknxeditor.namespaces.intermediate.security_mode_t import SecurityMode
    from xknxeditor.namespaces.intermediate.security_t import Security
    from xknxeditor.namespaces.intermediate.segment_base_t import SegmentBase
    from xknxeditor.namespaces.intermediate.space_t import Space
    from xknxeditor.namespaces.intermediate.space_type_t import SpaceType
    from xknxeditor.namespaces.intermediate.space_usage_t import SpaceUsage
    from xknxeditor.namespaces.intermediate.split_info_t import SplitInfo
    from xknxeditor.namespaces.intermediate.split_infos_t import SplitInfos
    from xknxeditor.namespaces.intermediate.text_alignment_t import TextAlignment
    from xknxeditor.namespaces.intermediate.text_encoding_t import TextEncoding
    from xknxeditor.namespaces.intermediate.to_do_item_t import ToDoItem
    from xknxeditor.namespaces.intermediate.to_do_status_t import ToDoStatus
    from xknxeditor.namespaces.intermediate.topology_t import Topology
    from xknxeditor.namespaces.intermediate.topology_t_area import TopologyArea
    from xknxeditor.namespaces.intermediate.topology_t_area_line import TopologyAreaLine
    from xknxeditor.namespaces.intermediate.topology_t_area_line_segment import TopologyAreaLineSegment
    from xknxeditor.namespaces.intermediate.topology_t_area_line_segment_additional_group_addresses import TopologyAreaLineSegmentAdditionalGroupAddresses
    from xknxeditor.namespaces.intermediate.topology_t_area_line_segment_additional_group_addresses_group_address import TopologyAreaLineSegmentAdditionalGroupAddressesGroupAddress
    from xknxeditor.namespaces.intermediate.topology_t_unassigned_devices import TopologyUnassignedDevices
    from xknxeditor.namespaces.intermediate.trade_t import Trade
    from xknxeditor.namespaces.intermediate.trades_t import Trades
    from xknxeditor.namespaces.intermediate.union_parameter_t import UnionParameter
    from xknxeditor.namespaces.intermediate.user_file_t import UserFile
    from xknxeditor.namespaces.intermediate.when_t import When


def __getattr__(name: str) -> object:
    if name in _LAZY:
        import importlib
        module_path, attr = _LAZY[name]
        mod = importlib.import_module(module_path)
        value = getattr(mod, attr)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
