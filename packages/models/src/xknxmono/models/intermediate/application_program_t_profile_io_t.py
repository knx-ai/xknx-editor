from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class ApplicationProgramProfileIo:
    """
    :ivar supports_co_apblock_wise_transfer: registration-relevant
    :ivar max_associations_per_group_object: registration-relevant
    :ivar max_recipient_table_entries: registration-relevant
    :ivar max_publisher_table_entries: registration-relevant
    :ivar max_access_token_list_entries: registration-relevant
    :ivar max_group_address_routing_table_entries: registration-relevant
    :ivar routable_datapoint_main_types: registration-relevant
    """

    class Meta:
        global_type = False

    supports_co_apblock_wise_transfer: bool = field(
        default=True,
        metadata={
            "name": "SupportsCoAPBlockWiseTransfer",
            "type": "Attribute",
        },
    )
    max_associations_per_group_object: int = field(
        default=20,
        metadata={
            "name": "MaxAssociationsPerGroupObject",
            "type": "Attribute",
        },
    )
    max_recipient_table_entries: int = field(
        default=0,
        metadata={
            "name": "MaxRecipientTableEntries",
            "type": "Attribute",
        },
    )
    max_publisher_table_entries: int = field(
        default=0,
        metadata={
            "name": "MaxPublisherTableEntries",
            "type": "Attribute",
        },
    )
    max_access_token_list_entries: int = field(
        default=0,
        metadata={
            "name": "MaxAccessTokenListEntries",
            "type": "Attribute",
        },
    )
    max_group_address_routing_table_entries: None | int = field(
        default=None,
        metadata={
            "name": "MaxGroupAddressRoutingTableEntries",
            "type": "Attribute",
        },
    )
    routable_datapoint_main_types: list[str] = field(
        default_factory=list,
        metadata={
            "name": "RoutableDatapointMainTypes",
            "type": "Attribute",
            "tokens": True,
        },
    )
