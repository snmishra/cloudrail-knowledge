from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_type import AzureAppServiceType
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.azure.resources.webapp.constants import FieldMode

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class FunctionAppBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'app-service.json'

    def do_build(self, attributes: dict) -> AzureFunctionApp:
        if AzureAppServiceType.FUNCTION_APP.value in attributes['kind']:
            client_cert_mode: FieldMode = None
            if attributes['properties']['clientCertMode']:
                client_cert_mode = FieldMode(attributes['properties']['clientCertMode'])
            return AzureFunctionApp(name=attributes['name'],
                                    client_cert_mode=client_cert_mode,
                                    https_only=attributes['properties']['httpsOnly'])
        return None
