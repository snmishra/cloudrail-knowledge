from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureApplicationSecurityGroupToNicAssociation(AzureResource):
    """
        Attributes:
            nic_id: The network interface id which needs to be connected to the NSG.
            application_security_group_id: The application security group id which needs to be connected to the NIC.
    """

    def __init__(self, nic_id: str, application_security_group_id: str):
        super().__init__(AzureResourceType.AZURERM_NETWORK_INTERFACE_APPLICATION_SECURITY_GROUP_ASSOCIATION)
        self.nic_id: str = nic_id
        self.application_security_group_id = application_security_group_id

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.get_id()]
