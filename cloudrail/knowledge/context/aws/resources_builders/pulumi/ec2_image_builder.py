from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_ami, build_ami_copy, build_ami_from_instance
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class AwsAmiBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_ami(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_AMI


class AwsAmiCopyBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_ami_copy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_AMI_COPY


class AwsAmiFromInstanceBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_ami_from_instance(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_AMI_FROM_INSTANCE
