from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_rds_cluster
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class RdsClusterBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_rds_cluster(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_RDS_CLUSTER
