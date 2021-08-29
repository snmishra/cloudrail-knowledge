from typing import Optional, List

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureSubscription(AzureResource):

    def __init__(self, name: str):
        super().__init__(AzureResourceType.NONE)
        self.name: str = name

    def get_keys(self) -> List[str]:
        return [self.subscription_id]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/overview'

    def get_name(self) -> str:
        return self.name

    @property
    def is_tagable(self) -> bool:
        return True
