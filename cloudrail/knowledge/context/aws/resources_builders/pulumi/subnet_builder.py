from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_subnet
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class SubnetBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        attributes["is_default"] = False
        attributes["tf_res_type"] = self.get_service_name()
        return build_subnet(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_SUBNET
