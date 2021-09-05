from cloudrail.knowledge.rules.azure.non_context_aware.azure_defender_enabled_rules import NonCarAzureServersDefenderEnabled

from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestNonCarAzureSqlServersDefenderEnabled(AzureBaseRuleTest):

    def get_rule(self):
        return NonCarAzureServersDefenderEnabled()

    def test_defender_for_container_registry_enabled(self):
        self.run_test_case('defender_for_servers_enabled', should_alert=False)

    def test_defender_for_container_registry_disabled(self):
        self.run_test_case('defender_for_servers_disabled', should_alert=True, show_cli_output=True)
