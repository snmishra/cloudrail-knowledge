from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_rds_cluster_instance
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class RdsClusterInstanceBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_rds_cluster_instance(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_RDS_CLUSTER_INSTANCE
