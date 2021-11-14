from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import FirewallRuleAction, GcpComputeFirewallDirection
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestComputeFirewall(GcpContextTest):
    def get_component(self):
        return 'compute_firewall'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        for firewall in ctx.compute_firewalls:
            if firewall.origin == EntityOrigin.TERRAFORM:
                self.assertEqual(firewall.network, 'crtest-vpc')
            else:
                self.assertEqual(firewall.network,
                                 'https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/networks/crtest-vpc')
            if firewall.name == 'crtestfirewall1':
                self.assertTrue(firewall.allow)
                self.assertEqual(firewall.allow[0].action, FirewallRuleAction.ALLOW)
                self.assertEqual(firewall.allow[0].protocol, 'TCP')
                self.assertEqual(firewall.allow[0].ports, ["80", "8080", "1000-2000"])
                self.assertFalse(firewall.deny)
                self.assertEqual(firewall.destination_ranges, ["8.8.8.8"])
                self.assertEqual(firewall.direction, GcpComputeFirewallDirection.EGRESS)
                self.assertIsNone(firewall.source_ranges)
            else:
                self.assertTrue(firewall.deny)
                self.assertEqual(firewall.allow[0].action, FirewallRuleAction.DENY)
                self.assertEqual(firewall.allow[0].protocol, 'ESP')
                self.assertFalse(firewall.allow[0].ports)
                self.assertFalse(firewall.allow)
                self.assertIsNone(firewall.destination_ranges)
                self.assertEqual(firewall.direction, GcpComputeFirewallDirection.INGRESS)
                self.assertEqual(firewall.source_ranges, ["8.8.8.8"])
