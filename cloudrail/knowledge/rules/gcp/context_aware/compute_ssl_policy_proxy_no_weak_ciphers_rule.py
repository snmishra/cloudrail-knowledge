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
        not_secure_ciphers = ["TLS_RSA_WITH_AES_128_GCM_SHA256", "TLS_RSA_WITH_AES_256_GCM_SHA384", "TLS_RSA_WITH_AES_128_CBC_SHA", "TLS_RSA_WITH_AES_256_CBC_SHA", "TLS_RSA_WITH_3DES_EDE_CBC_SHA"]
        for global_forwarding_rule in env_context.compute_global_forwarding_rule:
            if global_forwarding_rule.target.is_encrypted:
                target_proxy = global_forwarding_rule.target
                if target_proxy.ssl_policy:
                    if target_proxy.ssl_policy.min_tls_version == "TLS_1_2":
                        if target_proxy.ssl_policy.profile == "MODERN" or target_proxy.ssl_policy.profile == "RESTRICTED" or \
                            (target_proxy.ssl_policy.profile == "CUSTOM" and
                             all(custom_feature not in not_secure_ciphers for custom_feature in target_proxy.ssl_policy.custom_features)):
                            evidence_string = ""
                        else:
                            evidence_string = f"The {global_forwarding_rule.get_type()} '{global_forwarding_rule.get_friendly_name()}' is using TLS version less that 1.2 in target " \
                                              f"{target_proxy.target_type} proxy {target_proxy.get_friendly_name()} with a misconfigured SSL policy {target_proxy.ssl_policy.get_friendly_name()}"
                    else:
                        evidence_string = f"The {global_forwarding_rule.get_type()} is using weak ciphers in target {target_proxy.target_type} " \
                                          f"proxy {target_proxy.get_friendly_name()} with a misconfigured SSL policy {target_proxy.ssl_policy.get_friendly_name()}"
                    if evidence_string:
                        issues.append(
                            Issue(
                                evidence_string,
                                global_forwarding_rule,
                                target_proxy.ssl_policy))
                else:
                    issues.append(
                        Issue(
                            f"The {global_forwarding_rule.get_type()} '{global_forwarding_rule.get_friendly_name()}' is missing SSL policy",
                            global_forwarding_rule,
                            global_forwarding_rule))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.compute_global_forwarding_rule)
