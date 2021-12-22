from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set_extension import AzureVirtualMachineScaleSetExtension


class VmssExtensionBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'vmss-extensions.json'

    def do_build(self, attributes: dict) -> AzureVirtualMachineScaleSetExtension:
        properties = attributes['properties']
        virtual_machine_scale_set_id = attributes['id'].split('extensions')[0][:-1]

        return AzureVirtualMachineScaleSetExtension(name=attributes['name'],
                                                    publisher=properties['publisher'],
                                                    extension_type=properties['type'],
                                                    type_handler_version=properties['typeHandlerVersion'],
                                                    virtual_machine_scale_set_id=virtual_machine_scale_set_id)
