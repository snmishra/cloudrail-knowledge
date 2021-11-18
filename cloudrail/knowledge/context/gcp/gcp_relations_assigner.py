from typing import List
from cloudrail.knowledge.context.environment_context.common_component_builder import extract_name_from_gcp_link
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, IterFunctionData, FunctionData
from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator
from cloudrail.knowledge.context.gcp.pseudo_builder import PseudoBuilder
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork


class GcpRelationsAssigner(DependencyInvocation):

    def __init__(self, ctx: GcpEnvironmentContext = None):
        self.pseudo_builder = PseudoBuilder(ctx)
        self.pseudo_builder.create_default_firewalls()

        function_pool = [
            ### VPC network
            FunctionData(self._assign_implied_firewalls_to_vpcs, (ctx.compute_networks,)),
            IterFunctionData(self._assign_firewalls_to_vpcs, ctx.compute_networks, (ctx.compute_firewalls,), [self._assign_implied_firewalls_to_vpcs]),
            ### Compute Instance
            IterFunctionData(self._assign_vpcs_to_instance, ctx.compute_instances, (ctx.compute_networks,), [self._assign_firewalls_to_vpcs]),
        ]

        super().__init__(function_pool, context=ctx)

    ## According to GCP docs, every VPC has 2 implied rules for Ipv4 and IPv6 if enabled:
    ## https://cloud.google.com/vpc/docs/firewalls#default_firewall_rules
    def _assign_implied_firewalls_to_vpcs(self, vpcs: List[GcpComputeNetwork]):
        implied_firewalls = self.pseudo_builder.get_implied_firewalls()
        for vpc in vpcs:
            for firewall in implied_firewalls:
                firewall.network = vpc.self_link
            vpc.firewalls.extend(implied_firewalls)

    @staticmethod
    def _assign_firewalls_to_vpcs(vpc: GcpComputeNetwork, firewalls: List[GcpComputeFirewall]):
        def get_firewalls_vpc():
            firewalls_list = [firewall for firewall in firewalls if extract_name_from_gcp_link(firewall.network) == vpc.name]
            return firewalls_list

        vpc.firewalls.extend(ResourceInvalidator.get_by_logic(get_firewalls_vpc, False))

    @staticmethod
    def _assign_vpcs_to_instance(instance: GcpComputeInstance, vpcs: List[GcpComputeNetwork]):
        def get_instance_vpcs():
            instance_vpcs = [vpc for vpc in vpcs if any(extract_name_from_gcp_link(interface.network) == vpc.name for interface in instance.network_interfaces)]
            return instance_vpcs

        instance.vpc_networks = ResourceInvalidator.get_by_logic(get_instance_vpcs, True, instance, 'Unable to find interface related VPC network')
