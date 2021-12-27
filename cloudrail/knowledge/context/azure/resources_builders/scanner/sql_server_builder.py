from typing import List
from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import AzureSqlServer, MsSqlServerVersion, MsSqlServerAzureAdAdministrator, \
    MsSqlServerIdentity, MsSqlServerIdentityTypes
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class SqlServerBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'sql-servers-list.json'

    def do_build(self, attributes: dict) -> AzureSqlServer:
        properties = attributes['properties']
        ## Azure admin list
        azuread_administrator_list: List[MsSqlServerAzureAdAdministrator] = []
        for azure_admin in attributes.get('administrators', []):
            azuread_administrator_list.append(MsSqlServerAzureAdAdministrator(login_username=azure_admin['login'],
                                                                              object_id=azure_admin['sid'],
                                                                              tenant_id=azure_admin['tenantId'],
                                                                              azuread_authentication_only=azure_admin['azureADOnlyAuthentication']))
        ## Managed Identities
        identity_list: List[MsSqlServerIdentity] = []
        for identity in attributes.get('identity', []):
            identity_list.append(MsSqlServerIdentity(type=enum_implementation(MsSqlServerIdentityTypes, identity['type']),
                                                    user_assigned_identity_ids=[user[0] for user in identity.get('userAssignedIdentities', [])]))
        return AzureSqlServer(server_name=attributes['name'],
                              version=enum_implementation(MsSqlServerVersion, properties['version']),
                              administrator_login=properties['administratorLogin'],
                              azuread_administrator_list=azuread_administrator_list,
                              connection_policy=
                              public_network_access_enabled=properties['publicNetworkAccess'] == 'Enabled')
