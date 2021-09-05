from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_dms_replication_instance_rule import \
    PublicAccessDmsReplicationInstanceRule


class TestPublicAccessDmsReplicationInstanceRule(AwsBaseRuleTest):

    def get_rule(self):
        return PublicAccessDmsReplicationInstanceRule()

    def test_no_public_access(self):
        self.run_test_case('no_public_access', False)

    def test_public_accessed_using_default_sg(self):
        self.run_test_case('public_accessed_using_default_sg', False)

    def test_default_vpc_public_access(self):
        self.run_test_case('default_vpc_public_access', False)

    def test_public_access_violating_sg(self):
        rule_result = self.run_test_case('public_access_violating_sg', True)
        self.assertTrue("is reachable from the internet due to subnet(s) and route table(s)" in rule_result.issue_items[0].evidence)
        self.assertEqual(rule_result.issue_items[0].exposed.type, 'DMS replication instance')
        self.assertEqual(rule_result.issue_items[0].violating.type, 'Security group')
