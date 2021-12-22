from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.event_hub.azure_event_hub_namespace import AzureEventHubNamespace, EventHubNamespaceSku
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import create_terraform_system_managed_identity
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class EventHubNamespaceBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureEventHubNamespace:
        return AzureEventHubNamespace(name=attributes['name'],
                                      namespace_id=attributes['id'],
                                      sku=EventHubNamespaceSku(attributes['sku']),
                                      capacity=attributes.get('capacity', 2),
                                      auto_inflate_enabled=attributes.get('auto_inflate_enabled', False),
                                      system_managed_identity=create_terraform_system_managed_identity(attributes),
                                      maximum_throughput_units=int(attributes.get('maximum_throughput_units', 0)))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_EVENTHUB_NAMESPACE
