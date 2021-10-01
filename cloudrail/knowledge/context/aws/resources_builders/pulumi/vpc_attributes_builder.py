from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_vpc_attribute
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class VpcAttributeBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_vpc_attribute(attributes, True)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_VPC


class DefaultVpcAttributeBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_vpc_attribute(attributes, False)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DEFAULT_VPC
