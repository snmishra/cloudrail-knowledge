from unittest import TestCase

from cloudrail.knowledge.context.azure.azure_role_definition import AzureRoleDefinition, AzureRoleDefinitionPermission
from cloudrail.knowledge.rules.azure.non_context_aware.no_custom_subscription_owner_roles_exist import NoCustomSubscriptionOwnerRolesExist

from cloudrail.knowledge.rules.base_rule import RuleResultType

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestNoCustomSubscriptionOwnerRoleExist(TestCase):

    def setUp(self):
        self.rule = NoCustomSubscriptionOwnerRolesExist()

    def test_role_exist(self):
        # Arrange
        role_definition: AzureRoleDefinition = create_empty_entity(AzureRoleDefinition)
        role_definition.permissions = [AzureRoleDefinitionPermission(actions=["*"], not_actions=[])]
        context = AzureEnvironmentContext(role_definitions=[role_definition])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_role_does_not_exist(self):
        # Arrange
        role_definition: AzureRoleDefinition = create_empty_entity(AzureRoleDefinition)
        role_definition.permissions = [AzureRoleDefinitionPermission(actions=["create/*/"], not_actions=["*"])]
        context = AzureEnvironmentContext(role_definitions=[role_definition])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
