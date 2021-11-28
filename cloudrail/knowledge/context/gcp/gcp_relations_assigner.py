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
            IterFunctionData(self._assign_target_proxy, ctx.compute_global_forwarding_rule, (ctx.compute_target_http_proxy,)),
            IterFunctionData(self._assign_target_proxy, ctx.compute_global_forwarding_rule, (ctx.compute_target_ssl_proxy,)),
        ]

        super().__init__(function_pool, context=ctx)

    def _assign_ssl_policy(self, target_ssl_proxy: GcpComputeTargetSslProxy, ssl_policies: List[GcpComputeSslPolicy]):
        def get_ssl_policy():
            ssl_policy = self._get_resource_by_keys_and_project_id(ssl_policies, target_ssl_proxy.ssl_policy, target_ssl_proxy.project_id)
            return ssl_policy

        target_ssl_proxy.ssl_policy_obj = ResourceInvalidator.get_by_logic(get_ssl_policy, False)

    def _assign_target_proxy(self, global_forwarding_rule: GcpComputeGlobalForwardingRule, targets: List[GcpComputeTargetProxy]):
        def get_target():
            target = self._get_resource_by_keys_and_project_id(targets, global_forwarding_rule.target, global_forwarding_rule.project_id)
            return target

        global_forwarding_rule.target_obj = ResourceInvalidator.get_by_logic(get_target, False)

    @staticmethod
    def _get_resource_by_keys_and_project_id(resources: List[GcpResource], key: str, project_id: str):
        return next((resource for resource in resources if
                    (key in resource.get_keys()) and
                    project_id == resource.project_id), None)
