from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_route_table_associations
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class RouteTableAssociationsBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_route_table_associations(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ROUTE_TABLE_ASSOCIATION
