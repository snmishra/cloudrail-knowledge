from dataclasses import dataclass
from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.network.azure_nsg import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.network.azure_public_ip import AzurePublicIp


@dataclass
class IpConfiguration:
    """
        Attributes:
            publicIpId:  TODO by Yoni
            publicIp:TODO by Yoni

    """
    publicIpId: str
    publicIp: AzurePublicIp

class AzureNetworkInterfaceController(AzureResource):
    """
        Attributes:
            name: The name of this NIC
            security_group_id: The id of the security group thats attached to this NIC
            security_group: The actual security group thats attached to this NIC
            ip_configurations: IP configurations of a network interface.
    """

    def __init__(self, name: str, security_group_id: Optional[str]):
        super().__init__(AzureResourceType.AZURERM_NETWORK_INTERFACE)
        self.security_group_id: str = security_group_id
        self.name: str = name
        self.security_group: AzureNetworkSecurityGroup = None
        self.ip_configurations: List[IpConfiguration] = []

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Network/networkInterfaces/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]
