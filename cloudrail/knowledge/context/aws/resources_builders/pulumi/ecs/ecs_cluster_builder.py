from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import (
    AwsPulumiBuilder,
)
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import (
    build_ecs_cluster,
)
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ecs.ecs_cluster import EcsCluster


class EcsClusterBuilder(AwsPulumiBuilder):
    def do_build(self, attributes: dict) -> EcsCluster:
        return build_ecs_cluster(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ECS_CLUSTER
