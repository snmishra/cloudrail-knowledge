from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance, GcpComputeInstanceNetworkInterface, GcpComputeInstanceNetIntfAccessCfg
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_no_public_ip_rule import ComputeInstanceNoPublicIpRule


class TestComputeInstanceNoPublicIpRule(TestCase):
    def setUp(self):
        self.rule = ComputeInstanceNoPublicIpRule()

    @parameterized.expand(
        [
            ["One public ip", "1.1.1.1", None, 1, True],
            ["Both public ip", "1.1.1.1", "2.2.2.2", 2, True],
            ["No public ip", None, None, 0, False],
        ]
    )

    def test_compute_instance_public_ip(self, unused_name: str, public_ip_1: str, public_ip_2: str, isusses: int, should_alert: bool):
        # Arrange
        compute_instance_1 = create_empty_entity(GcpComputeInstance)
        compute_instance_2 = create_empty_entity(GcpComputeInstance)
        if public_ip_1:
            compute_instance_1.network_interfaces = [create_empty_entity(GcpComputeInstanceNetworkInterface)]
            compute_instance_1.network_interfaces[0].access_config = [create_empty_entity(GcpComputeInstanceNetIntfAccessCfg)]
            compute_instance_1.network_interfaces[0].access_config[0].nat_ip = public_ip_1
        if public_ip_2:
            compute_instance_2.network_interfaces = [create_empty_entity(GcpComputeInstanceNetworkInterface)]
            compute_instance_2.network_interfaces[0].access_config = [create_empty_entity(GcpComputeInstanceNetIntfAccessCfg)]
            compute_instance_2.network_interfaces[0].access_config[0].nat_ip = public_ip_2
        context = GcpEnvironmentContext(compute_instances=[compute_instance_1, compute_instance_2])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(isusses, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
