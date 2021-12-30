from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import ApiGatewayIntegration
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_stage import ApiGatewayStage
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import \
    build_rest_api_gw, build_api_gateway_method_settings, build_rest_api_gw_policy, build_rest_api_gw_mapping, \
    build_rest_api_gw_domain, build_api_gateway_integration, build_api_gateway_method, build_api_gateway_stage


class RestApiGwBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_rest_api_gw(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_REST_API_GW


class ApiGatewayMethodSettingsBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_api_gateway_method_settings(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_REST_API_GW_METHOD_SETTINGS


class RestApiGwPolicyBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_rest_api_gw_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_API_GATEWAY_REST_API_POLICY


class RestApiGwMappingBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_rest_api_gw_mapping(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_API_GATEWAY_BASE_PATH_MAPPING


class RestApiGwDomainBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_rest_api_gw_domain(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_API_GATEWAY_DOMAIN_NAME


class ApiGateWayIntegrationBuilder(AwsPulumiBuilder):

    def do_build(self, attributes) -> ApiGatewayIntegration:
        return build_api_gateway_integration(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_API_GATEWAY_INTEGRATION


class ApiGateWayMethodBuilder(AwsPulumiBuilder):

    def do_build(self, attributes) -> ApiGatewayMethod:
        return build_api_gateway_method(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_API_GATEWAY_METHOD


class ApiGatewayStageBuilder(AwsPulumiBuilder):

    def do_build(self, attributes) -> ApiGatewayStage:
        return build_api_gateway_stage(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_API_GATEWAY_STAGE
