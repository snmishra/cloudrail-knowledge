from typing import Dict

from cloudrail.knowledge.context.aws.resources.ec2.nat_gateways import NatGateways
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationNatGatewayBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.NAT_GW, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> NatGateways:
        properties: dict = cfn_res_attr['Properties']
        allocation_id = self.get_property(properties, 'AllocationId')
        subnet_id = self.get_property(properties, 'SubnetId')
        return NatGateways(nat_gateway_id=self.create_random_pseudo_identifier(), allocation_id=allocation_id,
                           subnet_id=subnet_id, eni_id=None,
                           private_ip=None, public_ip=None,
                           account=cfn_res_attr['account_id'], region=cfn_res_attr['region'])
