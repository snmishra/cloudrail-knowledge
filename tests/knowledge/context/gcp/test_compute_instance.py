from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestComputeInstance(GcpContextTest):
    def get_component(self):
        return 'compute_instance'

    @context(module_path="basic", test_options=TestOptions(run_cloudformation=False,
                                                           run_cloudmapper=False,
                                                           run_drift_detection=False))
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'cloudrail-test-google-compute-instance'), None)
        self.assertFalse(compute.can_ip_forward)
        self.assertIsNone(compute.hostname)
        self.assertTrue(compute.network_interfaces)
        self.assertTrue(compute.network_interfaces[0].access_config)
        self.assertIsNone(compute.network_interfaces[0].access_config[0].nat_ip)
        self.assertEqual(compute.network_interfaces[0].access_config[0].network_tier, 'PREMIUM')
        self.assertIsNone(compute.network_interfaces[0].access_config[0].public_ptr_domain_name)
        self.assertFalse(compute.network_interfaces[0].alias_ip_range)
        self.assertEqual(compute.network_interfaces[0].network, 'default')
        self.assertIsNone(compute.network_interfaces[0].network_ip)
        self.assertIsNone(compute.network_interfaces[0].nic_type)
        self.assertIsNone(compute.network_interfaces[0].subnetwork)
        self.assertIsNone(compute.network_interfaces[0].subnetwork_project)
        self.assertEqual(compute.project, 'dev-for-tests')
        self.assertIsNone(compute.service_account)
        self.assertIsNone(compute.shielded_instance_config)
        self.assertEqual(compute.zone, 'us-west1-a')
