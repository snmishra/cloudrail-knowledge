import unittest

from parameterized import parameterized

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.keyvault.azure_key_vault import AzureKeyVault
from cloudrail.knowledge.context.azure.keyvault.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting, \
    AzureMonitorDiagnosticLogsSettings, AzureMonitorDiagnosticLogsRetentionPolicySettings
from cloudrail.knowledge.rules.azure.context_aware.key_vault_diagnostic_logs_enabled_rule import KeyVaultDiagnosticLogsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestKeyVaultDiagnosticLogsEnabled(unittest.TestCase):
    def setUp(self):
        self.rule = KeyVaultDiagnosticLogsEnabledRule()

    @parameterized.expand(
        [
            [None, True],
            [AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', None), True],
            [AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(True, None)), True],
            [AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(False, None)), True],
            [AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(False, AzureMonitorDiagnosticLogsRetentionPolicySettings(False))), True],
            [AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(False, AzureMonitorDiagnosticLogsRetentionPolicySettings(True))), True],
            [AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(False))), True],
            [AzureMonitorDiagnosticSetting('settings_name', 'keyvault_id', AzureMonitorDiagnosticLogsSettings(True, AzureMonitorDiagnosticLogsRetentionPolicySettings(True))), False],
        ]
    )
    def test_states(self, monitor_diagnostic_settings: AzureMonitorDiagnosticSetting, should_alert: bool):
        # Arrange
        key_vault: AzureKeyVault = create_empty_entity(AzureKeyVault)
        key_vault.name = 'tmp-name'
        key_vault.monitor_diagnostic_settings = monitor_diagnostic_settings

        context = AzureEnvironmentContext(key_vaults=AliasesDict(key_vault))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
