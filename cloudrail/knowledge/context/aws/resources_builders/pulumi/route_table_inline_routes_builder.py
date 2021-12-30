from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ec2.route import Route
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_inline_routes
from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder


class RouteTableInlineRoutesBuilder(AwsPulumiBuilder):

    def do_build(self, attributes) -> List[Route]:
        return build_inline_routes(attributes['route'], attributes['id'], attributes['region'], attributes['account_id'])

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ROUTE_TABLE
