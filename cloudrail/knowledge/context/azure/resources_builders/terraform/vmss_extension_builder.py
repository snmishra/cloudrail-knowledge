from typing import Optional
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set_extension import AzureVirtualMachineScaleSetExtension

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class VmssBasicExtensionBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureVirtualMachineScaleSetExtension:
        return _build_vmss_extension(attributes)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_VIRTUAL_MACHINE_SCALE_SET_EXTENSION


class VmssNestedExtensionBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> Optional[AzureVirtualMachineScaleSetExtension]:
        if extension_attributes := self._get_known_value(attributes, 'extension'):
            extension_attributes[0]['virtual_machine_scale_set_id'] = attributes['id']
            return _build_vmss_extension(extension_attributes[0])
        return None

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_VIRTUAL_MACHINE_SCALE_SET

def _build_vmss_extension(attributes: dict) -> AzureVirtualMachineScaleSetExtension:
    return AzureVirtualMachineScaleSetExtension(name=attributes['name'],
                                                publisher=attributes['publisher'],
                                                extension_type=attributes['type'],
                                                type_handler_version=attributes['type_handler_version'],
                                                virtual_machine_scale_set_id=attributes['virtual_machine_scale_set_id'])
