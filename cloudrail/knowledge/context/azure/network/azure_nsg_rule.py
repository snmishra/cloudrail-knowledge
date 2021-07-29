from enum import Enum
from typing import Tuple, List

from cloudrail.knowledge.context.aws.aws_connection import ConnectionDirectionType
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.ip_protocol import IpProtocol


class NetworkSecurityRuleActionType(str, Enum):
    ALLOW = 'Allow'
    DENY = 'Deny'


class PortRange(tuple[int, int]):
    pass


class AzureNetworkSecurityRule(AzureResource):
    """
        Attributes:
            name: The NSG name
            priority
            direction
            access
            protocol
            source_port_ranges
            destination_port_ranges
            source_address_prefix
            destination_address_prefix
            network_security_group_name
    """

    def __init__(self,
                 name: str,
                 priority: int,
                 direction: ConnectionDirectionType,
                 access: NetworkSecurityRuleActionType,
                 protocol: IpProtocol,
                 source_port_ranges: List[PortRange],
                 destination_port_ranges: List[PortRange],
                 source_address_prefix: str,
                 destination_address_prefix: str,
                 network_security_group_name: str
                 ):
        super().__init__(AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.name: str = name
        self.priority: int = priority
        self.direction: ConnectionDirectionType = direction
        self.access: NetworkSecurityRuleActionType = access
        self.protocol: IpProtocol = protocol
        self.source_port_ranges: List[PortRange] = source_port_ranges
        self.destination_port_ranges: List[PortRange] = destination_port_ranges
        # read the docs as this can contain an enum as well, (Optional) CIDR or source IP range or * to match any IP. Tags such as ‘VirtualNetwork’, ‘AzureLoadBalancer’ and ‘Internet’ can also be used
        self.source_address_prefix: str  = source_address_prefix
        # same shit as source
        self.destination_address_prefix: str   = destination_address_prefix
        self.network_security_group_name: str = network_security_group_name
