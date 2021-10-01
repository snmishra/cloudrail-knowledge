from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_default_vpc
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class DefaultVpcBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_default_vpc(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DEFAULT_VPC
