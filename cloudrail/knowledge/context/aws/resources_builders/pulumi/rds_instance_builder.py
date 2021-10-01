from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_rds_db_instance
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class RdsInstanceBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        attributes["tf_res_type"] = self.get_service_name()
        return build_rds_db_instance(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DB_INSTANCE
