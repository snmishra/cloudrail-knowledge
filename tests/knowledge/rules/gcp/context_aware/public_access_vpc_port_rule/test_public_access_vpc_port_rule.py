from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.context_aware.public_access_vpc_port_rule import PublicAccessVpcSshPortRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestPublicAccessVpcSshPortRule(GcpBaseRuleTest):
    def get_rule(self):
        return PublicAccessVpcSshPortRule()

    @rule_test('unrestricted_and_pub_ip', should_alert=True)
    def test_unrestricted_and_pub_ip(self, rule_result: RuleResponse):
        pass
