from xknxmono.models.files.v12.access_t import Access
from xknxmono.models.files.v12.addin_data_t import AddinData
from xknxmono.models.files.v12.application_program_channel_t import (
    ApplicationProgramChannel,
)
from xknxmono.models.files.v12.application_program_dynamic_t import (
    ApplicationProgramDynamic,
)
from xknxmono.models.files.v12.application_program_ipconfig_t import (
    ApplicationProgramIpconfig,
)
from xknxmono.models.files.v12.application_program_ref_t import ApplicationProgramRef
from xknxmono.models.files.v12.application_program_static_t import (
    ApplicationProgramStatic,
)
from xknxmono.models.files.v12.application_program_static_t_address_table import (
    ApplicationProgramStaticAddressTable,
)
from xknxmono.models.files.v12.application_program_static_t_association_table import (
    ApplicationProgramStaticAssociationTable,
)
from xknxmono.models.files.v12.application_program_static_t_binary_data import (
    ApplicationProgramStaticBinaryData,
)
from xknxmono.models.files.v12.application_program_static_t_code import (
    ApplicationProgramStaticCode,
)
from xknxmono.models.files.v12.application_program_static_t_code_absolute_segment import (
    ApplicationProgramStaticCodeAbsoluteSegment,
)
from xknxmono.models.files.v12.application_program_static_t_code_relative_segment import (
    ApplicationProgramStaticCodeRelativeSegment,
)
from xknxmono.models.files.v12.application_program_static_t_com_object_refs import (
    ApplicationProgramStaticComObjectRefs,
)
from xknxmono.models.files.v12.application_program_static_t_com_object_table import (
    ApplicationProgramStaticComObjectTable,
)
from xknxmono.models.files.v12.application_program_static_t_device_compare import (
    ApplicationProgramStaticDeviceCompare,
)
from xknxmono.models.files.v12.application_program_static_t_device_compare_exclude_memory import (
    ApplicationProgramStaticDeviceCompareExcludeMemory,
)
from xknxmono.models.files.v12.application_program_static_t_device_compare_exclude_property import (
    ApplicationProgramStaticDeviceCompareExcludeProperty,
)
from xknxmono.models.files.v12.application_program_static_t_extension import (
    ApplicationProgramStaticExtension,
)
from xknxmono.models.files.v12.application_program_static_t_extension_baggage import (
    ApplicationProgramStaticExtensionBaggage,
)
from xknxmono.models.files.v12.application_program_static_t_fixup_list import (
    ApplicationProgramStaticFixupList,
)
from xknxmono.models.files.v12.application_program_static_t_options import (
    ApplicationProgramStaticOptions,
)
from xknxmono.models.files.v12.application_program_static_t_options_parameter_byte_order import (
    ApplicationProgramStaticOptionsParameterByteOrder,
)
from xknxmono.models.files.v12.application_program_static_t_options_text_parameter_encoding_selector import (
    ApplicationProgramStaticOptionsTextParameterEncodingSelector,
)
from xknxmono.models.files.v12.application_program_static_t_parameter_calculations import (
    ApplicationProgramStaticParameterCalculations,
)
from xknxmono.models.files.v12.application_program_static_t_parameter_refs import (
    ApplicationProgramStaticParameterRefs,
)
from xknxmono.models.files.v12.application_program_static_t_parameter_types import (
    ApplicationProgramStaticParameterTypes,
)
from xknxmono.models.files.v12.application_program_static_t_parameters import (
    ApplicationProgramStaticParameters,
)
from xknxmono.models.files.v12.application_program_static_t_parameters_parameter import (
    ApplicationProgramStaticParametersParameter,
)
from xknxmono.models.files.v12.application_program_static_t_parameters_union import (
    ApplicationProgramStaticParametersUnion,
)
from xknxmono.models.files.v12.application_program_t import ApplicationProgram
from xknxmono.models.files.v12.application_program_type_t import ApplicationProgramType
from xknxmono.models.files.v12.assign_t import Assign
from xknxmono.models.files.v12.binary_data_ref_t import BinaryDataRef
from xknxmono.models.files.v12.binary_data_t import BinaryData
from xknxmono.models.files.v12.building_part_t import BuildingPart
from xknxmono.models.files.v12.bus_access_t import BusAccess
from xknxmono.models.files.v12.calculation_parameter_ref_t import (
    CalculationParameterRef,
)
from xknxmono.models.files.v12.capability_t import Capability
from xknxmono.models.files.v12.catalog_section_t import CatalogSection
from xknxmono.models.files.v12.catalog_section_t_catalog_item import (
    CatalogSectionCatalogItem,
)
from xknxmono.models.files.v12.channel_choose_t import (
    ChannelChoose,
    ChannelChooseWhen,
)
from xknxmono.models.files.v12.channel_independent_block_t import (
    ChannelIndependentBlock,
)
from xknxmono.models.files.v12.com_object_instance_ref_t import ComObjectInstanceRef
from xknxmono.models.files.v12.com_object_instance_ref_t_connectors import (
    ComObjectInstanceRefConnectors,
)
from xknxmono.models.files.v12.com_object_instance_ref_t_connectors_receive import (
    ComObjectInstanceRefConnectorsReceive,
)
from xknxmono.models.files.v12.com_object_instance_ref_t_connectors_send import (
    ComObjectInstanceRefConnectorsSend,
)
from xknxmono.models.files.v12.com_object_parameter_choose_t import (
    ComObjectParameterBlock,
    ComObjectParameterChoose,
    ComObjectParameterChooseWhen,
)
from xknxmono.models.files.v12.com_object_priority_t import ComObjectPriority
from xknxmono.models.files.v12.com_object_ref_ref_t import ComObjectRefRef
from xknxmono.models.files.v12.com_object_ref_t import ComObjectRef
from xknxmono.models.files.v12.com_object_size_t import ComObjectSize
from xknxmono.models.files.v12.com_object_t import ComObject
from xknxmono.models.files.v12.com_table_expectation_t import ComTableExpectation
from xknxmono.models.files.v12.completion_status_t import CompletionStatus
from xknxmono.models.files.v12.datapoint_type_t import DatapointType
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes import (
    DatapointTypeDatapointSubtypes,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype import (
    DatapointTypeDatapointSubtypesDatapointSubtype,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormat,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_bit import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatBit,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumeration,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_enumeration_enum_value import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatEnumerationEnumValue,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_float import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatFloat,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_ref_type import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatRefType,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_reserved import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatReserved,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_signed_integer import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatSignedInteger,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_string import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatString,
)
from xknxmono.models.files.v12.datapoint_type_t_datapoint_subtypes_datapoint_subtype_format_unsigned_integer import (
    DatapointTypeDatapointSubtypesDatapointSubtypeFormatUnsignedInteger,
)
from xknxmono.models.files.v12.dependent_channel_choose_t import (
    DependentChannelChoose,
    DependentChannelChooseWhen,
)
from xknxmono.models.files.v12.device_instance_ref_t import DeviceInstanceRef
from xknxmono.models.files.v12.device_instance_t import DeviceInstance
from xknxmono.models.files.v12.device_instance_t_additional_addresses import (
    DeviceInstanceAdditionalAddresses,
)
from xknxmono.models.files.v12.device_instance_t_additional_addresses_address import (
    DeviceInstanceAdditionalAddressesAddress,
)
from xknxmono.models.files.v12.device_instance_t_binary_data import (
    DeviceInstanceBinaryData,
)
from xknxmono.models.files.v12.device_instance_t_binary_data_binary_data import (
    DeviceInstanceBinaryDataBinaryData,
)
from xknxmono.models.files.v12.device_instance_t_com_object_instance_refs import (
    DeviceInstanceComObjectInstanceRefs,
)
from xknxmono.models.files.v12.device_instance_t_parameter_instance_refs import (
    DeviceInstanceParameterInstanceRefs,
)
from xknxmono.models.files.v12.download_behavior_t import DownloadBehavior
from xknxmono.models.files.v12.enable_t import Enable
from xknxmono.models.files.v12.fixup_t import Fixup
from xknxmono.models.files.v12.function_t import Function
from xknxmono.models.files.v12.group_address_ref_t import GroupAddressRef
from xknxmono.models.files.v12.group_address_style_t import GroupAddressStyle
from xknxmono.models.files.v12.group_address_t import GroupAddress
from xknxmono.models.files.v12.group_addresses_t import GroupAddresses
from xknxmono.models.files.v12.group_addresses_t_group_ranges import (
    GroupAddressesGroupRanges,
)
from xknxmono.models.files.v12.group_range_t import GroupRange
from xknxmono.models.files.v12.hardware2_program_t import Hardware2Program
from xknxmono.models.files.v12.hardware_t import Hardware
from xknxmono.models.files.v12.hardware_t_hardware2_programs import (
    HardwareHardware2Programs,
)
from xknxmono.models.files.v12.hardware_t_products import HardwareProducts
from xknxmono.models.files.v12.hardware_t_products_product import (
    HardwareProductsProduct,
)
from xknxmono.models.files.v12.hardware_t_products_product_attributes import (
    HardwareProductsProductAttributes,
)
from xknxmono.models.files.v12.hardware_t_products_product_attributes_attribute import (
    HardwareProductsProductAttributesAttribute,
)
from xknxmono.models.files.v12.hardware_t_products_product_attributes_attribute_name import (
    HardwareProductsProductAttributesAttributeName,
)
from xknxmono.models.files.v12.hardware_t_products_product_baggages import (
    HardwareProductsProductBaggages,
)
from xknxmono.models.files.v12.hardware_t_products_product_baggages_baggage import (
    HardwareProductsProductBaggagesBaggage,
)
from xknxmono.models.files.v12.hawk_configuration_data_t import HawkConfigurationData
from xknxmono.models.files.v12.hawk_configuration_data_t_features import (
    HawkConfigurationDataFeatures,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_features_feature import (
    HawkConfigurationDataFeaturesFeature,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_features_feature_name import (
    HawkConfigurationDataFeaturesFeatureName,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_interface_objects import (
    HawkConfigurationDataInterfaceObjects,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_interface_objects_interface_object import (
    HawkConfigurationDataInterfaceObjectsInterfaceObject,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_interface_objects_interface_object_property import (
    HawkConfigurationDataInterfaceObjectsInterfaceObjectProperty,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_memory_segments import (
    HawkConfigurationDataMemorySegments,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_memory_segments_memory_segment import (
    HawkConfigurationDataMemorySegmentsMemorySegment,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_memory_segments_memory_segment_access_rights import (
    HawkConfigurationDataMemorySegmentsMemorySegmentAccessRights,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_procedures import (
    HawkConfigurationDataProcedures,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_procedures_procedure import (
    HawkConfigurationDataProceduresProcedure,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_procedures_procedure_value import (
    HawkConfigurationDataProceduresProcedureValue,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_resources import (
    HawkConfigurationDataResources,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_resources_resource import (
    HawkConfigurationDataResourcesResource,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_resources_resource_access_rights import (
    HawkConfigurationDataResourcesResourceAccessRights,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_resources_resource_resource_type import (
    HawkConfigurationDataResourcesResourceResourceType,
)
from xknxmono.models.files.v12.hawk_configuration_data_t_resources_resource_resource_type_flavour import (
    HawkConfigurationDataResourcesResourceResourceTypeFlavour,
)
from xknxmono.models.files.v12.horizontal_alignment_t import HorizontalAlignment
from xknxmono.models.files.v12.ipconfig_assign_t import IpconfigAssign
from xknxmono.models.files.v12.ipconfig_t import Ipconfig
from xknxmono.models.files.v12.knx import Knx
from xknxmono.models.files.v12.language_data_t import LanguageData
from xknxmono.models.files.v12.language_data_t_translation_unit import (
    LanguageDataTranslationUnit,
)
from xknxmono.models.files.v12.language_data_t_translation_unit_translation_element import (
    LanguageDataTranslationUnitTranslationElement,
)
from xknxmono.models.files.v12.language_data_t_translation_unit_translation_element_translation import (
    LanguageDataTranslationUnitTranslationElementTranslation,
)
from xknxmono.models.files.v12.ld_ctrl_abs_segment_t import LdCtrlAbsSegment
from xknxmono.models.files.v12.ld_ctrl_base_t import LdCtrlBase
from xknxmono.models.files.v12.ld_ctrl_clear_cached_object_types_t import (
    LdCtrlClearCachedObjectTypes,
)
from xknxmono.models.files.v12.ld_ctrl_clear_lcfilter_table_t import (
    LdCtrlClearLcfilterTable,
)
from xknxmono.models.files.v12.ld_ctrl_compare_mem_t import LdCtrlCompareMem
from xknxmono.models.files.v12.ld_ctrl_compare_prop_t import LdCtrlCompareProp
from xknxmono.models.files.v12.ld_ctrl_compare_rel_mem_t import LdCtrlCompareRelMem
from xknxmono.models.files.v12.ld_ctrl_connect_t import LdCtrlConnect
from xknxmono.models.files.v12.ld_ctrl_control_variable_t import LdCtrlControlVariable
from xknxmono.models.files.v12.ld_ctrl_declare_prop_desc_t import LdCtrlDeclarePropDesc
from xknxmono.models.files.v12.ld_ctrl_delay_t import LdCtrlDelay
from xknxmono.models.files.v12.ld_ctrl_disconnect_t import LdCtrlDisconnect
from xknxmono.models.files.v12.ld_ctrl_invoke_function_prop_t import (
    LdCtrlInvokeFunctionProp,
)
from xknxmono.models.files.v12.ld_ctrl_load_completed_t import LdCtrlLoadCompleted
from xknxmono.models.files.v12.ld_ctrl_load_image_mem_t import LdCtrlLoadImageMem
from xknxmono.models.files.v12.ld_ctrl_load_image_prop_t import LdCtrlLoadImageProp
from xknxmono.models.files.v12.ld_ctrl_load_image_rel_mem_t import LdCtrlLoadImageRelMem
from xknxmono.models.files.v12.ld_ctrl_load_t import LdCtrlLoad
from xknxmono.models.files.v12.ld_ctrl_map_error_t import LdCtrlMapError
from xknxmono.models.files.v12.ld_ctrl_master_reset_t import LdCtrlMasterReset
from xknxmono.models.files.v12.ld_ctrl_max_length_t import LdCtrlMaxLength
from xknxmono.models.files.v12.ld_ctrl_mem_addr_space_t import LdCtrlMemAddrSpace
from xknxmono.models.files.v12.ld_ctrl_merge_t import LdCtrlMerge
from xknxmono.models.files.v12.ld_ctrl_proc_type_t import LdCtrlProcType
from xknxmono.models.files.v12.ld_ctrl_progress_text_t import LdCtrlProgressText
from xknxmono.models.files.v12.ld_ctrl_read_function_prop_t import (
    LdCtrlReadFunctionProp,
)
from xknxmono.models.files.v12.ld_ctrl_rel_segment_t import LdCtrlRelSegment
from xknxmono.models.files.v12.ld_ctrl_restart_t import LdCtrlRestart
from xknxmono.models.files.v12.ld_ctrl_set_control_variable_t import (
    LdCtrlSetControlVariable,
)
from xknxmono.models.files.v12.ld_ctrl_task_ctrl1_t import LdCtrlTaskCtrl1
from xknxmono.models.files.v12.ld_ctrl_task_ctrl2_t import LdCtrlTaskCtrl2
from xknxmono.models.files.v12.ld_ctrl_task_ptr_t import LdCtrlTaskPtr
from xknxmono.models.files.v12.ld_ctrl_task_segment_t import LdCtrlTaskSegment
from xknxmono.models.files.v12.ld_ctrl_unload_t import LdCtrlUnload
from xknxmono.models.files.v12.ld_ctrl_write_mem_t import LdCtrlWriteMem
from xknxmono.models.files.v12.ld_ctrl_write_prop_t import LdCtrlWriteProp
from xknxmono.models.files.v12.ld_ctrl_write_rel_mem_t import LdCtrlWriteRelMem
from xknxmono.models.files.v12.load_procedure_style_t import LoadProcedureStyle
from xknxmono.models.files.v12.load_procedure_t import LoadProcedure
from xknxmono.models.files.v12.load_procedures_t import LoadProcedures
from xknxmono.models.files.v12.load_procedures_t_load_procedure import (
    LoadProceduresLoadProcedure,
)
from xknxmono.models.files.v12.locations_t import Locations
from xknxmono.models.files.v12.manufacturer_data_t import ManufacturerData
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer import (
    ManufacturerDataManufacturer,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_application_programs import (
    ManufacturerDataManufacturerApplicationPrograms,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_baggages import (
    ManufacturerDataManufacturerBaggages,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_baggages_baggage import (
    ManufacturerDataManufacturerBaggagesBaggage,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_baggages_baggage_file_info import (
    ManufacturerDataManufacturerBaggagesBaggageFileInfo,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_catalog import (
    ManufacturerDataManufacturerCatalog,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_hardware import (
    ManufacturerDataManufacturerHardware,
)
from xknxmono.models.files.v12.manufacturer_data_t_manufacturer_languages import (
    ManufacturerDataManufacturerLanguages,
)
from xknxmono.models.files.v12.mask_version_t import MaskVersion
from xknxmono.models.files.v12.mask_version_t_downward_compatible_masks import (
    MaskVersionDownwardCompatibleMasks,
)
from xknxmono.models.files.v12.mask_version_t_downward_compatible_masks_downward_compatible_mask import (
    MaskVersionDownwardCompatibleMasksDownwardCompatibleMask,
)
from xknxmono.models.files.v12.mask_version_t_management_model import (
    MaskVersionManagementModel,
)
from xknxmono.models.files.v12.mask_version_t_mask_entries import MaskVersionMaskEntries
from xknxmono.models.files.v12.mask_version_t_mask_entries_mask_entry import (
    MaskVersionMaskEntriesMaskEntry,
)
from xknxmono.models.files.v12.master_data_t import MasterData
from xknxmono.models.files.v12.master_data_t_datapoint_types import (
    MasterDataDatapointTypes,
)
from xknxmono.models.files.v12.master_data_t_functional_blocks import (
    MasterDataFunctionalBlocks,
)
from xknxmono.models.files.v12.master_data_t_functional_blocks_functional_block import (
    MasterDataFunctionalBlocksFunctionalBlock,
)
from xknxmono.models.files.v12.master_data_t_functional_blocks_functional_block_parameters import (
    MasterDataFunctionalBlocksFunctionalBlockParameters,
)
from xknxmono.models.files.v12.master_data_t_functional_blocks_functional_block_parameters_parameter import (
    MasterDataFunctionalBlocksFunctionalBlockParametersParameter,
)
from xknxmono.models.files.v12.master_data_t_interface_object_properties import (
    MasterDataInterfaceObjectProperties,
)
from xknxmono.models.files.v12.master_data_t_interface_object_properties_interface_object_property import (
    MasterDataInterfaceObjectPropertiesInterfaceObjectProperty,
)
from xknxmono.models.files.v12.master_data_t_interface_object_types import (
    MasterDataInterfaceObjectTypes,
)
from xknxmono.models.files.v12.master_data_t_interface_object_types_interface_object_type import (
    MasterDataInterfaceObjectTypesInterfaceObjectType,
)
from xknxmono.models.files.v12.master_data_t_languages import MasterDataLanguages
from xknxmono.models.files.v12.master_data_t_manufacturers import (
    MasterDataManufacturers,
)
from xknxmono.models.files.v12.master_data_t_manufacturers_manufacturer import (
    MasterDataManufacturersManufacturer,
)
from xknxmono.models.files.v12.master_data_t_manufacturers_manufacturer_import_restriction import (
    MasterDataManufacturersManufacturerImportRestriction,
)
from xknxmono.models.files.v12.master_data_t_manufacturers_manufacturer_public_keys import (
    MasterDataManufacturersManufacturerPublicKeys,
)
from xknxmono.models.files.v12.master_data_t_manufacturers_manufacturer_public_keys_public_key import (
    MasterDataManufacturersManufacturerPublicKeysPublicKey,
)
from xknxmono.models.files.v12.master_data_t_manufacturers_manufacturer_public_keys_public_key_rsakey_value import (
    MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue,
)
from xknxmono.models.files.v12.master_data_t_mask_versions import MasterDataMaskVersions
from xknxmono.models.files.v12.master_data_t_medium_types import MasterDataMediumTypes
from xknxmono.models.files.v12.master_data_t_medium_types_medium_type import (
    MasterDataMediumTypesMediumType,
)
from xknxmono.models.files.v12.master_data_t_product_languages import (
    MasterDataProductLanguages,
)
from xknxmono.models.files.v12.master_data_t_product_languages_language import (
    MasterDataProductLanguagesLanguage,
)
from xknxmono.models.files.v12.master_data_t_property_data_types import (
    MasterDataPropertyDataTypes,
)
from xknxmono.models.files.v12.master_data_t_property_data_types_property_data_type import (
    MasterDataPropertyDataTypesPropertyDataType,
)
from xknxmono.models.files.v12.memory_parameter_t import MemoryParameter
from xknxmono.models.files.v12.memory_type_t import MemoryType
from xknxmono.models.files.v12.memory_union_t import MemoryUnion
from xknxmono.models.files.v12.parameter_base_t import ParameterBase
from xknxmono.models.files.v12.parameter_calculation_t import ParameterCalculation
from xknxmono.models.files.v12.parameter_calculation_t_language import (
    ParameterCalculationLanguage,
)
from xknxmono.models.files.v12.parameter_calculation_t_lparameters import (
    ParameterCalculationLparameters,
)
from xknxmono.models.files.v12.parameter_calculation_t_rparameters import (
    ParameterCalculationRparameters,
)
from xknxmono.models.files.v12.parameter_instance_ref_t import ParameterInstanceRef
from xknxmono.models.files.v12.parameter_ref_ref_t import ParameterRefRef
from xknxmono.models.files.v12.parameter_ref_t import ParameterRef
from xknxmono.models.files.v12.parameter_separator_t import ParameterSeparator
from xknxmono.models.files.v12.parameter_type_t import ParameterType
from xknxmono.models.files.v12.parameter_type_t_type_color import ParameterTypeTypeColor
from xknxmono.models.files.v12.parameter_type_t_type_color_space import (
    ParameterTypeTypeColorSpace,
)
from xknxmono.models.files.v12.parameter_type_t_type_date import ParameterTypeTypeDate
from xknxmono.models.files.v12.parameter_type_t_type_date_encoding import (
    ParameterTypeTypeDateEncoding,
)
from xknxmono.models.files.v12.parameter_type_t_type_float import ParameterTypeTypeFloat
from xknxmono.models.files.v12.parameter_type_t_type_float_encoding import (
    ParameterTypeTypeFloatEncoding,
)
from xknxmono.models.files.v12.parameter_type_t_type_float_uihint import (
    ParameterTypeTypeFloatUihint,
)
from xknxmono.models.files.v12.parameter_type_t_type_ipaddress import (
    ParameterTypeTypeIpaddress,
)
from xknxmono.models.files.v12.parameter_type_t_type_ipaddress_address_type import (
    ParameterTypeTypeIpaddressAddressType,
)
from xknxmono.models.files.v12.parameter_type_t_type_ipaddress_version import (
    ParameterTypeTypeIpaddressVersion,
)
from xknxmono.models.files.v12.parameter_type_t_type_number import (
    ParameterTypeTypeNumber,
)
from xknxmono.models.files.v12.parameter_type_t_type_number_type import (
    ParameterTypeTypeNumberType,
)
from xknxmono.models.files.v12.parameter_type_t_type_number_uihint import (
    ParameterTypeTypeNumberUihint,
)
from xknxmono.models.files.v12.parameter_type_t_type_picture import (
    ParameterTypeTypePicture,
)
from xknxmono.models.files.v12.parameter_type_t_type_restriction import (
    ParameterTypeTypeRestriction,
)
from xknxmono.models.files.v12.parameter_type_t_type_restriction_base import (
    ParameterTypeTypeRestrictionBase,
)
from xknxmono.models.files.v12.parameter_type_t_type_restriction_enumeration import (
    ParameterTypeTypeRestrictionEnumeration,
)
from xknxmono.models.files.v12.parameter_type_t_type_text import ParameterTypeTypeText
from xknxmono.models.files.v12.parameter_type_t_type_time import ParameterTypeTypeTime
from xknxmono.models.files.v12.parameter_type_t_type_time_uihint import (
    ParameterTypeTypeTimeUihint,
)
from xknxmono.models.files.v12.parameter_type_t_type_time_unit import (
    ParameterTypeTypeTimeUnit,
)
from xknxmono.models.files.v12.procedure_type_t import ProcedureType
from xknxmono.models.files.v12.project_t import Project
from xknxmono.models.files.v12.project_t_addin_data import ProjectAddinData
from xknxmono.models.files.v12.project_t_installations import ProjectInstallations
from xknxmono.models.files.v12.project_t_installations_installation import (
    ProjectInstallationsInstallation,
)
from xknxmono.models.files.v12.project_t_installations_installation_split_type import (
    ProjectInstallationsInstallationSplitType,
)
from xknxmono.models.files.v12.project_t_project_information import (
    ProjectProjectInformation,
)
from xknxmono.models.files.v12.project_t_project_information_history_entries import (
    ProjectProjectInformationHistoryEntries,
)
from xknxmono.models.files.v12.project_t_project_information_history_entries_history_entry import (
    ProjectProjectInformationHistoryEntriesHistoryEntry,
)
from xknxmono.models.files.v12.project_t_project_information_project_traces import (
    ProjectProjectInformationProjectTraces,
)
from xknxmono.models.files.v12.project_t_project_information_to_do_items import (
    ProjectProjectInformationToDoItems,
)
from xknxmono.models.files.v12.project_t_user_files import ProjectUserFiles
from xknxmono.models.files.v12.project_trace_t import ProjectTrace
from xknxmono.models.files.v12.project_tracing_level_t import ProjectTracingLevel
from xknxmono.models.files.v12.prop_type_t import PropType
from xknxmono.models.files.v12.property_parameter_t import PropertyParameter
from xknxmono.models.files.v12.property_union_t import PropertyUnion
from xknxmono.models.files.v12.registration_info_t import RegistrationInfo
from xknxmono.models.files.v12.registration_info_t_registration_key import (
    RegistrationInfoRegistrationKey,
)
from xknxmono.models.files.v12.registration_status_t import RegistrationStatus
from xknxmono.models.files.v12.rename_t import Rename
from xknxmono.models.files.v12.resource_access_rights_t import ResourceAccessRights
from xknxmono.models.files.v12.resource_access_t import ResourceAccess
from xknxmono.models.files.v12.resource_addr_space_t import ResourceAddrSpace
from xknxmono.models.files.v12.resource_location_t import ResourceLocation
from xknxmono.models.files.v12.resource_mgmt_style_t import ResourceMgmtStyle
from xknxmono.models.files.v12.resource_name_t import ResourceName
from xknxmono.models.files.v12.rfdevice_mode_t import RfdeviceMode
from xknxmono.models.files.v12.segment_base_t import SegmentBase
from xknxmono.models.files.v12.space_type_t import SpaceType
from xknxmono.models.files.v12.split_info_t import SplitInfo
from xknxmono.models.files.v12.split_infos_t import SplitInfos
from xknxmono.models.files.v12.text_encoding_t import TextEncoding
from xknxmono.models.files.v12.to_do_item_t import ToDoItem
from xknxmono.models.files.v12.to_do_status_t import ToDoStatus
from xknxmono.models.files.v12.topology_t import Topology
from xknxmono.models.files.v12.topology_t_area import TopologyArea
from xknxmono.models.files.v12.topology_t_area_line import TopologyAreaLine
from xknxmono.models.files.v12.topology_t_area_line_additional_group_addresses import (
    TopologyAreaLineAdditionalGroupAddresses,
)
from xknxmono.models.files.v12.topology_t_area_line_additional_group_addresses_group_address import (
    TopologyAreaLineAdditionalGroupAddressesGroupAddress,
)
from xknxmono.models.files.v12.topology_t_unassigned_devices import (
    TopologyUnassignedDevices,
)
from xknxmono.models.files.v12.trade_t import Trade
from xknxmono.models.files.v12.trades_t import Trades
from xknxmono.models.files.v12.union_parameter_t import UnionParameter
from xknxmono.models.files.v12.user_file_t import UserFile
from xknxmono.models.files.v12.when_t import When

__all__ = [
    "Access",
    "AddinData",
    "ApplicationProgramChannel",
    "ApplicationProgramDynamic",
    "ApplicationProgramIpconfig",
    "ApplicationProgramRef",
    "ApplicationProgramStatic",
    "ApplicationProgramStaticAddressTable",
    "ApplicationProgramStaticAssociationTable",
    "ApplicationProgramStaticBinaryData",
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
    "ApplicationProgramStaticOptions",
    "ApplicationProgramStaticOptionsParameterByteOrder",
    "ApplicationProgramStaticOptionsTextParameterEncodingSelector",
    "ApplicationProgramStaticParameterCalculations",
    "ApplicationProgramStaticParameterRefs",
    "ApplicationProgramStaticParameterTypes",
    "ApplicationProgramStaticParameters",
    "ApplicationProgramStaticParametersParameter",
    "ApplicationProgramStaticParametersUnion",
    "ApplicationProgram",
    "ApplicationProgramType",
    "Assign",
    "BinaryDataRef",
    "BinaryData",
    "BuildingPart",
    "BusAccess",
    "CalculationParameterRef",
    "Capability",
    "CatalogSection",
    "CatalogSectionCatalogItem",
    "ChannelChoose",
    "ChannelChooseWhen",
    "ChannelIndependentBlock",
    "ComObjectInstanceRef",
    "ComObjectInstanceRefConnectors",
    "ComObjectInstanceRefConnectorsReceive",
    "ComObjectInstanceRefConnectorsSend",
    "ComObjectParameterBlock",
    "ComObjectParameterChoose",
    "ComObjectParameterChooseWhen",
    "ComObjectPriority",
    "ComObjectRefRef",
    "ComObjectRef",
    "ComObjectSize",
    "ComObject",
    "ComTableExpectation",
    "CompletionStatus",
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
    "DeviceInstanceRef",
    "DeviceInstance",
    "DeviceInstanceAdditionalAddresses",
    "DeviceInstanceAdditionalAddressesAddress",
    "DeviceInstanceBinaryData",
    "DeviceInstanceBinaryDataBinaryData",
    "DeviceInstanceComObjectInstanceRefs",
    "DeviceInstanceParameterInstanceRefs",
    "DownloadBehavior",
    "Enable",
    "Fixup",
    "Function",
    "GroupAddressRef",
    "GroupAddressStyle",
    "GroupAddress",
    "GroupAddresses",
    "GroupAddressesGroupRanges",
    "GroupRange",
    "Hardware2Program",
    "Hardware",
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
    "IpconfigAssign",
    "Ipconfig",
    "Knx",
    "LanguageData",
    "LanguageDataTranslationUnit",
    "LanguageDataTranslationUnitTranslationElement",
    "LanguageDataTranslationUnitTranslationElementTranslation",
    "LdCtrlAbsSegment",
    "LdCtrlBase",
    "LdCtrlClearCachedObjectTypes",
    "LdCtrlClearLcfilterTable",
    "LdCtrlCompareMem",
    "LdCtrlCompareProp",
    "LdCtrlCompareRelMem",
    "LdCtrlConnect",
    "LdCtrlControlVariable",
    "LdCtrlDeclarePropDesc",
    "LdCtrlDelay",
    "LdCtrlDisconnect",
    "LdCtrlInvokeFunctionProp",
    "LdCtrlLoadCompleted",
    "LdCtrlLoadImageMem",
    "LdCtrlLoadImageProp",
    "LdCtrlLoadImageRelMem",
    "LdCtrlLoad",
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
    "LoadProcedureStyle",
    "LoadProcedure",
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
    "MasterDataDatapointTypes",
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
    "MasterDataManufacturersManufacturerImportRestriction",
    "MasterDataManufacturersManufacturerPublicKeys",
    "MasterDataManufacturersManufacturerPublicKeysPublicKey",
    "MasterDataManufacturersManufacturerPublicKeysPublicKeyRsakeyValue",
    "MasterDataMaskVersions",
    "MasterDataMediumTypes",
    "MasterDataMediumTypesMediumType",
    "MasterDataProductLanguages",
    "MasterDataProductLanguagesLanguage",
    "MasterDataPropertyDataTypes",
    "MasterDataPropertyDataTypesPropertyDataType",
    "MemoryParameter",
    "MemoryType",
    "MemoryUnion",
    "ParameterBase",
    "ParameterCalculation",
    "ParameterCalculationLanguage",
    "ParameterCalculationLparameters",
    "ParameterCalculationRparameters",
    "ParameterInstanceRef",
    "ParameterRefRef",
    "ParameterRef",
    "ParameterSeparator",
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
    "ParameterTypeTypeRestriction",
    "ParameterTypeTypeRestrictionBase",
    "ParameterTypeTypeRestrictionEnumeration",
    "ParameterTypeTypeText",
    "ParameterTypeTypeTime",
    "ParameterTypeTypeTimeUihint",
    "ParameterTypeTypeTimeUnit",
    "ProcedureType",
    "Project",
    "ProjectAddinData",
    "ProjectInstallations",
    "ProjectInstallationsInstallation",
    "ProjectInstallationsInstallationSplitType",
    "ProjectProjectInformation",
    "ProjectProjectInformationHistoryEntries",
    "ProjectProjectInformationHistoryEntriesHistoryEntry",
    "ProjectProjectInformationProjectTraces",
    "ProjectProjectInformationToDoItems",
    "ProjectUserFiles",
    "ProjectTrace",
    "ProjectTracingLevel",
    "PropType",
    "PropertyParameter",
    "PropertyUnion",
    "RegistrationInfo",
    "RegistrationInfoRegistrationKey",
    "RegistrationStatus",
    "Rename",
    "ResourceAccessRights",
    "ResourceAccess",
    "ResourceAddrSpace",
    "ResourceLocation",
    "ResourceMgmtStyle",
    "ResourceName",
    "RfdeviceMode",
    "SegmentBase",
    "SpaceType",
    "SplitInfo",
    "SplitInfos",
    "TextEncoding",
    "ToDoItem",
    "ToDoStatus",
    "Topology",
    "TopologyArea",
    "TopologyAreaLine",
    "TopologyAreaLineAdditionalGroupAddresses",
    "TopologyAreaLineAdditionalGroupAddressesGroupAddress",
    "TopologyUnassignedDevices",
    "Trade",
    "Trades",
    "UnionParameter",
    "UserFile",
    "When",
]
