from cloudrail.knowledge.context.azure.resources.iot.azure_iot_hub import AzureIoTHub
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class IoTHubBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-iot-hubs.json'

    def do_build(self, attributes: dict) -> AzureIoTHub:
        return AzureIoTHub(attributes['name'], attributes['properties'].get('enablePurgeProtection', False))
