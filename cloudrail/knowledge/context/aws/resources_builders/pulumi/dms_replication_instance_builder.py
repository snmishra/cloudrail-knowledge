from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_dms_replication_instance,\
    build_dms_replication_instance_subnet_group


class DmsReplicationInstanceBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_dms_replication_instance(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DMS_REPLICATION_INSTANCE


class DmsReplicationInstanceSubnetGroupsBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_dms_replication_instance_subnet_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DMS_REPLICATION_SUBNET_GROUP
