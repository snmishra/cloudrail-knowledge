from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class ContainerClusterEnsureNoPublicIptRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_gke_control_plane_ensure_not_public'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for container_cluster in env_context.container_cluster:
            should_alert = True
            if container_cluster.master_authorized_networks_config:
                for cidr_obj in container_cluster.master_authorized_networks_config.cidr_blocks:
                    if cidr_obj.cidr_block:
                        should_alert = False
            if should_alert:
                issues.append(
                    Issue(
                        f"The {container_cluster.get_type()} `{container_cluster.get_friendly_name()}` control plane is publicly accessible",
                        container_cluster,
                        container_cluster))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.container_cluster)
