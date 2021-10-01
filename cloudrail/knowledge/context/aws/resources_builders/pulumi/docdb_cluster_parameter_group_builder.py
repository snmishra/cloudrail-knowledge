from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_docdb_cluster_parameter_group
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class DocDbClusterParameterGroupBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_docdb_cluster_parameter_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DOCDB_CLUSTER_PARAMETER_GROUP
