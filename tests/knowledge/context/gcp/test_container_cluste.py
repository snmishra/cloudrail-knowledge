from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestSqlDatabaseInstance(GcpContextTest):
    def get_component(self):
        return 'container_cluster'

    @context(module_path="cluster_empty", test_options=TestOptions(run_drift_detection=False, run_cloudmapper=False))
    def test_cluster_empty(self, ctx: GcpEnvironmentContext):
        pass

    @context(module_path="cluster_with_optional", test_options=TestOptions(run_drift_detection=False, run_cloudmapper=False))
    def test_cluster_with_optional(self, ctx: GcpEnvironmentContext):
        pass

    @context(module_path="cluster_without_optional", test_options=TestOptions(run_drift_detection=False, run_cloudmapper=False))
    def test_cluster_without_optional(self, ctx: GcpEnvironmentContext):
        pass
