from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.ec2_role_share_rule import Ec2RoleShareRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class Ec2RoleShareRuleTest(AwsBaseRuleTest):
    @classmethod
    def get_rule(cls):
        return Ec2RoleShareRule()

    def test_public_and_private_ec2_same_role(self):
    @rule_test(tf_use_case_folder_name, True)
        tf_use_case_folder_name = 'public_and_private_ec2_same_role'
        pass

    def test_public_and_private_ec2_different_role(self):
    @rule_test(tf_use_case_folder_name, False)
        tf_use_case_folder_name = 'public_and_private_ec2_different_role'
        pass

    def test_public_and_public_ec2_same_role(self):
    @rule_test(tf_use_case_folder_name, False)
        tf_use_case_folder_name = 'public_and_public_ec2_same_role'
        pass

    def test_private_and_private_ec2_same_role(self):
    @rule_test(tf_use_case_folder_name, False)
        tf_use_case_folder_name = 'private_and_private_ec2_same_role'
        pass
