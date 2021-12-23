from unittest import TestCase
from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine_extension import AzureVirtualMachineExtension
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet, OperatingSystemType
from cloudrail.knowledge.rules.azure.context_aware.vmss_diagnostics_logs_enabled_rule import VmssDiagnosticsLogsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestVmssDiagnosticsLogsEnabledRule(TestCase):

    def setUp(self):
        self.rule = VmssDiagnosticsLogsEnabledRule()

    @parameterized.expand(
        [
            ["no_logs_enabled", False, True],
            ["logs_enabled", True, False],
        ]
    )
    def test_vmss_diagnostics_logs(self, unused_name: str, extnesion_configured: bool, should_alert: bool):
        # Arrange
        virtual_machines_scales_set: AzureVirtualMachineScaleSet = create_empty_entity(AzureVirtualMachineScaleSet)
        virtual_machines_scales_set.name = 'vmss-test'
        virtual_machines_scales_set.os_type = OperatingSystemType.WINDOWS
        vmss_extension: AzureVirtualMachineExtension = create_empty_entity(AzureVirtualMachineExtension)
        if extnesion_configured:
            vmss_extension.publisher = 'Microsoft.Azure.Diagnostics'
            vmss_extension.extension_type = 'IaaSDiagnostics'
            virtual_machines_scales_set.extensions.append(vmss_extension)
        context = AzureEnvironmentContext(virtual_machines_scale_sets=AliasesDict(virtual_machines_scales_set),
                                          vms_extentions=AliasesDict(vmss_extension))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
