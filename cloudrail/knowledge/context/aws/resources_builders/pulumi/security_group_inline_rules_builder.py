from typing import List

from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_inline_security_group_rules
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRule


class SecurityGroupInlineRulesBuilder(AwsPulumiBuilder):

    def do_build(self, attributes) -> List[SecurityGroupRule]:
        return build_inline_security_group_rules(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_SECURITY_GROUP


class DefaultSecurityGroupInlineRulesBuilder(SecurityGroupInlineRulesBuilder):

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DEFAULT_SECURITY_GROUP
