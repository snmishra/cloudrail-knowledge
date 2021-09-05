from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_security_groups_port_rule \
    import PublicAccessSecurityGroupsAllPortsRule


class TestPublicAccessSecurityGroupsPortRule(AwsBaseRuleTest):

    def get_rule(self):
        return PublicAccessSecurityGroupsAllPortsRule()

    def test_all_ports_range(self):
        rule_result = self.run_test_case('all_ports_range', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("allows all ports range" in rule_result.issue_items[0].evidence)
        self.assertEqual(rule_result.issue_items[0].exposed.name, 'PublicAccessSecurityGroupsPort test - use case 2')
        self.assertEqual(rule_result.issue_items[0].exposed.type, 'EC2 Instance')
        self.assertEqual(rule_result.issue_items[0].violating.name, 'aws_security_group.sg.name')
        self.assertEqual(rule_result.issue_items[0].violating.type, 'Security group')

    def test_port_22_allowed_from_internet_to_ec2_explicit(self):
        self.run_test_case('port_22_allowed_from_internet_to_ec2_explicit', False)
