from abc import abstractmethod
from typing import List, Dict
from cloudrail.knowledge.context.gcp.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.connection import ConnectionType, PortConnectionProperty, ConnectionDirectionType
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.gcp_connection_builder import GcpConnection
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.constants.known_ports import KnownPorts
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils.utils import is_port_in_range


class PublicAccessVpcPortRule(GcpBaseRule):

    def __init__(self, port: KnownPorts) -> None:
        self.port = port

    @abstractmethod
    def get_id(self) -> str:
        pass

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.get_all_network_entities())

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for network_entity in env_context.get_all_network_entities():
            if connection := self.conn_accessible_on_port(network_entity, self.port):
                if network_entity.network_info.public_ip_addresses and network_entity.network_info.forwarding_rules
                issues.append(
                    Issue(
                        f"The {network_entity.get_type()} `{network_entity.get_friendly_name()}` "
                        f"with one of the public IP addresses `{', ' .join([x for x in network_entity.network_info.public_ip_addresses])}` "
                        f"is reachable from the Internet via SSH port",
                        network_entity,
                        connection.firewall))
        return issues

    @staticmethod
    def conn_accessible_on_port(network_resource: NetworkEntity, port: int) -> GcpConnection:
        return next((conn for conn in network_resource.inbound_connections if any(conn.connection_type == ConnectionType.PUBLIC \
                   and isinstance(conn.connection_property, PortConnectionProperty) \
                       and any(is_port_in_range(ports, port) for ports in conn.connection_property.ports) \
                           and conn.connection_property.ip_protocol_type in (IpProtocol.ALL, IpProtocol('TCP')) \
                               and conn.connection_direction_type == ConnectionDirectionType.INBOUND \
                                   and conn.connection_property.cidr_block == '0.0.0.0/0' \
                                       for conn in network_resource.inbound_connections)), None)

class PublicAccessVpcSshPortRule(PublicAccessVpcPortRule):

    def get_id(self) -> str:
        return 'car_vpc_not_publicly_accessible_ssh'

    def __init__(self):
        super().__init__(KnownPorts.SSH)
