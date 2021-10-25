from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_launch_with_vm_shield_rule import ComputeInstanceLaunchWithVmShieldRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestComputeInstanceLaunchWithVmShieldRule(GcpBaseRuleTest):
    def get_rule(self):
        return ComputeInstanceLaunchWithVmShieldRule()

    @rule_test('both_vptm_and_integrity_disabled_secure_boot_enabled', should_alert=True)
    def test_enable_neither_vptm_nor_integrity(self, rule_result: RuleResponse):
        pass

    @rule_test('all_attributes_enabled', should_alert=False)
    def test_enable_vtpm_and_integrity(self, rule_result: RuleResponse):
        pass

    @rule_test('vtpm_and_secure_boot_enabled_integrity_disabled', should_alert=True)
    def test_enable_vtpm_not_integrity(self, rule_result: RuleResponse):
        pass

    @rule_test('vtpm_and_integrity_enabled_secure_boot_disabled', should_alert=True)
    def test_no_secure_boot(self, rule_result: RuleResponse):
        pass
