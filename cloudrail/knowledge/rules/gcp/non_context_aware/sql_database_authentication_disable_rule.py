from typing import Dict, List
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class SqlDatabaseAuthenticationDisableRule(GcpBaseRule):

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for sql_db in env_context.sql_database_instances:
            if sql_db.database_version and 'SQLSERVER' in sql_db.database_version.value and \
                    sql_db.settings and sql_db.settings.database_flags and \
                    any(db_flag.name == 'contained database authentication' and db_flag.value == 'on'
                        for db_flag in sql_db.settings.database_flags):
                issues.append(
                    Issue(
                        f"The Google Cloud database instance `{sql_db.get_friendly_name()}` "
                        f"has database flag ‘contained database authentication’ set to off.",
                        sql_db,
                        sql_db))
        return issues

    def get_id(self) -> str:
        return 'non_car_cloud_sql_contained_database_authentication_off'

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.sql_database_instances)
