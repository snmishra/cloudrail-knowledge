from cloudrail.knowledge.context.azure.resources.event_hub.azure_event_hub_namespace import AzureEventHubNamespace, EventHubNamespaceSku
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import create_scanner_system_managed_identity
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class EventHubNamespaceBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-event-hub-namespaces.json'

    def do_build(self, attributes: dict) -> AzureEventHubNamespace:
        properties: dict = attributes['properties']
        return AzureEventHubNamespace(name=attributes['name'],
                                      namespace_id=attributes['id'],
                                      sku=EventHubNamespaceSku(attributes['sku']['tier']),
                                      capacity=attributes['sku']['capacity'],
                                      auto_inflate_enabled=properties['isAutoInflateEnabled'],
                                      system_managed_identity=create_scanner_system_managed_identity(attributes),
                                      maximum_throughput_units=properties['maximumThroughputUnits'])
