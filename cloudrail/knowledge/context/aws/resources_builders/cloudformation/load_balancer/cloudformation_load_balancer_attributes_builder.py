from typing import Dict
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_attributes import LoadBalancerAttributes, LoadBalancerAccessLogs
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLoadBalancerBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ELASTIC_LOAD_BALANCER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> LoadBalancerAttributes:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        load_balancer_arn = self.get_resource_id(cfn_res_attr)
        attributes_dict = {}
        for attribute in attributes['Value']['Attributes']:
            if attribute['Value'] == 'true':
                attributes_dict.update({attribute['Key']: True})
            elif attribute['Value'] == 'false':
                attributes_dict.update({attribute['Key']: False})
            else:
                attributes_dict.update({attribute['Key']: attribute['Value']})
        lb_access_logs = LoadBalancerAccessLogs(attributes_dict['access_logs.s3.bucket'],
                                                attributes_dict['access_logs.s3.prefix'],
                                                attributes_dict['access_logs.s3.enabled'])
        return LoadBalancerAttributes(account=account, region=region, load_balancer_arn=load_balancer_arn, )