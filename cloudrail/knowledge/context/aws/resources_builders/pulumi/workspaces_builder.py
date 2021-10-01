from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_workspace
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class WorkspacesBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_workspace(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_WORKSPACES_WORKSPACE
