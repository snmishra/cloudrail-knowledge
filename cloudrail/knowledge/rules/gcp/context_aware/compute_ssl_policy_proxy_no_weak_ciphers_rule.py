from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class ComputeSslPolicyProxyNoWeakCiphersRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'car_proxy_lb_ssl_policy_no_weak_ciphers'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for global_forwarding in env_context.compute_global_forwarding_rule:
            if target_https_proxy := self.get_target_https_proxy_by_name(env_context, global_forwarding.target):
                for compute_ssl_policy in env_context.compute_ssl_policy:
                    if compute_ssl_policy.min_tls_version:
                        issues.append(
                            Issue(
                                f"The {compute_instance.get_type()} `{compute_instance.get_friendly_name()}` has IP forwarding feature enabled.",
                                compute_instance,
                                compute_instance))
        return issues

    def get_target_https_proxy_by_name(self, env_context: GcpEnvironmentContext, name: str):
        return next((target_https_proxy for target_https_proxy in env_context.compute_target_https_proxy if
                     target_https_proxy.name == name), None)

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.compute_instances)
