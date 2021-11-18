from abc import abstractmethod
from typing import List, Set
from dataclasses import dataclass
from cloudrail.knowledge.context.connection import ConnectionInstance, ConnectionDetail, ConnectionType
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource
from cloudrail.knowledge.context.gcp.resources.networking_config.network_info import NetworkInfo
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall, FirewallRuleAction

@dataclass
class GcpConnection(ConnectionDetail):
    connection_type: ConnectionType
    firewall_action: FirewallRuleAction
    priority: int
    firewall: GcpComputeFirewall

    def __hash__(self) -> int:
        return hash((self.connection_type, self.firewall_action, self.priority))


class NetworkEntity(GcpResource, ConnectionInstance):
    """
        This class is the parent of all resources that have a network connection.

        Attributes:
            network_info: Networking information of the entity.
    """
    def __init__(self) -> None:
        super().__init__(GcpResourceType.NONE)
        ConnectionInstance.__init__(self)
        self.network_info: NetworkInfo = NetworkInfo()
        self.inbound_connections: Set[GcpConnection] = set()
        self.outbound_connections: Set[GcpConnection] = set()

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        pass

    @property
    def is_labeled(self) -> bool:
        pass

    @abstractmethod
    def fill_network_info(self):
        pass
