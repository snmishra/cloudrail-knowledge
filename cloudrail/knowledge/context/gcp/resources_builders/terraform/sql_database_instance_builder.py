from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance

from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder


class SqlDatabaseInstanceBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpSqlDatabaseInstance:
        settings = attributes.get('settings', [{}])[0]
        ip_configuration = self._get_known_value(settings, 'ip_configuration', [{}])[0]
        require_ssl = ip_configuration.get('require_ssl', False)

        return GcpSqlDatabaseInstance(attributes['name'],
                                      require_ssl)

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_SQL_DATABASE_INSTANCE
