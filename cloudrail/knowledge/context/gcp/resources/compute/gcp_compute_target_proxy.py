# pylint: disable=W0107
from abc import abstractmethod
from typing import List, Optional

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeTargetProxy(GcpResource):
    """
        A parent resource for all target proxy resources

        Attributes:
            name: (Required) A unique name of the resource.
    """

    def __init__(self,
                 name: str,
                 self_link: str,
                 resource_type: GcpResourceType):

        super().__init__(resource_type)
        self.name: str = name
        self.self_link: str = self_link

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    def get_name(self) -> str:
        return self.name

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return False


    @property
    @abstractmethod
    def is_encrypted(self) -> bool:
        pass

    @abstractmethod
    def get_cloud_resource_url(self) -> Optional[str]:
        """
            True if the target protocol is secure (e.g ssl, https)
        """
        pass

    @abstractmethod
    def get_type(self, is_plural: bool = False) -> str:
        pass
