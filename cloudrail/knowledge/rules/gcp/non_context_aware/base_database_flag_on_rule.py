from abc import abstractmethod
from typing import Dict, List
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class BaseDatabaseFlagOnRule(GcpBaseRule):

    @abstractmethod
    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        pass

    @staticmethod
    def is_flag_on(db_instance: GcpSqlDatabaseInstance, flag_name: str) -> bool:
        return db_instance.settings and db_instance.settings.database_flags and \
               any(db_flag.name == flag_name and db_flag.value == 'on'
                   for db_flag in db_instance.settings.database_flags)

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        pass
