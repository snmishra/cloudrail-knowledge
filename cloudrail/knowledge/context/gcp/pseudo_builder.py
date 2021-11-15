import os
import json
from typing import List

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_firewall_builder import ComputeFirewallBuilder
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall
from cloudrail.knowledge.context.mergeable import EntityOrigin


class PseudoBuilder:
    def __init__(self, merged_ctx: GcpEnvironmentContext):
        self.ctx = merged_ctx

    def create_default_firewalls(self):
        if len(self.ctx.compute_firewalls) == 0 \
            or not any(firewall.origin == EntityOrigin.LIVE_ENV for firewall in self.ctx.compute_firewalls):
            current_path = os.path.dirname(os.path.abspath(__file__))
            firewalls_raw_data = os.path.join(current_path + '/pseudo_docs/', 'default_firewalls.json')
            with open(firewalls_raw_data, 'r') as data:
                firewalls = json.load(data)
            firewalls_list: List[GcpComputeFirewall] = []
            for firewall in firewalls['value']:
                firewalls_list.append(ComputeFirewallBuilder.do_build(ComputeFirewallBuilder, firewall))
            self.ctx.compute_firewalls.extend(firewalls_list)
