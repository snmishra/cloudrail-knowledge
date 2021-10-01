from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import (
    AwsPulumiBuilder,
)
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import (
    build_vpc_endpoint_route_table_association,
)
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class VpcEndpointRouteTableAssociationBuilder(AwsPulumiBuilder):
    def do_build(self, attributes):
        return build_vpc_endpoint_route_table_association(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_VPC_ENDPOINT_ROUTE_TABLE_ASSOCIATION
