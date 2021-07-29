from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_connection import ConnectionType, PortConnectionProperty
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils.utils import is_port_in_range


class VirtualMachineNotPubliclyAccessibleRdpRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'car_vm_not_publicly_accessible_rdp'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for vm in env_context.virtual_machines:
            for inbound_connection in vm.inbound_connections:
                if isinstance(inbound_connection, PortConnectionProperty):
                    if inbound_connection.connection_type == ConnectionType.PUBLIC:
                        if is_port_in_range(inbound_connection.ports, 3389):
                            issues.append(
                                Issue(
                                    f'The Virtual Machine `{vm.get_friendly_name()}` with public IP address public_ip is reachable from the Internet via RDP port',
                                    vm,
                                    vm  # ???
                                ))
                pass
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.app_services)
