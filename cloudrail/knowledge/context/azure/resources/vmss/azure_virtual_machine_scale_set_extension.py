from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureVirtualMachineScaleSetExtension(AzureResource):
    """
        Attributes:
            name: The name for the Virtual Machine Scale Set Extension
            publisher: Specifies the Publisher of the Extension
            extension_type: Specifies the type of the Extension
            type_handler_version: Specifies the version of the extension to use
            virtual_machine_scale_set_id: The ID of the Virtual Machine Scale Set
    """

    def __init__(self,
                 name: str,
                 publisher: str,
                 extension_type: str,
                 type_handler_version: str,
                 virtual_machine_scale_set_id: str):
        super().__init__(AzureResourceType.AZURERM_VIRTUAL_MACHINE_SCALE_SET_EXTENSION)
        self.name: str = name
        self.publisher: str = publisher
        self.extension_type: str = extension_type
        self.type_handler_version: str = type_handler_version
        self.virtual_machine_scale_set_id: str = virtual_machine_scale_set_id
        self.with_aliases(self.virtual_machine_scale_set_id)

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Compute/virtualMachineScaleSets/{self.virtual_machine_scale_set_id}/extensions'

    @property
    def is_tagable(self) -> bool:
        return False

    @staticmethod
    def is_standalone() -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self._id]

    def get_type(self, is_plural: bool = False) -> str:
        return 'Virtual Machine Scale Set ' + ('Extension' if not is_plural else 'Extensions')

    def get_name(self) -> str:
        return self.name

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags,
                'type_handler_version': self.type_handler_version}
