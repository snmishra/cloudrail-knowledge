from abc import abstractmethod
from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.security.azure_security_center_subscription_pricing import SubscriptionPricingResourceType, \
    SubscriptionPricingTier
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class BaseDefenderEnabledRule(AzureBaseRule):

    @abstractmethod
    def _get_resource_type(self) -> SubscriptionPricingResourceType:
        pass

    @abstractmethod
    def _get_evidence(self, subscription_id) -> str:
        pass

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for subscription_pricing in env_context.security_center_subscription_pricings:
            if subscription_pricing.resource_type == self._get_resource_type() and \
                    subscription_pricing.tier != SubscriptionPricingTier.STANDARD:
                issues.append(
                    Issue(
                        self._get_evidence(subscription_pricing.subscription_id),
                        subscription_pricing,
                        subscription_pricing))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.security_center_subscription_pricings)


class ContainerRegistriesDefenderEnabledRule(BaseDefenderEnabledRule):
    def get_id(self) -> str:
        return 'non_car_azure_defender_for_container_registries_enabled'

    @abstractmethod
    def _get_resource_type(self) -> SubscriptionPricingResourceType:
        return SubscriptionPricingResourceType.CONTAINER_REGISTRY

    @abstractmethod
    def _get_evidence(self, subscription_id) -> str:
        return f'Azure Defender is not enabled for container registries in the subscription `{subscription_id}`.'


class SqlServersDefenderEnabledRule(BaseDefenderEnabledRule):
    def get_id(self) -> str:
        return 'non_car_azure_defender_for_azure_sql_servers_enabled'

    @abstractmethod
    def _get_resource_type(self) -> SubscriptionPricingResourceType:
        return SubscriptionPricingResourceType.SQL_SERVERS

    @abstractmethod
    def _get_evidence(self, subscription_id) -> str:
        return f"Azure Defender is not enabled for Azure SQL Database servers in the subscription `{subscription_id}`."


class SqlServersOnVirtualMachinesDefenderEnabledRule(BaseDefenderEnabledRule):
    def get_id(self) -> str:
        return 'non_car_azure_defender_for_sql_servers_on_machines_enabled'

    @abstractmethod
    def _get_resource_type(self) -> SubscriptionPricingResourceType:
        return SubscriptionPricingResourceType.SQL_SERVER_VIRTUAL_MACHINES

    @abstractmethod
    def _get_evidence(self, subscription_id) -> str:
        return f'Azure Defender is not enabled for SQL Servers on Virtual Machines in the subscription `{subscription_id}`.'


class KubernetesDefenderEnabledRule(BaseDefenderEnabledRule):
    def get_id(self) -> str:
        return 'non_car_azure_defender_for_kubernetes_enabled'

    @abstractmethod
    def _get_resource_type(self) -> SubscriptionPricingResourceType:
        return SubscriptionPricingResourceType.KUBERNETES_SERVICE

    @abstractmethod
    def _get_evidence(self, subscription_id) -> str:
        return f"Azure Defender is not enabled for Kubernetes in the subscription `{subscription_id}`."


class KeyVaultsDefenderEnabledRule(BaseDefenderEnabledRule):
    def get_id(self) -> str:
        return 'non_car_azure_defender_for_key_vault_enabled'

    @abstractmethod
    def _get_resource_type(self) -> SubscriptionPricingResourceType:
        return SubscriptionPricingResourceType.KEY_VAULTS

    @abstractmethod
    def _get_evidence(self, subscription_id) -> str:
        return f"Azure Defender is not enabled for Key Vault in the subscription `{subscription_id}`."


class StorageDefenderEnabledRule(BaseDefenderEnabledRule):
    def get_id(self) -> str:
        return 'non_car_azure_defender_for_storage_enabled'

    @abstractmethod
    def _get_resource_type(self) -> SubscriptionPricingResourceType:
        return SubscriptionPricingResourceType.STORAGE_ACCOUNTS

    @abstractmethod
    def _get_evidence(self, subscription_id) -> str:
        return f"Azure Defender is not enabled for Storage in the subscription `{subscription_id}`."


class ServersDefenderEnabledRule(BaseDefenderEnabledRule):
    def get_id(self) -> str:
        return 'non_car_azure_defender_for_servers_enabled'

    @abstractmethod
    def _get_resource_type(self) -> SubscriptionPricingResourceType:
        return SubscriptionPricingResourceType.VIRTUAL_MACHINES

    @abstractmethod
    def _get_evidence(self, subscription_id) -> str:
        return f"Azure Defender is not enabled for Servers in the subscription `{subscription_id}`."


class AppServicesDefenderEnabledRule(BaseDefenderEnabledRule):
    def get_id(self) -> str:
        return 'non_car_azure_defender_for_app_services_enabled'

    @abstractmethod
    def _get_resource_type(self) -> SubscriptionPricingResourceType:
        return SubscriptionPricingResourceType.APP_SERVICES

    @abstractmethod
    def _get_evidence(self, subscription_id) -> str:
        return f'Azure Defender is not enabled for App Services in the subscription `{subscription_id}`.'
