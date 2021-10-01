from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_nat_gateways
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class NatGatewayBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_nat_gateways(attributes)

    def get_service_name(self) -> str:
        return AwsServiceName.AWS_NAT_GATEWAY
