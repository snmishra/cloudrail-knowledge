from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_ec2_instance_detailed_monitoring_enabled_rule import \
    EnsureEc2InstanceDetailedMonitoringEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureEc2InstanceDetailedMonitoringEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEc2InstanceDetailedMonitoringEnabledRule()

    def test_monitoring_disabled(self):
        self.run_test_case('monitoring_disabled', True, always_use_cache_on_jenkins=True)

    def test_monitoring_enabled(self):
        self.run_test_case('monitoring_enabled', False, always_use_cache_on_jenkins=True)
