
from typing import Set, Optional, List
from cloudrail.knowledge.context.connection import ConnectionDirectionType, ConnectionType, PortConnectionProperty
from cloudrail.knowledge.context.gcp.resources.networking_config.network_entity import GcpConnection, NetworkEntity
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall, FirewallRuleAction
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.utils import is_port_in_range


class GcpConnectionEvaluator:

    @staticmethod
    def firewalls_allowing_public_conns_on_port(network_entity: NetworkEntity, port: int) -> Optional[Set[GcpComputeFirewall]]:
        conns = [conn for conn in network_entity.inbound_connections
                 if GcpConnectionEvaluator._is_effected_ip_protocol(conn, IpProtocol('TCP'))
                 and GcpConnectionEvaluator._is_public_inbound_conn(conn)
                 and GcpConnectionEvaluator._is_port_conn(conn)
                 and any(is_port_in_range(ports, port) for ports in conn.connection_property.ports)]
        if not GcpConnectionEvaluator._evaluate_if_denied(conns):
            return {conn.firewall for conn in conns if conn.firewall_action == FirewallRuleAction.ALLOW}
        return None

    @staticmethod
    def _evaluate_if_denied(conns_list: List[GcpConnection]) -> bool:
        if conns_list:
            conns_list = sorted(conns_list, key=lambda rule: rule.priority)
            return conns_list[0].firewall_action == FirewallRuleAction.DENY
        return False

    @staticmethod
    def _is_public_inbound_conn(conn: GcpConnection) -> bool:
        return conn.connection_type == ConnectionType.PUBLIC \
            and conn.connection_direction_type == ConnectionDirectionType.INBOUND \
                and conn.connection_property.cidr_block == '0.0.0.0/0'

    @staticmethod
    def _is_port_conn(conn: GcpConnection) -> bool:
        return isinstance(conn.connection_property, PortConnectionProperty)

    @staticmethod
    def _is_effected_ip_protocol(conn: GcpConnection, ip_protocol: IpProtocol) -> bool:
        return ip_protocol == conn.connection_property.ip_protocol_type or \
               IpProtocol.ALL == conn.connection_property.ip_protocol_type
