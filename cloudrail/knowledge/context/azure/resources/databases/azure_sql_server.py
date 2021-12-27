from typing import Optional, List
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import \
    AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_extended_auditing_policy import \
    AzureSqlServerExtendedAuditingPolicy
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_security_alert_policy import AzureMsSqlServerSecurityAlertPolicy


class MsSqlServerVersion(str, Enum):
    VERSION_2_0 = '2.0'
    VERSION_12_0 = '12.0'


class MsSqlServerConnectionPolicy(str, Enum):
    DEFAULT = 'Default'
    PROXY = 'Proxy'
    REDIRECT = 'Redirect'


class MsSqlServerIdentityTypes(str, Enum):
    SYSTEM_ASSIGNED = 'SystemAssigned'
    USER_ASSIGNED = 'UserAssigned'


class MsSqlServerMinimumTLSVersion(str, Enum):
    VERSION_1_0 = '1.0'
    VERSION_1_1 = '1.1'
    VERSION_1_2 = '1.2'


@dataclass
class MsSqlServerAzureAdAdministrator:
    """
        Attributes:
            login_username: The login username of the Azure AD Administrator of this SQL Server.
            object_id: The object id of the Azure AD Administrator of this SQL Server.
            tenant_id: The tenant id of the Azure AD Administrator of this SQL Server.
            azuread_authentication_only: Specifies whether only AD Users and administrators can be used to login or also local database users.
    """
    login_username: str
    object_id: str
    tenant_id: str
    azuread_authentication_only: bool


@dataclass
class MsSqlServerIdentity:
    """
        Attributes:
            type: Specifies the identity type of the Microsoft SQL Server.
            user_assigned_identity_ids: Specifies a list of User Assigned Identity IDs to be assigned.
    """
    type: MsSqlServerIdentityTypes
    user_assigned_identity_ids: Optional[List[str]]


@dataclass
class MsSqlServerTransparentDataEncryption:
    """
        Attributes:
            server_id: Specifies the name of the MS SQL Server.
            key_vault_key_id: To use customer managed keys from Azure Key Vault, provide the AKV Key ID. To use service managed keys, omit this field.
    """
    server_id: str
    key_vault_key_id: Optional[str]


class AzureSqlServer(AzureResource):
    """
        Attributes:
            server_name: The name of the SQL server
            azuread_administrator_list: A list (only 1 element supported) of AD Administrator for this server.
            connection_policy: The connection policy the server will use.
            identity_list: A list of identities (only 1 element supported) to be used by this server.
            minimum_tls_version: The Minimum TLS Version for all SQL Database and SQL Data Warehouse databases associated with the server.
            public_network_access_enabled: Whether public network access is allowed for this server.
            primary_user_assigned_identity_id: Specifies the primary user managed identity id.
            public_network_access_enabled: An indication on if public network access is enabled.
    """

    def __init__(self,
                 server_name: str,
                 version: MsSqlServerVersion,
                 administrator_login: str,
                 azuread_administrator_list: Optional[List[MsSqlServerAzureAdAdministrator]],
                 connection_policy: MsSqlServerConnectionPolicy,
                 identity_list: List[MsSqlServerIdentity],
                 minimum_tls_version: Optional[MsSqlServerMinimumTLSVersion],
                 primary_user_assigned_identity_id: Optional[str],
                 public_network_access_enabled: bool) -> None:
        super().__init__(AzureResourceType.AZURERM_SQL_SERVER)
        self.server_name: str = server_name
        self.with_aliases(server_name)
        self.version: MsSqlServerVersion = version
        self.administrator_login: str = administrator_login
        self.azuread_administrator_list: Optional[List[MsSqlServerAzureAdAdministrator]
                                                  ] = azuread_administrator_list
        self.connection_policy: MsSqlServerConnectionPolicy = connection_policy
        self.minimum_tls_version: Optional[MsSqlServerMinimumTLSVersion] = minimum_tls_version
        self.public_network_access_enabled: bool = public_network_access_enabled
        self.identity_list: MsSqlServerIdentity = identity_list
        self.primary_user_assigned_identity_id: Optional[str] = primary_user_assigned_identity_id
        self.security_alert_policy_list: Optional[List[AzureMsSqlServerSecurityAlertPolicy]] = []
        self.transparent_data_encryption: Optional[MsSqlServerTransparentDataEncryption] = None
        self.public_network_access_enabled: bool = public_network_access_enabled
        self.extended_auditing_policy: AzureSqlServerExtendedAuditingPolicy = None

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.server_name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self._id}/overview'

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'server_name': self.server_name,
                'public_network_access_enabled': self.public_network_access_enabled}
