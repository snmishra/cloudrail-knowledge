from unittest import TestCase

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.context.azure.storage.azure_storage_account_network_rules import AzureStorageAccountNetworkRules
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_storage_account_default_network_deny_rule import EnsureStorageAccountDefaultNetworkDenyRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureStorageAccountDefaultNetworkDenyRule(TestCase):

    def setUp(self):
        self.rule = EnsureStorageAccountDefaultNetworkDenyRule()

    def test_storage_account_deny_default_network(self):
        # Arrange
        storage_account: AzureStorageAccount = create_empty_entity(AzureStorageAccount)
        network_rule: AzureStorageAccountNetworkRules = create_empty_entity(AzureStorageAccountNetworkRules)
        network_rule.default_action = 'Deny'
        storage_account.network_rules = network_rule
        context = AzureEnvironmentContext(storage_accounts=AliasesDict(storage_account))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_storage_account_allow_default_network(self):
        # Arrange
        storage_account: AzureStorageAccount = create_empty_entity(AzureStorageAccount)
        network_rule: AzureStorageAccountNetworkRules = create_empty_entity(AzureStorageAccountNetworkRules)
        network_rule.default_action = 'Allow'
        storage_account.network_rules = network_rule
        context = AzureEnvironmentContext(storage_accounts=AliasesDict(storage_account))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
