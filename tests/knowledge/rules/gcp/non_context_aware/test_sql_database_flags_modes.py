from unittest import TestCase
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance, GcpSqlDBInstanceSettings, \
    GcpSqlDBInstanceSettingsDBFlags, GcpSqlDBInstanceVersion
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_authentication_disable_rule import SqlDatabaseAuthenticationDisableRule


class TestSqlDatabaseFlagsModes(TestCase):

    def setUp(self):
        self.rule = SqlDatabaseAuthenticationDisableRule()

    def test_sql_flag_mode(self):
        # Arrange
        sql = create_empty_entity(GcpSqlDatabaseInstance)
        sql.name = 'name'
        sql.settings = create_empty_entity(GcpSqlDBInstanceSettings)
        sql.settings.database_flags = [GcpSqlDBInstanceSettingsDBFlags('contained database authentication', 'on')]
        sql.database_version = GcpSqlDBInstanceVersion.SQLSERVER_2017_STANDARD
        context = GcpEnvironmentContext(sql_database_instances=[sql])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
