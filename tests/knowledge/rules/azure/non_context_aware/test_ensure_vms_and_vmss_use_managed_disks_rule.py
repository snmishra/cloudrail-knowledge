from unittest import TestCase
from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.vm.azure_virtual_machine import AzureVirtualMachine, DataDisk, DiskSettings, OsDisk
from cloudrail.knowledge.context.azure.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_vms_and_vmss_use_managed_disks_rule import EnsureVmAndVmssUseManagedDisksRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureVmAndVmssUseManagedDisksRule(TestCase):

    def setUp(self):
        self.rule = EnsureVmAndVmssUseManagedDisksRule()

    @parameterized.expand(
        [
            ["virtual_machine_unmanaged_disk", False, 1, True, 'virtual_machine'],
            ["virtual_machine_2_types_of_unmanaged_disk", False, 2, True, 'virtual_machine'],
            ["virtual_machine_managed_disk", True, 1, False, 'virtual_machine'],
            ["vmss_unmanaged_disk", False, 1, True, 'vmss'],
            ["vmss_2_types_of_unmanaged_disk", False, 2, True, 'vmss'],
            ["vmss_managed_disk", True, 1, False, 'vmss']
        ]
    )
    def test_auth_states(self, unused_name: str, unmanaged_disk: bool, types_num: int, should_alert: bool, resource_type: str):
        # Arrange
        virtual_machine: AzureVirtualMachine = create_empty_entity(AzureVirtualMachine)
        virtual_machines_scales_set: AzureVirtualMachineScaleSet = create_empty_entity(AzureVirtualMachineScaleSet)
        disk_settings: DiskSettings = create_empty_entity(DiskSettings)
        os_disk: OsDisk = create_empty_entity(OsDisk)
        data_disk: DataDisk = create_empty_entity(DataDisk)
        data_disk.is_managed_disk = unmanaged_disk
        disk_settings.data_disks = [data_disk]
        if types_num == 2:
            os_disk.is_managed_disk = unmanaged_disk
        else:
            os_disk.is_managed_disk = True
        disk_settings.os_disk = os_disk
        virtual_machine.disk_settings = disk_settings
        virtual_machines_scales_set.disk_settings = disk_settings
        if resource_type == 'virtual_machine':
            context = AzureEnvironmentContext(virtual_machines=AliasesDict(virtual_machine))
        else:
            context = AzureEnvironmentContext(virtual_machines_scale_sets=AliasesDict(virtual_machines_scales_set))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        elif should_alert and types_num == 2:
            self.assertTrue("for both it's os_disk and one of it's managed disks" in result.issues[0].evidence)
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
