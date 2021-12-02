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
        for global_forwarding_rule in env_context.compute_global_forwarding_rule:
            if global_forwarding_rule.target.is_encrypted:
                if global_forwarding_rule.target.ssl_policy:
                    if global_forwarding_rule.target.ssl_policy.min_tls_version == "TLS_1_2":
                        if global_forwarding_rule.target.ssl_policy.profile in ["MODERN", "RESTRICTED"] or \
                                (global_forwarding_rule.target.ssl_policy.profile == "CUSTOM" and global_forwarding_rule.target.ssl_policy.is_using_secure_ciphers):
                            evidence_string = ""
                        else:
                            evidence_string = f"The {global_forwarding_rule.get_type()} '{global_forwarding_rule.get_friendly_name()}' is using weak ciphers in target " \
                                              f"{global_forwarding_rule.target.target_type} proxy {global_forwarding_rule.target.get_friendly_name()} with a misconfigured SSL policy " \
                                              f"{global_forwarding_rule.target.ssl_policy.get_friendly_name()}"
                    else:
                        evidence_string = f"The {global_forwarding_rule.get_type()} '{global_forwarding_rule.get_friendly_name()}' is using TLS version less that 1.2 in target " \
                                          f"{global_forwarding_rule.target.target_type} proxy {global_forwarding_rule.target.get_friendly_name()} " \
                                          f"with a misconfigured SSL policy {global_forwarding_rule.target.ssl_policy.get_friendly_name()}"
                    if evidence_string:
                        issues.append(
                            Issue(
                                evidence_string,
                                global_forwarding_rule,
                                global_forwarding_rule.target.ssl_policy))
                else:
                    issues.append(
                        Issue(
                            f"The {global_forwarding_rule.get_type()} '{global_forwarding_rule.get_friendly_name()}' is missing SSL policy",
                            global_forwarding_rule,
                            global_forwarding_rule))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.compute_global_forwarding_rule)
