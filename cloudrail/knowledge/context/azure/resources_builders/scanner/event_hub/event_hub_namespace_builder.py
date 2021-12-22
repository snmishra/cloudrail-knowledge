from typing import Optional

from cloudrail.knowledge.context.azure.resources.event_hub.azure_event_hub_namespace import AzureEventHubNamespace, EventHubNamespaceSku
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity, ManagedIdentityType
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class EventHubNamespaceBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-event-hub-namespaces.json'

    def do_build(self, attributes: dict) -> AzureEventHubNamespace:
        properties: dict = attributes['properties']
        managed_identity: Optional[AzureManagedIdentity] = None
        if identity := attributes.get('identity'):
            managed_identity = AzureManagedIdentity(principal_id=identity['principalId'],
                                                    tenant_id=identity['tenantId'],
                                                    identity_type=ManagedIdentityType(identity['type']))
        return AzureEventHubNamespace(name=attributes['name'],
                                      namespace_id=attributes['id'],
                                      sku=EventHubNamespaceSku(attributes['sku']['tier']),
                                      capacity=attributes['sku']['capacity'],
                                      auto_inflate_enabled=properties['isAutoInflateEnabled'],
                                      system_managed_identity=managed_identity,
                                      maximum_throughput_units=properties['maximumThroughputUnits'])
