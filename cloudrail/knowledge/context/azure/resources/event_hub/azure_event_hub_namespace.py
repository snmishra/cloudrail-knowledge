from enum import Enum
from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.event_hub.event_hub_network_rule_set import EventHubNetworkRuleSet
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting


class EventHubNamespaceSku(Enum):
    BASIC = 'Basic'
    STANDARD = 'Standard'
    PREMIUM = 'Premium'


class AzureEventHubNamespace(AzureResource, IMonitorSettings):
    """
        Attributes:
            name: The name of the Data Lake Analytics Store.
            sku: Defines which tier to use (allowed values: Basic, Standard, and Premium).
            capacity: Specifies the capacity units for a Standard SKU namespace.
            auto_inflate_enabled: Enable or disable Auto Inflate for the EventHub Namespace.
            system_managed_identity: The type of identity which should be used for this EventHub Namespace.
            maximum_throughput_units: Specifies the maximum number of throughput units when Auto Inflate is enabled.
            network_rule_set: Set of network rules to control access to the EventHub Namespace.
    """

    def __init__(self,
                 name: str,
                 namespace_id: str,
                 sku: EventHubNamespaceSku,
                 capacity: int,
                 auto_inflate_enabled: bool,
                 system_managed_identity: AzureManagedIdentity,
                 maximum_throughput_units: int):
        super().__init__(AzureResourceType.AZURERM_EVENTHUB_NAMESPACE)
        self.name: str = name
        self.namespace_id: str = namespace_id
        self.sku: EventHubNamespaceSku = sku
        self.capacity: int = capacity
        self.auto_inflate_enabled: bool = auto_inflate_enabled
        self.system_managed_identity: AzureManagedIdentity = system_managed_identity
        self.maximum_throughput_units: int = maximum_throughput_units
        self.network_rule_set: Optional[EventHubNetworkRuleSet] = None
        self.with_aliases(self.namespace_id, self.name)
        self.monitor_diagnostic_settings: List[AzureMonitorDiagnosticSetting] = []

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.EventHub/namespaces/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'EventHub Namespace' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {}  # todo

    def get_id(self) -> str:
        return self.namespace_id

    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        return self.monitor_diagnostic_settings
