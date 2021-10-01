from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_ec2
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class Ec2Builder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_ec2(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_EC2_INSTANCE
