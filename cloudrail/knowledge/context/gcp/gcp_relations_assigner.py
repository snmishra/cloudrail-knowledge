from typing import List

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, FunctionData


class GcpRelationsAssigner(DependencyInvocation):

    def __init__(self, ctx: GcpEnvironmentContext = None):
        function_pool = [
            FunctionData(self._assign_clone_sql_database_instance_context, (ctx.sql_database_instances, )),
        ]

        super().__init__(function_pool, context=ctx)

    @staticmethod
    def _assign_clone_sql_database_instance_context(sql_database_instances: List[GcpSqlDatabaseInstance]):
        pass  # TODO: complete sql clone assigner
