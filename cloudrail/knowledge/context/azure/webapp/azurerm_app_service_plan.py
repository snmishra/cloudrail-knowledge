from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureAppServicePlan(AzureResource):
    """
        Attributes:
            name: Specifies the name of the App Service Plan component.
            kind: The kind of the App Service Plan to create.
    """

    def __init__(self, name: str, kind: str):
        super().__init__(AzureResourceType.AZURERM_APP_SERVICE_PLAN)
        self.name: str = name
        self.kind: str = kind

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_kind(self) -> str:
        return self.kind

    @property
    def is_tagable(self) -> bool:
        return True
