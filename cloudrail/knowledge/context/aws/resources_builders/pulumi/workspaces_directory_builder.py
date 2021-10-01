from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_workspaces_directory
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class WorkspacesDirectoryBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_workspaces_directory(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_WORKSPACES_DIRECTORY
