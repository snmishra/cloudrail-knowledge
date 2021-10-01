from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_elasticache_subnet_group
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ElastiCacheSubnetGroupBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_elasticache_subnet_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ELASTICACHE_SUBNET_GROUP
