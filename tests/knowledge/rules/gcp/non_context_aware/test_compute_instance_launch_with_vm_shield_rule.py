from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance, GcpComputeInstanceShieldInstCfg
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_launch_with_vm_shield_rule import ComputeInstanceLaunchWithVmShieldRule


class TestComputeInstanceLaunchWithVmShieldRule(TestCase):
    def setUp(self):
        self.rule = ComputeInstanceLaunchWithVmShieldRule()

    @parameterized.expand(
        [
            ["shield_vm_config_no_integrity", True, False, True, True],
            ["shield_vm_config_no_vtpm", True, True, False, True],
            ["shield_vm_config_no_integrity_no_vtpm", True, False, False, True],
            ["shield_vm_config_both_integrity_and_vtpm", True, True, True, False],
            ["shield_vm_config_both_integrity_and_vtpm_enabled_secure_boot_disabled", False, True, True, True]
        ]
    )

    def test_compute_instance_shield_vm_config(self, unused_name: str, secure_boot: bool,
                                               enable_integrity_monitoring: bool, enabled_vtpm: bool, should_alert: bool):
        # Arrange
        compute_instance = create_empty_entity(GcpComputeInstance)
        shielded_instance_config = create_empty_entity(GcpComputeInstanceShieldInstCfg)
        shielded_instance_config.enable_integrity_monitoring = enable_integrity_monitoring
        shielded_instance_config.enable_secure_boot = secure_boot
        shielded_instance_config.enable_vtpm = enabled_vtpm
        compute_instance.shielded_instance_config = shielded_instance_config
        context = GcpEnvironmentContext(compute_instances=[compute_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
