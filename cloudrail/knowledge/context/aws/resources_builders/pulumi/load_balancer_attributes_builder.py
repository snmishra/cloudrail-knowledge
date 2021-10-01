from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_load_balancer_attributes
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class LoadBalancerAttributesBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_load_balancer_attributes(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LOAD_BALANCER
