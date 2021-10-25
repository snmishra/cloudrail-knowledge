from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_launch_with_vm_shield_rule import ComputeInstanceLaunchWithVmShieldRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestComputeInstanceLaunchWithVmShieldRule(GcpBaseRuleTest):
    def get_rule(self):
        return ComputeInstanceLaunchWithVmShieldRule()

    @rule_test('enable_neither_vptm_nor_integrity', should_alert=True)
    def test_enable_neither_vptm_nor_integrity(self, rule_result: RuleResponse):
        pass

    @rule_test('enable_vtpm_and_integrity', should_alert=False)
    def test_enable_vtpm_and_integrity(self, rule_result: RuleResponse):
        pass

    @rule_test('enable_vtpm_not_integrity', should_alert=True)
    def test_enable_vtpm_not_integrity(self, rule_result: RuleResponse):
        pass
