from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_glue_data_catalog_policy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class GlueDataCatalogPolicyBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_glue_data_catalog_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_GLUE_RESOURCE_POLICY
