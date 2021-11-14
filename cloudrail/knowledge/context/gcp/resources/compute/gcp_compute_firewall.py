from typing import List, Optional
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource

class GcpComputeFirewallLogCfgMetaData(Enum):
    EXCLUDE_ALL_METADATA  = 'exclude_all_metadata'
    INCLUDE_ALL_METADATA = 'include_all_metadata'

class GcpComputeFirewallDirection(Enum):
    INGRESS  = 'ingress'
    EGRESS = 'egress'

@dataclass
class GcpComputeFirewallAllow:
    """
        Attributes:
	       protocol: (Required) The IP protocol to which this rule applies.
	       ports: (Optional) An optional list of ports to which this rule applies. This field is only applicable for UDP or TCP protocol.
    """
    protocol: str
    ports: Optional[List[int]]

@dataclass
class GcpComputeFirewallDeny:
    """
        Attributes:
	        protocol: (Required) The IP protocol to which this rule applies.
	        ports: (Optional) An optional list of ports to which this rule applies. This field is only applicable for UDP or TCP protocol.
    """
    protocol: str
    ports: Optional[List[int]]

class GcpComputeFirewall(GcpResource):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            network: (Required) The VPC network name or self_link of the network to attach this firewall to a compute resource.
            allow: (Optional) The list of ALLOW rules specified by this firewall.
            deny: (Optional) The list of DENY rules specified by this firewall.
            destination_ranges: (Optional) If destination ranges are specified, the firewall will apply only to traffic that has destination IP address in these ranges.
            direction: (Optional) Direction of traffic to which this firewall applies; default is INGRESS. Possible values are INGRESS and EGRESS.
            source_ranges: (Optional) If source ranges are specified, the firewall will apply only to traffic that has source IP address in these ranges.
    """

    def __init__(self,
                 name: str,
                 network: str,
                 allow: Optional[List[GcpComputeFirewallAllow]],
                 deny: Optional[List[GcpComputeFirewallDeny]],
		         destination_ranges: Optional[List[str]],
		         direction: Optional[GcpComputeFirewallDirection],
		         source_ranges: Optional[List[str]]):

        super().__init__(GcpResourceType.GOOGLE_COMPUTE_FIREWALL)
        self.name: str = name
        self.network: str = network
        self.allow: Optional[List[GcpComputeFirewallAllow]] = allow
        self.deny: Optional[List[GcpComputeFirewallDeny]] = deny
        self.destination_ranges: Optional[List[str]] = destination_ranges
        self.direction: Optional[GcpComputeFirewallDirection] = direction
        self.source_ranges: Optional[List[str]] = source_ranges

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    @property
    def is_tagable(self) -> bool:
        return False

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/networking/firewalls/details/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Compute Firewall Details'
        else:
            return 'Compute Firewall Details'

    def to_drift_detection_object(self) -> dict:
        return {'destination_ranges': self.destination_ranges,
                'source_ranges': self.source_ranges}
