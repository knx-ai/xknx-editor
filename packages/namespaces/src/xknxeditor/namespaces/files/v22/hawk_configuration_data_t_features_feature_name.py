from __future__ import annotations

from enum import Enum

__NAMESPACE__ = "http://knx.org/xml/project/22"


class HawkConfigurationDataFeaturesFeatureName(Enum):
    PARAMETER_BYTE_ORDER = "ParameterByteOrder"
    FIRST_APP_OBJECT_IDX = "FirstAppObjectIdx"
    MAX_INDIVIDUAL_ADDRESS = "MaxIndividualAddress"
    MAX_GROUP_ADDRESS = "MaxGroupAddress"
    POLLING_GROUP_SUPPORT = "PollingGroupSupport"
    AUTHORIZE_LEVELS = "AuthorizeLevels"
    RESTART_TIME = "RestartTime"
    UNLOADED_INDIVIDUAL_ADDRESS = "UnloadedIndividualAddress"
    ASSOCIATION_TABLE_FLAVOUR = "AssociationTableFlavour"
    VERIFY_MODE = "VerifyMode"
    MGMT_CONN_TYPES = "MgmtConnTypes"
    PROPERTY_MAPPED_LSMS = "PropertyMappedLsms"
    ALLOC_EXTRA_BYTE = "AllocExtraByte"
    MASKDATA_VERSION = "MaskdataVersion"
    DOWNLOAD_STAMP = "DownloadStamp"
    GROUP_OBJECT_TABLE_FLAVOUR = "GroupObjectTableFlavour"
    INTERFACE_OBJECT_DISCOVERY_BY_IO_LIST = "InterfaceObjectDiscoveryByIoList"
    INTERFACE_OBJECT_DISCOVERY_BY_NETWORK_PARAMETER_READ = (
        "InterfaceObjectDiscoveryByNetworkParameterRead"
    )
    SUPPORTS_CONFIRMED_RESTART = "SupportsConfirmedRestart"
    SUPPORTS_INTERFACE_OBJECTS = "SupportsInterfaceObjects"
    MAY_SUPPORT_LONG_FRAMES = "MaySupportLongFrames"
