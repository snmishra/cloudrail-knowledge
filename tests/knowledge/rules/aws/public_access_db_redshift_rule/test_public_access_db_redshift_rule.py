from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_redshift_rule import PublicAccessDbRedshiftRule


class PublicAccessDbRedshiftRuleTest(AwsBaseRuleTest):
    @classmethod
    def get_rule(cls):
        return PublicAccessDbRedshiftRule()

    def test_redshift_with_public_access(self):
    @rule_test(tf_use_case_folder_name, True)
        tf_use_case_folder_name = 'redshift_with_public_access'
        pass

    def test_redshift_without_public_access(self):
    @rule_test(tf_use_case_folder_name, False)
        tf_use_case_folder_name = 'redshift_without_public_access'
        pass
