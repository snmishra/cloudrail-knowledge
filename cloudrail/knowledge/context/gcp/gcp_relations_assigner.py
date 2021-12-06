from typing import List

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, IterFunctionData
from cloudrail.knowledge.context.gcp.pseudo_builder import PseudoBuilder
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_global_forwarding_rule import GcpComputeGlobalForwardingRule
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_ssl_policy import GcpComputeSslPolicy
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_subnetwork import GcpComputeSubNetwork
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_proxy import GcpComputeTargetProxy


class GcpRelationsAssigner(DependencyInvocation):

    def __init__(self, ctx: GcpEnvironmentContext = None):
        self.pseudo_builder = PseudoBuilder(ctx)
        self.pseudo_builder.create_default_firewalls()

        function_pool = [
            IterFunctionData(self._assign_ssl_policy, ctx.compute_target_ssl_proxy, (ctx.compute_ssl_policy,)),
            IterFunctionData(self._assign_ssl_policy, ctx.compute_target_https_proxy, (ctx.compute_ssl_policy,)),
            IterFunctionData(self._assign_target_proxy, ctx.compute_global_forwarding_rule, (ctx.get_all_targets_proxy(),)),
            IterFunctionData(self._assign_subnetwork, ctx.compute_networks, (ctx.compute_subnetworks,)),
        ]

        super().__init__(function_pool, context=ctx)

    @staticmethod
    def _assign_ssl_policy(target_proxy: GcpComputeTargetProxy, ssl_policies: AliasesDict[GcpComputeSslPolicy]):
        def get_ssl_policy():
            ssl_policy = ResourceInvalidator.get_by_id(ssl_policies, target_proxy.ssl_policy_identifier, False)
            if not ssl_policy:
                ssl_policy = next((ssl_policy for ssl_policy in ssl_policies if
                                  target_proxy.project_id == ssl_policy.project_id and
                                  target_proxy.ssl_policy_identifier == ssl_policy.name), None)
            return ssl_policy

        # only is_encrypted resources have ssl_policy
        if target_proxy.is_encrypted and not target_proxy.ssl_policy:
            target_proxy.ssl_policy = ResourceInvalidator.get_by_logic(get_ssl_policy, False)

    @staticmethod
    def _assign_target_proxy(global_forwarding_rule: GcpComputeGlobalForwardingRule, targets: AliasesDict[GcpComputeTargetProxy]):
        def get_target():
            target = ResourceInvalidator.get_by_id(targets, global_forwarding_rule.target_identifier, False)
            if not target:
                target = next((target for target in targets if
                               global_forwarding_rule.project_id == target.project_id and
                               global_forwarding_rule.target_identifier == target.name), None)
            return target

        global_forwarding_rule.target = ResourceInvalidator.get_by_logic(get_target, True, global_forwarding_rule, "Could not associate target proxy")

    @staticmethod
    def _assign_subnetwork(network: GcpComputeNetwork, subnetworks: AliasesDict[GcpComputeSubNetwork]):
        def get_subnetworks():
            subnetworks_list: List[GcpComputeSubNetwork] = []
            for subnetwork in subnetworks:
                if subnetwork.network_identifier in [network.self_link, network.name, network.network_id]:
                    subnetworks_list.append(subnetwork)
            return subnetworks_list

        network.subnetworks = ResourceInvalidator.get_by_logic(get_subnetworks, False)
