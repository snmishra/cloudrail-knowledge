from abc import abstractmethod
from typing import List, Dict, Optional, Union

from cloudrail.knowledge.context.aws.aws_connection import ConnectionType, PortConnectionProperty
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.network.azure_nic import AzureNetworkInterfaceController
from cloudrail.knowledge.context.azure.network.azure_nsg import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.network.azure_nsg_rule import AzureNetworkSecurityRule
from cloudrail.knowledge.context.azure.vm.azure_virtual_machine import AzureVirtualMachine
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils.utils import is_port_in_range


class VirtualMachineNotPubliclyAccessibleBaseRule(AzureBaseRule):

    def __init__(self, port: int, port_protocol: str):
        self.port: int = port
        self.port_protocol: str = port_protocol

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for vm in env_context.virtual_machines:
            if violating_nic := self._get_violating_nic(vm):
                # What if there is no NSG in NIC and subnet?
                # What if there is NSG attached to both NIC and subnet?
                pass
        return issues

    def _get_violating_nic(self, vm: AzureVirtualMachine) -> Optional[AzureNetworkInterfaceController]:
        for nic in vm.network_resource.network_interfaces:
            for inbound_connection in nic.inbound_connections:
                if inbound_connection.connection_type == ConnectionType.PUBLIC \
                   and isinstance(inbound_connection, PortConnectionProperty) \
                   and any(is_port_in_range(x, self.port) for x in inbound_connection.ports):
                    return nic
        return None

    def _get_violating_nsg_or_rule(self, nic: AzureNetworkInterfaceController) -> Union[AzureNetworkSecurityGroup, AzureNetworkSecurityRule]:
        for nsg_rule in nic.security_group.network_security_rules:
            pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.virtual_machines)


class VirtualMachineNotPubliclyAccessibleRdpRule(VirtualMachineNotPubliclyAccessibleBaseRule):

    def __init__(self):
        super(VirtualMachineNotPubliclyAccessibleRdpRule, self).__init__(3389, 'RDP')

    def get_id(self) -> str:
        return 'car_vm_not_publicly_accessible_rdp'
