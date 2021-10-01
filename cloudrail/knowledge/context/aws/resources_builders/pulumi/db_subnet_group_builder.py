from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_db_subnet_group
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class DbSubnetGroupBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_db_subnet_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DB_SUBNET_GROUP
