from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_api_gateway
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ApiGatewayBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_api_gateway(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_APIGATEWAYV_2_API
