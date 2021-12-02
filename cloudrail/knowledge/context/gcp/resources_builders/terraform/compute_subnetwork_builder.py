from typing import Optional
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_subnetwork import GcpComputeSubNetwork, GcpComputeSubNetworkLogConfig
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class ComputeSubNetworkBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeSubNetwork:
        name = attributes["name"]
        subnetwork_id = attributes["id"]
        self_link = attributes["self_link"]
        region = attributes["region"]
        network_identifier = attributes["network"]
        ip_cidr_range = attributes["ip_cidr_range"]
        log_config = self.build_log_config_block(attributes)

        return GcpComputeSubNetwork(name, subnetwork_id, self_link, region, network_identifier, ip_cidr_range, log_config)

    def build_log_config_block(self, attribute: dict) -> Optional[GcpComputeSubNetworkLogConfig]:
        log_config_block = attribute.get("log_config")

        if log_config_block:
            aggregation_interval = self._get_known_value(log_config_block, "aggregation_interval")
            flow_sampling = self._get_known_value(log_config_block, "flow_sampling")
            metadata = self._get_known_value(log_config_block, "metadata")
            metadata_fields = self._get_known_value(log_config_block, "metadata_fields")
            filter_expr = self._get_known_value(log_config_block, "filter_expr")

            return GcpComputeSubNetworkLogConfig(aggregation_interval, flow_sampling, metadata, metadata_fields, filter_expr)

        return None

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_SUBNETWORK
