from cloudrail.knowledge.rules.azure.non_context_aware.azure_defender_enabled_rules import NonCarAzureKubernetesDefenderEnabled

from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestNonCarAzureKubernetesDefenderEnabled(AzureBaseRuleTest):

    def get_rule(self):
        return NonCarAzureKubernetesDefenderEnabled()

    def test_defender_for_container_registry_enabled(self):
        self.run_test_case('defender_for_az_kubernetes_enabled', should_alert=False)

    def test_defender_for_container_registry_disabled(self):
        self.run_test_case('defender_for_az_kubernetes_disabled', should_alert=True)
