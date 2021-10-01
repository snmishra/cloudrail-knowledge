from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_sagemaker_endpoint_config
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class SageMakerEndpointConfigBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_sagemaker_endpoint_config(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_SAGEMAKER_ENDPOINT_CONFIGURATION
