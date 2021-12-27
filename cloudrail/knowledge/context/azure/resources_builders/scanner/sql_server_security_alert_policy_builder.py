from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_security_alert_policy import AzureMsSqlServerSecurityAlertPolicy, \
    AzureMsSqlServerSecurityAlertPolicyState, AzureMsSqlServerSecurityAlertPolicyDisabledAlerts
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation

class SqlServerSecurityAlertPolicyBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'sql-servers-security-alert-policies.json'

    def do_build(self, attributes: dict) -> AzureMsSqlServerSecurityAlertPolicy:
        properties= attributes['properties']
        ## Disabled Alerts
        disabled_alerts = []
        for alert in properties['disabledAlerts']:
            disabled_alerts.append(enum_implementation(AzureMsSqlServerSecurityAlertPolicyDisabledAlerts, alert))
        return AzureMsSqlServerSecurityAlertPolicy(server_name=attributes['name'],
                                                   state=enum_implementation(AzureMsSqlServerSecurityAlertPolicyState, properties['state']),
                                                   disabled_alerts=disabled_alerts,
                                                   email_account_admins=properties['emailAccountAdmins'],
                                                   email_addresses=properties['emailAddresses'],
                                                   retention_days=properties['retentionDays'],
                                                   storage_account_access_key=properties['storageAccountAccessKey'],
                                                   storage_endpoint=properties['storageEndpoint'])
