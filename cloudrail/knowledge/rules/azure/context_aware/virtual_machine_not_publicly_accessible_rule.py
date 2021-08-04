from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional, Union

from cloudrail.knowledge.context.aws.aws_connection import ConnectionType, PortConnectionProperty, ConnectionDirectionType
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.network.azure_nsg import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.network.azure_nsg_rule import AzureNetworkSecurityRule, NetworkSecurityRuleActionType
from cloudrail.knowledge.context.azure.network.azure_public_ip import AzurePublicIp
from cloudrail.knowledge.context.azure.vm.azure_virtual_machine import AzureVirtualMachine
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils.port_set import PortSet


@dataclass
class ViolationData:
    violating_resource: Optional[Union[AzureNetworkSecurityGroup, AzureNetworkSecurityRule, AzurePublicIp]]
    public_ip: Optional[str]


class VirtualMachineNotPubliclyAccessibleBaseRule(AzureBaseRule):

    def __init__(self, port: int, port_protocol: str):
        self.port: int = port
        self.port_protocol: str = port_protocol

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for vm in env_context.virtual_machines:
            violating = self._get_violating(vm)

            if violating:
                if isinstance(violating.violating_resource, (AzureNetworkSecurityGroup, AzurePublicIp)):
                    if violating.public_ip:
                        public_ip_msg = f'with public IP address `{violating.public_ip}`'
                    else:
                        public_ip_msg = 'with unknown public IP address'
                    issues.append(Issue(f'The Virtual Machine `{vm.get_friendly_name()}` '
                                        f'{public_ip_msg} is reachable from the internet via {self.port_protocol} port', vm, violating.violating_resource))
                else:
                    issues.append(Issue(
                        f'The Virtual Machine `{vm.get_friendly_name()}` with NAT rule '
                        f'`{violating.violating_resource.get_friendly_name()}` is reachable from the internet via {self.port_protocol} port',
                        vm, violating.violating_resource))
        return issues

    def _get_violating(self, vm: AzureVirtualMachine) -> Optional[ViolationData]:
        for nic in vm.network_resource.network_interfaces:
            for ip_config in nic.ip_configurations:
                for inbound_connection in ip_config.inbound_connections:
                    if inbound_connection.connection_type == ConnectionType.PUBLIC \
                            and isinstance(inbound_connection.connection_property, PortConnectionProperty) \
                            and self.port in PortSet(inbound_connection.connection_property.ports):
                        if nic.security_group is None and ip_config.subnet.security_group is None:
                            return ViolationData(ip_config.public_ip, ip_config.public_ip.public_ip_address)
                        return ViolationData(self._get_violating_nsg_or_rule(nic.security_group, ip_config.subnet.security_group),
                                             ip_config.public_ip.public_ip_address)
        return None

    def _get_violating_nsg_or_rule(self, nic_nsg: Optional[AzureNetworkSecurityGroup], subnet_nsg: Optional[AzureNetworkSecurityGroup]):
        for nsg in list(filter(None, [nic_nsg, subnet_nsg])):
            for nsg_rule in nsg.network_security_rules:
                if nsg_rule.direction == ConnectionDirectionType.INBOUND and nsg_rule.access == NetworkSecurityRuleActionType.ALLOW and self.port in nsg_rule.destination_port_ranges:
                    if nsg_rule.is_managed_by_iac:
                        return nsg_rule
                    return nsg
        return None

    @abstractmethod
    def get_id(self) -> str:
        pass

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.virtual_machines)


class VirtualMachineNotPubliclyAccessibleRdpRule(VirtualMachineNotPubliclyAccessibleBaseRule):

    def __init__(self):
        super().__init__(3389, 'RDP')

    def get_id(self) -> str:
        return 'car_vm_not_publicly_accessible_rdp'
