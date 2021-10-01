from typing import List

from cloudrail.knowledge.context.aws.resources_builders.pulumi.aws_pulumi_builder import AwsPulumiBuilder
from cloudrail.knowledge.context.aws.resources_builders.pulumi.pulumi_resource_builder_helper import build_inline_network_acl_rules
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRule


class NetworkAclInlineRulesBuilder(AwsPulumiBuilder):

    def do_build(self, attributes) -> List[SecurityGroupRule]:
        return build_inline_network_acl_rules(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_NETWORK_ACL


class DefaultNetworkAclInlineRulesBuilder(NetworkAclInlineRulesBuilder):

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DEFAULT_NETWORK_ACL
