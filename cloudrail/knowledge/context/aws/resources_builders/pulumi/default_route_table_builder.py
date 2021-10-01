from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_default_route_table
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class DefaultRouteTableBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_default_route_table(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DEFAULT_ROUTE_TABLE
