from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_directory_service
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudDirectoryBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_directory_service(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DIRECTORY_SERVICE_DIRECTORY
