from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import (
    AwsPulumiBuilder,
)
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import (
    build_vpc,
    build_vpc_endpoint,
)
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class VpcBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_vpc(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_VPC


class VpcEndpointBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_vpc_endpoint(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_VPC_ENDPOINT
