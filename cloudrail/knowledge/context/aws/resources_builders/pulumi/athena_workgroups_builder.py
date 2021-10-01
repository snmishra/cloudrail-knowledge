from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_athena_workgroup
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class AthenaWorkGroupsBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_athena_workgroup(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ATHENA_WORKGROUP
