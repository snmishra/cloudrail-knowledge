from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_ecs_target
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_event_target import CloudWatchEventTarget


class CloudWatchEventTargetBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict) -> CloudWatchEventTarget:
        return build_ecs_target(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CLOUD_WATCH_EVENT_TARGET
