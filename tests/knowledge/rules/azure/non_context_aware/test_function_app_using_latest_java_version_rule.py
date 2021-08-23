from unittest import TestCase

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_non_car_function_app_using_latest_java_version_rule import \
    FunctionAppUsingLatestJavaVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestFunctionAppUseLatestTlsVersionRule(TestCase):

    def setUp(self):
        self.rule = FunctionAppUsingLatestJavaVersionRule()

    @parameterized.expand(
        [
            ['java version linux is 11 the rule should alert', 'java', 'JAVA|11', False],
            ['java version win is 11 the rule should not alert', 'java', '11', False],
            ['java version linux is 1.8 the rule should alert', 'java', 'JAVA|8', True],
            ['java version win is 11 the rule should not alert', 'java', '1.8', True],
            ['java version win is 11 the rule should not alert', 'python', None, False]
        ]
    )
    def test_non_car_function_app_using_latest_java_version(self, unused_name: str, functions_worker_runtime: str, java_version: str, should_alert: bool):
        # Arrange
        function_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        function_app.functions_worker_runtime = functions_worker_runtime
        function_app.java_version = java_version
        context = AzureEnvironmentContext(function_apps=AliasesDict(function_app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
