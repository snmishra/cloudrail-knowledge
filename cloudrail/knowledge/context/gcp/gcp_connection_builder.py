from typing import Set
from cloudrail.knowledge.context.connection import ConnectionType, PortConnectionProperty, ConnectionDirectionType
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, IterFunctionData
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import FirewallRuleAction, GcpComputeFirewallDirection
from cloudrail.knowledge.context.gcp.resources.networking_config.network_entity import NetworkEntity, GcpConnection
from cloudrail.knowledge.utils.utils import is_public_ip_range


class GcpConnectionBuilder(DependencyInvocation):

    def __init__(self, ctx: GcpEnvironmentContext):
        network_entities = ctx.get_all_network_entities()
        function_pool = [
            IterFunctionData(self._assign_inbound_public_port_connections, network_entities, ()),
        ]

        super().__init__(function_pool, context=None)

    def _assign_inbound_public_port_connections(self, network_entity: NetworkEntity):
        gcp_connections_set = self._get_gcp_connections_set(network_entity)
        for conn in gcp_connections_set:
            if conn.connection_type == ConnectionType.PUBLIC and conn.connection_direction_type == ConnectionDirectionType.INBOUND:
                network_entity.inbound_connections.add(conn)

    ## Evaluation of GCP connections, fowllowing GCP doc: https://cloud.google.com/vpc/docs/firewalls
    def _get_gcp_connections_set(self, network_entity: NetworkEntity) -> Set[GcpConnection]:
        allowed_denied_connections_set: Set[GcpConnection] = set()
        for firewall in network_entity.firewalls:
            connection_direction = ConnectionDirectionType.INBOUND if firewall.direction == GcpComputeFirewallDirection.INGRESS else ConnectionDirectionType.OUTBOUND
            for cidr in firewall.firewall_ip_ranges:
                connection_type = ConnectionType.PUBLIC if is_public_ip_range(cidr) else ConnectionType.PRIVATE
                for rule in firewall.allow:
                    allowed_denied_connections_set.add(GcpConnection(connection_type=connection_type,
                                                                     connection_property=PortConnectionProperty(rule.ports.port_ranges, cidr, rule.protocol),
                                                                     connection_direction_type=connection_direction,
                                                                     firewall_action=FirewallRuleAction.ALLOW,
                                                                     priority=firewall.priority,
                                                                     firewall=firewall))
                for rule in firewall.deny:
                    allowed_denied_connections_set.add(GcpConnection(connection_type=connection_type,
                                                                     connection_property=PortConnectionProperty(rule.ports.port_ranges, cidr, rule.protocol),
                                                                     connection_direction_type=connection_direction,
                                                                     firewall_action=FirewallRuleAction.DENY,
                                                                     priority=firewall.priority,
                                                                     firewall=firewall))
        allowed_denied_connections_set = sorted(allowed_denied_connections_set, key=lambda rule: rule.priority)
        connections_set = self._filter_conns_by_priority_and_action(allowed_denied_connections_set)
        return connections_set

    @staticmethod
    def _filter_conns_by_priority_and_action(connections_list: Set[GcpConnection]) -> Set[GcpConnection]:
        connections_set: Set[GcpConnection] = set()
        for connection in connections_list:
            if not any(connection.__eq__(list_con) for list_con in connections_set):
                conns_with_same_priority = [list_con for list_con in connections_list if list_con.priority == connection.priority and connection.__eq__(list_con)]
                if len(conns_with_same_priority) > 1:
                    connections_set.add(next(conn for conn in conns_with_same_priority if conn.firewall_action == FirewallRuleAction.DENY))
                else:
                    connections_set.add(connection)
        return connections_set
