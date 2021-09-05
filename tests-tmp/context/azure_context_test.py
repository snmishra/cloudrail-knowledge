import abc
from typing import Type

from cloudrail.knowledge.context.cloud_provider import CloudProvider

from common.constants import IacType
from core.api.aws_lambda.services.supported_services_service import SupportedServicesService
from core.azure.azure_terraform_environment_context_builder import AzureTerraformEnvironmentContextBuilder
from core.environment_context.base_environment_context_builder import BaseEnvironmentContextBuilder
from core.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from test.knowledge.context.base_context_test import BaseContextTest


class AzureContextTest(BaseContextTest):
    DUMMY_ACCOUNT_ID = 'ae7905ce-4577-4a32-934b-9f662c77869d'
    DUMMY_TENANT_ID = '871cad0f-903e-4648-9655-89b796e7c99e'

    def get_supported_services(self):
        return SupportedServicesService.list_azure_supported_services()

    def get_provider_name(self):
        return 'azure'

    def build_context(self, base_scanner_data_for_iac, output_path):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AZURE,
                                                    IacType.TERRAFORM).build(
            base_scanner_data_for_iac,
            output_path,
            self.DUMMY_ACCOUNT_ID,
            tenant_id=self.DUMMY_TENANT_ID)

    def get_latest_provider_block(self):
        return """
provider "azurerm" {
  features {}
}
        """

    def get_version_provider_block(self, version):
        return """
provider "azurerm" {{
  features {{}}
  version = "{}"
}} 
        """.format(version)

    @abc.abstractmethod
    def get_component(self):
        pass

    def create_context_builder_factory(self) -> Type[BaseEnvironmentContextBuilder]:
        return AzureTerraformEnvironmentContextBuilder


class AzureNoCloudAccountContextTest(AzureContextTest):

    def create_context_builder_factory(self) -> Type[BaseEnvironmentContextBuilder]:
        return AzureTerraformEnvironmentContextBuilder

    def get_component(self):
        pass

    def build_context(self, base_scanner_data_for_iac, output_path):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AZURE, IacType.TERRAFORM).build(base_scanner_data_for_iac,
                                                                                                  output_path,
                                                                                                  None)
