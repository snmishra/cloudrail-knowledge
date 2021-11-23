from typing import Optional

from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_proxy import GcpComputeTargetProxy
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType


class GcpComputeTargetHttpProxy(GcpComputeTargetProxy):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            url_map: A reference to the UrlMap resource that defines the mapping from URL to the BackendService.
    """

    def __init__(self,
                 name: str,
                 url_map: str):

        super().__init__(name, GcpResourceType.GOOGLE_COMPUTE_TARGET_HTTP_PROXY)
        self.url_map: str = url_map

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/net-services/loadbalancing/advanced/targetHttpProxies/details/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        return 'Compute Target Http Proxy Details'

    def to_drift_detection_object(self) -> dict:
        return {'url_map': self.url_map}
