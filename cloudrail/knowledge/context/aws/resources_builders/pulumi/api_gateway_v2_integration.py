from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_api_gateway_v2_integration
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ApiGatewayV2IntegrationBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_api_gateway_v2_integration(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_APIGATEWAYV_2_INTEGRATION
