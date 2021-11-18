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
        for entity in network_entities:
            entity.fill_network_info()
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
        allowed_connections = set()
        denied_connections = set()
        for firewall in network_entity.network_info.firewalls:
            connection_direction = ConnectionDirectionType.INBOUND if firewall.direction == GcpComputeFirewallDirection.INGRESS else ConnectionDirectionType.OUTBOUND
            for cidr in firewall.firewall_ip_ranges:
                connection_type = ConnectionType.PUBLIC if is_public_ip_range(cidr) else ConnectionType.PRIVATE
                for rule in firewall.allow:
                    allowed_connections.add(GcpConnection(connection_type=connection_type,
                                                          connection_property=PortConnectionProperty(rule.ports.port_ranges, cidr, rule.protocol),
                                                          connection_direction_type=connection_direction,
                                                          firewall_action=FirewallRuleAction.ALLOW,
                                                          priority=firewall.priority,
                                                          firewall=firewall))
                for rule in firewall.deny:
                    denied_connections.add(GcpConnection(connection_type=connection_type,
                                                         connection_property=PortConnectionProperty(rule.ports.port_ranges, cidr, rule.protocol),
                                                         connection_direction_type=connection_direction,
                                                         firewall_action=FirewallRuleAction.DENY,
                                                         priority=firewall.priority,
                                                         firewall=firewall))
        allowed_connections_by_priority = self._filter_connections_by_priority(allowed_connections)
        denied_connections_by_priority = self._filter_connections_by_priority(denied_connections)
        connections_set = set.union(self._filter_connections_by_action(allowed_connections_by_priority, denied_connections_by_priority),
                                    self._filter_connections_by_action(denied_connections_by_priority, allowed_connections_by_priority))
        return connections_set

    def _filter_connections_by_priority(self, connections_list: Set[GcpConnection]) -> set:
        connections_set = set()
        for connection in connections_list:
            lowest_priority_connection = next((gcp_connection for gcp_connection in connections_list
                                               if self.are_connection_details_equal(gcp_connection, connection)
                                               and connection.priority < gcp_connection.priority), None)
            if lowest_priority_connection:
                connections_set.add(lowest_priority_connection)
            else:
                connections_set.add(connection)
        return connections_set

    def _filter_connections_by_action(self, source_conn_set: Set[GcpConnection], dest_conn_set: Set[GcpConnection]) -> set:
        connections_set = set()
        for source_conn in source_conn_set:
            for dest_conn in dest_conn_set:
                if not self.are_connection_details_equal(source_conn, dest_conn):
                    connections_set.add(source_conn)
                elif dest_conn.firewall_action == FirewallRuleAction.DENY:
                    self._add_to_connections_set(connections_set, dest_conn, source_conn)
                else:
                    self._add_to_connections_set(connections_set, source_conn, dest_conn)
        return connections_set

    @staticmethod
    def _add_to_connections_set(connections_set: set, deny_conn: GcpConnection, allow_conn: GcpConnection):
        if (deny_conn.priority == allow_conn.priority) or (deny_conn.priority < allow_conn.priority):
            connections_set.add(deny_conn)
        else:
            connections_set.add(allow_conn)

    @staticmethod
    def are_connection_details_equal(set_connection_1: GcpConnection, set_connection_2: GcpConnection) -> bool:
        return set_connection_1.connection_property == set_connection_2.connection_property \
            and set_connection_1.connection_type == set_connection_2.connection_type \
                and set_connection_1.connection_direction_type == set_connection_2.connection_direction_type
