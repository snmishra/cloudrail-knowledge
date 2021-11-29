from typing import List

from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, IterFunctionData
from cloudrail.knowledge.context.gcp.pseudo_builder import PseudoBuilder
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_global_forwarding_rule import GcpComputeGlobalForwardingRule
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_ssl_policy import GcpComputeSslPolicy
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_proxy import GcpComputeTargetProxy
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_ssl_proxy import GcpComputeTargetSslProxy
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpRelationsAssigner(DependencyInvocation):

    def __init__(self, ctx: GcpEnvironmentContext = None):
        self.pseudo_builder = PseudoBuilder(ctx)
        self.pseudo_builder.create_default_firewalls()

        function_pool = [
            IterFunctionData(self._assign_ssl_policy, ctx.compute_target_ssl_proxy, (ctx.compute_ssl_policy,)),
            IterFunctionData(self._assign_ssl_policy, ctx.compute_target_https_proxy, (ctx.compute_ssl_policy,)),
            IterFunctionData(self._assign_target_proxy, ctx.compute_global_forwarding_rule, (ctx.compute_target_http_proxy,)),
            IterFunctionData(self._assign_target_proxy, ctx.compute_global_forwarding_rule, (ctx.compute_target_ssl_proxy,)),
            IterFunctionData(self._assign_target_proxy, ctx.compute_global_forwarding_rule, (ctx.compute_target_https_proxy,)),
        ]

        super().__init__(function_pool, context=ctx)

    @staticmethod
    def _assign_ssl_policy(target_ssl_proxy: GcpComputeTargetSslProxy, ssl_policies: List[GcpComputeSslPolicy]):
        def get_ssl_policy():
            ssl_policy = next((ssl_policy for ssl_policy in ssl_policies if
                               target_ssl_proxy.ssl_policy and
                              (target_ssl_proxy.ssl_policy in [ssl_policy.get_name(), ssl_policy.get_id()], ssl_policy.self_link) and
                              target_ssl_proxy.project_id == ssl_policy.project_id), None)
            return ssl_policy

        if not target_ssl_proxy.ssl_policy_obj:
            target_ssl_proxy.ssl_policy_obj = ResourceInvalidator.get_by_logic(get_ssl_policy, False)

    @staticmethod
    def _assign_target_proxy(global_forwarding_rule: GcpComputeGlobalForwardingRule, targets: List[GcpComputeTargetProxy]):
        def get_target():
            target = next((target for target in targets if
                           global_forwarding_rule.target and
                           (global_forwarding_rule.target in [target.get_name(), target.get_id(), target.self_link]) and
                           global_forwarding_rule.project_id == target.project_id), None)
            return target

        if not global_forwarding_rule.target_obj:
            global_forwarding_rule.target_obj = ResourceInvalidator.get_by_logic(get_target, False)
