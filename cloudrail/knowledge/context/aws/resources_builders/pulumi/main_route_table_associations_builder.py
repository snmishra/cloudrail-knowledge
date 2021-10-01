from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_main_route_table_association
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class MainRouteTableAssociationsBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_main_route_table_association(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_MAIN_ROUTE_TABLE_ASSOCIATION
