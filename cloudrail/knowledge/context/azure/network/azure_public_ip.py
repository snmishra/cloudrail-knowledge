from typing import Optional, List

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzurePublicIp(AzureResource):
    """
        Attributes:
            name: The name of this Public IP
    """
    def __init__(self, name: str):
        super().__init__(AzureResourceType.AZURERM_PUBLIC_IP)
        self.name = name

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
