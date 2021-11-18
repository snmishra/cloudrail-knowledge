from typing import List, Set
from cloudrail.knowledge.utils.port_set import PortSet
from cloudrail.knowledge.utils.utils import flat_list
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_forwarding_rule import GcpComputeForwardingRule
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork


class NetworkInfo:

    def __init__(self):
        self.vpc_networks: List[GcpComputeNetwork] = []
        self.forwarding_rules: List[GcpComputeForwardingRule] = []
        self.private_ip_addresses: List[str] = []
        self.public_ip_addresses: List[str] = []

    @property
    def firewalls(self) -> Set[GcpComputeFirewall]:
        return {firewall for vpc in self.vpc_networks for firewall in vpc.firewalls}

    @property
    def forward_rule_port_range(self) -> List[PortSet]:
        return flat_list([rule.port_range for rule in self.forwarding_rules])
