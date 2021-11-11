from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_authentication_disable_rule import SqlDatabaseAuthenticationDisableRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestQqlDatabaseAuthenticationDisable(GcpBaseRuleTest):

    def get_rule(self):
        return SqlDatabaseAuthenticationDisableRule()

    @rule_test('auth_disabled', should_alert=True)
    def test_sql_db_auth_disabled(self, rule_result: RuleResponse):
        pass
