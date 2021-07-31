from typing import List

from cloudrail.knowledge.context.azure.network.azure_nic import AzureNetworkInterfaceController


class NetworkResource:
    def __init__(self):
        self.network_interfaces: List[AzureNetworkInterfaceController] = []

    @property
    def inbound_connections(self):
        return [inbound_connection for nic in self.network_interfaces for inbound_connection in nic.inbound_connections]

    @property
    def outbound_connections(self):
        return [outbound_connection for nic in self.network_interfaces for outbound_connection in nic.outbound_connections]
