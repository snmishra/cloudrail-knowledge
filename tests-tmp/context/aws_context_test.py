from abc import abstractmethod
from typing import Type

from cloudrail.knowledge.context.cloud_provider import CloudProvider

from common.constants import IacType
from core.api.aws_lambda.services.supported_services_service import SupportedServicesService
from core.aws.aws_terraform_environment_context_builder import AwsTerraformEnvironmentContextBuilder
from core.environment_context.base_environment_context_builder import BaseEnvironmentContextBuilder
from core.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from test.knowledge.context.base_context_test import BaseContextTest


class AwsContextTest(BaseContextTest):
    DUMMY_ACCOUNT_ID: str = '111111111111'
    REGION: str = 'us-east-1'

    def get_supported_services(self):
        return SupportedServicesService.list_aws_supported_services(IacType.TERRAFORM)

    def get_provider_name(self):
        return 'aws'

    def build_context(self, base_scanner_data_for_iac, output_path):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES,
                                                    IacType.TERRAFORM).build(base_scanner_data_for_iac,
                                                   output_path,
                                                   self.DUMMY_ACCOUNT_ID)

    def get_latest_provider_block(self):
        return """
provider "aws" {
    region = "us-east-1"
}
        """

    def get_version_provider_block(self, version):
        return """
provider "aws" {{
    region = "us-east-1"
    version = "{}"
}}  
        """.format(version)

    @abstractmethod
    def get_component(self):
        pass

    def create_context_builder_factory(self) -> Type[BaseEnvironmentContextBuilder]:
        return AwsTerraformEnvironmentContextBuilder


class AwsNoCloudAccountContextTest(AwsContextTest):
    def get_component(self):
        pass

    def build_context(self, base_scanner_data_for_iac, output_path):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES,
                                                    IacType.TERRAFORM).build(
                                                   base_scanner_data_for_iac,
                                                   output_path,
                                                   None)

    def create_context_builder_factory(self) -> Type[BaseEnvironmentContextBuilder]:
        return AwsTerraformEnvironmentContextBuilder
