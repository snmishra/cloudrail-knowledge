from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_ecs_service
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService


class EcsServiceBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict) -> EcsService:
        return build_ecs_service(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ECS_SERVICE
