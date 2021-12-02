from typing import Optional
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_subnetwork import GcpComputeSubNetwork, GcpComputeSubNetworkLogConfig
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeSubNetworkBuilder(BaseGcpTerraformBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-subnetworks-list.json'

    def do_build(self, attributes: dict) -> GcpComputeSubNetwork:
        name = attributes["name"]
        subnetwork_id = attributes["id"]
        self_link = attributes["selfLink"]
        region = attributes["region"] # TODO: filter region
        network_identifier = attributes["network"]
        ip_cidr_range = attributes["ipCidrRange"]
        log_config = self.build_log_config_block(attributes)

        return GcpComputeSubNetwork(name, subnetwork_id, self_link, region, network_identifier, ip_cidr_range, log_config)

    def build_log_config_block(self, attribute: dict) -> Optional[GcpComputeSubNetworkLogConfig]:
        log_config_block = attribute.get("logConfig")

        if log_config_block:
            aggregation_interval = self._get_known_value(log_config_block, "aggregationInterval")
            flow_sampling = self._get_known_value(log_config_block, "flowSampling")
            metadata = self._get_known_value(log_config_block, "metadata")
            metadata_fields = self._get_known_value(log_config_block, "metadataFields")
            filter_expr = self._get_known_value(log_config_block, "filterExpr")

            return GcpComputeSubNetworkLogConfig(aggregation_interval, flow_sampling, metadata, metadata_fields, filter_expr)

        return None

