from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class OperationsType(Enum):
    WRITE_OPERATION = 'Microsoft.Sql/servers/firewallRules/write'
    DELETE_OPERATION = 'Microsoft.Sql/servers/firewallRules/delete'


class CategoryType(Enum):
    ADMINISTRATIVE = 'Administrative'


@dataclass
class Criteria:
    operation_name: OperationsType
    category: str


class AzureMonitorActivityLogAlertSqlServer(AzureResource):

    def __init__(self, name: str, scopes: List[str], enabled: bool, criteria: Criteria):
        super().__init__(AzureResourceType.AZURERM_MONITOR_ACTIVITY_LOG_ALERT)
        self.name: str = name
        self.scopes: List[str] = scopes
        self.enabled: bool = enabled
        self.criteria: Criteria = criteria

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/overview'

    def get_name(self) -> str:
        return self.name

    @property
    def is_tagable(self) -> bool:
        return True
