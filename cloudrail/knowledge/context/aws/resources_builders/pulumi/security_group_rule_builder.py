from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_security_group_rule
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class SecurityGroupRuleBuilder(AwsPulumiBuilder):

    def do_build(self, attributes):
        return build_security_group_rule(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_SECURITY_GROUP_RULE
