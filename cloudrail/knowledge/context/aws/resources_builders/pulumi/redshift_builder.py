from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_redshift_cluster, build_redshift_subnet_group,\
    build_redshift_logging
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class RedshiftBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_redshift_cluster(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_REDSHIFT_CLUSTER


class RedshiftSubnetGroupBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_redshift_subnet_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_REDSHIFT_SUBNET_GROUP


class RedshiftLoggingBuilder(AwsPulumiBuilder):

    def do_build(self, attributes: dict):
        return build_redshift_logging(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_REDSHIFT_CLUSTER
