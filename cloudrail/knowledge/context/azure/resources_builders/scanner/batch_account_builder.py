from cloudrail.knowledge.context.azure.resources.batch_management.azure_batch_account import AzureBatchAccount, BatchAccountPoolAllocationMode, BatchAccountKeyVaultReference
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class BatchAccountBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-batch-accounts.json'

    def do_build(self, attributes: dict) -> AzureBatchAccount:
        key_vault_reference = None
        if key_vault_ref_data := attributes.get('keyVaultReference'):
            key_vault_reference=BatchAccountKeyVaultReference(name=attributes['name'],
                                                              id=key_vault_ref_data['id'],
                                                              url=key_vault_ref_data['url'])
        return AzureBatchAccount(name=attributes['name'],
                                 pool_allocation_mode=BatchAccountPoolAllocationMode(attributes['poolAllocationMode']),
                                 public_network_access_enabled=attributes['publicNetworkAccess'] == 'enabled',
                                 key_vault_reference=key_vault_reference,
                                 storage_account_id=attributes.get('autoStorage', {}).get('storageAccountId'))
