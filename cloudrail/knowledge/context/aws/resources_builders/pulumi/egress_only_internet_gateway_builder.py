from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_internet_gateway
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ec2.igw_type import IgwType
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway


class EgressOnlyInternetGatewayBuilder(AwsPulumiBuilder):

    def do_build(self, attributes) -> InternetGateway:
        attributes["igw_type"] = IgwType.EGRESS_ONLY_IGW
        attributes["tf_res_type"] = self.get_service_name()
        return build_internet_gateway(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_EGRESS_ONLY_INTERNET_GATEWAY
