from typing import Dict, List

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class StorageAccountPublicAccessRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_activity_log_alert_create_update_delete_sql_server_firewall_rule'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        subscription_id = '111'
        issues: List[Issue] = []
        for subscription in env_context.subscriptions:
            for activity_log_alert in env_context.activity_log_alert:
                if subscription.subscription_id in activity_log_alert.scops:
                    subscription_id = activity_log_alert
                    if activity_log_alert.criterian:
                        if activity_log_alert.enabled:
                            y = 1
                        else:
                            x = 1
                else:
                    Issue(
                        'The subscription `{subscription_id}` does not have Activity Log Alerts for Create/Update/Delete SQL Server Firewall Rules events',
                        subscription_id,
                        activity_log_alert)
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.activity_log_alert)
