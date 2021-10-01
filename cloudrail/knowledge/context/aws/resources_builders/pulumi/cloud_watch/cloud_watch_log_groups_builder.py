from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_cloud_watch_log_groups
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudWatchLogGroupsBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_cloud_watch_log_groups(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CLOUDWATCH_LOG_GROUP
