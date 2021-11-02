from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_no_serial_port_connection_rule import ComputeInstanceNoSerialPortConnectionRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestComputeInstanceNoSerialPortConnectionRule(GcpBaseRuleTest):
    def get_rule(self):
        return ComputeInstanceNoSerialPortConnectionRule()

    @rule_test('compute_both_serial_enabled', should_alert=True, number_of_issue_items=2)
    def test_compute_both_serial_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('compute_no_serial_enabled', should_alert=False)
    def test_compute_no_serial_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('compute_one_serial_enabled', should_alert=True)
    def test_compute_one_serial_enabled(self, rule_result: RuleResponse):
        pass
