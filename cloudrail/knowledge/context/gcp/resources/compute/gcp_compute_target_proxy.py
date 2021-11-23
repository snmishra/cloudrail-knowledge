from abc import abstractmethod
from typing import List, Optional

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeTargetProxy(GcpResource):
    """
        Attributes:
            name: (Required) A unique name of the resource.
    """

    def __init__(self,
                 name: str,
                 resource_type: GcpResourceType):

        super().__init__(resource_type)
        self.name: str = name

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    def get_name(self) -> str:
        return self.name

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return False

    @abstractmethod
    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_type(self, is_plural: bool = False) -> str:
        pass


