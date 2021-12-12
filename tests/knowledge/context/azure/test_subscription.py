from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from tests.knowledge.context.azure_context_test import AzureNoCloudAccountContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestSubscription(AzureNoCloudAccountContextTest):

    def get_component(self):
        return 'subscription'

    @context(module_path="basic", test_options=TestOptions(run_drift_detection=False))
    def test_basic(self, ctx: AzureEnvironmentContext):
        subscription = next((subscription for subscription in ctx.subscriptions if subscription.subscription_name == 'dev_alon'), None)
        self.assertIsNotNone(subscription)
        self.assertEqual(subscription.subscription_id, '00000000-0000-0000-0000-000000000000')
