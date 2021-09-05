from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions
from common.utils.customer_string_utils import CustomerStringUtils


class TestTfDefaultTags(AwsContextTest):

    def get_component(self):
        return "tf_default_tags"

    @context(module_path="basic", test_options=TestOptions(tf_version='>3.33.0', always_use_cache_on_jenkins=True))
    def test_basic(self, ctx: AwsEnvironmentContext):
        self._assert_subnet_vpc_tags(ctx)

    @context(module_path="old_behavior_no_default_tags", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_old_behavior_no_default_tags(self, ctx: AwsEnvironmentContext):
        self._assert_subnet_vpc_tags(ctx)

    def _assert_subnet_vpc_tags(self, ctx: AwsEnvironmentContext):
        vpc = next((vpc for vpc in ctx.vpcs if vpc.tags and 'Provider Tag' in vpc.tags.values()), None)
        subnet = next((subnet for subnet in ctx.subnets
                       if subnet.tags and
                       CustomerStringUtils.to_hashcode('Testing_default_tf_tags') == subnet.tags.get('Environment_hashcode')), None)
        self.assertIsNotNone(vpc)
        self.assertIsNotNone(subnet)
