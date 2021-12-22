from typing import Optional

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.event_hub.azure_event_hub_namespace import AzureEventHubNamespace, EventHubNamespaceSku
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity, ManagedIdentityType
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class EventHubNamespaceBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureEventHubNamespace:
        managed_identity: Optional[AzureManagedIdentity] = None
        if identity := attributes.get('identity'):
            identity = identity[0]
            managed_identity = AzureManagedIdentity(principal_id=identity['principal_id'],
                                                    tenant_id=identity['tenant_id'],
                                                    identity_type=ManagedIdentityType.SYSTEM_ASSIGNED)
        return AzureEventHubNamespace(name=attributes['name'],
                                      namespace_id=attributes['id'],
                                      sku=EventHubNamespaceSku(attributes['sku']),
                                      capacity=attributes.get('capacity', 2),
                                      auto_inflate_enabled=attributes.get('auto_inflate_enabled', False),
                                      system_managed_identity=managed_identity,
                                      maximum_throughput_units=int(attributes.get('maximum_throughput_units', 0)))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_EVENTHUB_NAMESPACE
