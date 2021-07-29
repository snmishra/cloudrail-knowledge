from typing import List, Optional

# TODO: move ConnectionInstance to common folder
from cloudrail.knowledge.context.aws.aws_connection import ConnectionInstance
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.network.azure_nic import AzureNetworkInterfaceController


class AzureVirtualMachine(AzureResource, ConnectionInstance):
    """
        Attributes:
            name: The name of this Public IP.
            network_interface_ids: A list of Network Interface ID's which are associated with the Virtual Machine.
            network_interfaces: A list of Network Interface which are associated with the Virtual Machine.
    """
    def __init__(self, name: str, network_interface_ids: List[str]):
        super().__init__(AzureResourceType.AZURERM_VIRTUAL_MACHINE)
        self.name: str = name
        self.network_interface_ids: List[str] = network_interface_ids
        self.network_interfaces: List[AzureNetworkInterfaceController] = []

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
