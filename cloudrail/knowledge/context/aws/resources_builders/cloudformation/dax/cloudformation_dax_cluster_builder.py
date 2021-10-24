from typing import Dict

from cloudrail.knowledge.context.aws.resources.dax.dax_cluster import DaxCluster
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationDaxClusterBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.DAX_CLUSTER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> DaxCluster:
        properties: dict = cfn_res_attr['Properties']
        server_side_encryption = properties.get("SSESpecification", {}).get("SSEEnabled", False)
        return DaxCluster(properties["ClusterName"],
                          server_side_encryption,
                          self.create_random_pseudo_identifier(),
                          cfn_res_attr['region'],
                          cfn_res_attr['account_id'])




