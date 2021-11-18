from typing import List, Set

from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork


class NetworkInfo:

    def __init__(self):
        self.vpc_networks: List[GcpComputeNetwork] = []
        self.private_ip_addresses: List[str] = []
        self.public_ip_addresses: List[str] = []

    @property
    def firewalls(self) -> Set[GcpComputeFirewall]:
        return {firewall for vpc in self.vpc_networks for firewall in vpc.firewalls}
