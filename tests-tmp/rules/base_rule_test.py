import inspect
import os
import shutil
import unittest
import uuid
from abc import abstractmethod, ABC
from datetime import datetime

from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.utils.utils import get_account_id

from cloudrail.cli.api_client.external_api_client import ExternalApiClient
from cloudrail.cli.terraform_service.terraform_context_service import TerraformContextService
from cloudrail.cli.terraform_service.terraform_plan_converter import TerraformPlanConverter
from cloudrail.cli.terraform_service.terraform_raw_data_explorer import TerraformRawDataExplorer
from common.all_rules_metadata_store import AllRulesMetadataStoreInstance
from common.api.dtos.cloud_provider_dto import CloudProviderDTO
from common.constants import IacType
from common.ip_encryption_utils import encode_ips_in_file, EncryptionMode
from common.utils.customer_string_utils import CustomerStringUtils
from core.api.aws_lambda.services.supported_services_service import SupportedServicesService
from core.entities.rule_enforcement_mode import RuleEnforcementMode
from core.entities.rule_result import RuleResultStatus, RuleResult
from core.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from core.environment_context.terraform_resource_finder import TerraformResourceFinder
from core.rules.rules_runner import RulesRunner, RuleExecution
from test.helpers.cli_output_helper import print_cli_output
from test.helpers.custom_terraform_helper import create_plan_json


class BaseRuleTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        # pylint: disable=super-with-arguments
        super(BaseRuleTest, self).__init__(*args, **kwargs)
        self.account_id = None
        self.account_data = None
        self.output_path = None
        self.tenant_id = str(uuid.uuid4())

    @abstractmethod
    def get_rule(self):
        pass

    def tearDown(self) -> None:
        for file in self.test_files:
            if os.path.exists(file):
                os.remove(file)

    def setUp(self) -> None:
        self.test_files = []
        self.rule_under_test = self.get_rule()
        self.checkov_checks = AllRulesMetadataStoreInstance.list_checkov_rule_ids()
        if not os.environ.get('AWS_DEFAULT_REGION', os.environ.get('AWS_REGION')):
            os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

    def _get_full_path(self, dir_path: str) -> str:
        abs_path = os.path.abspath(dir_path)
        if os.path.isdir(abs_path):
            return abs_path
        dir_path = os.path.join(self._find_caller_path(), dir_path)
        if os.path.isdir(dir_path):
            return dir_path
        else:
            raise Exception('cannot find dir path {}'.format(dir_path))

    @staticmethod
    def _save_result_to_file(result, dest_path):
        with open(dest_path, 'w+') as file:
            file.write(result)
        return dest_path

    @staticmethod
    def _find_caller_path() -> str:
        current_file = os.path.abspath(__file__)
        stack = inspect.stack()
        for info in stack:
            # search for the first file which is not the current one.
            if os.path.abspath(info.filename) != os.path.abspath(current_file):
                return os.path.dirname(info.filename)
        return ''

    def run_test_case(self, test_case_folder: str,
                      should_alert: bool = True,
                      number_of_issue_items: int = 1,
                      show_cli_output=False,
                      always_use_cache_on_jenkins: bool = False,
                      use_state_file: bool = False,
                      use_cached_plan_data_ratio: int = int(os.getenv("TESTS_CACHED_PLAN_RATIO", "100"))) -> RuleResult:

        local_account_data = None
        try:
            # Arrange
            TerraformResourceFinder.initialize()
            test_case_folder_full_path = self._get_full_path(test_case_folder)
            plan_json = create_plan_json(use_cached_plan_data_ratio,
                                         test_case_folder_full_path,
                                         test_case_folder_full_path,
                                         always_use_cache_on_jenkins,
                                         use_state_file)
            self.test_files.append(plan_json)
            TerraformRawDataExplorer.update_working_dir(test_case_folder_full_path)

            local_account_data = os.path.join(test_case_folder_full_path, 'account-data')

            account_data_zip = f'{local_account_data}.zip'

            if os.path.isfile(account_data_zip):
                shutil.unpack_archive(account_data_zip, extract_dir=local_account_data, format='zip')
                self.account_data = local_account_data
            else:
                self.account_data = self.set_default_account_data()

            self.account_id = self.get_account_id(self.account_data)
            customer_id = '00000000-0000-0000-0000-000000000000'
            CustomerStringUtils.set_hashcode_salt(customer_id)
            context_service = TerraformContextService(TerraformPlanConverter())
            checkov_results = context_service.run_checkov_checks(test_case_folder_full_path, self.checkov_checks)
            terraform_result = context_service.process_json_result(plan_json,
                                                                   self.get_supported_service(),
                                                                   checkov_results.result,
                                                                   customer_id,
                                                                   ExternalApiClient.get_cli_handshake_version(),
                                                                   '',
                                                                   CloudProviderDTO.AMAZON_WEB_SERVICES)

            self.output_path = self._save_result_to_file(terraform_result.result,
                                                         os.path.join(test_case_folder_full_path, 'output.json'))
            encode_ips_in_file(self.output_path, customer_id, EncryptionMode.DECRYPT)
            self.test_files.append(self.output_path)
            context = self.build_environment_context()

            # Act
            rule_start_time = datetime.now()
            rule_result = RulesRunner.run_rules({self.rule_under_test.get_id():
                                                               RuleExecution(self.rule_under_test, None, RuleEnforcementMode.MANDATE_ALL_RESOURCES,
                                                                             None)}, context, None, None)[0]
            rule_end_time = datetime.now()
            rule_runtime_seconds = (rule_end_time - rule_start_time).total_seconds()
            if show_cli_output:
                print_cli_output([rule_result])
            # Assert
            if should_alert:
                self.assertEqual(RuleResultStatus.FAILED, rule_result.status)
                self.assertEqual(number_of_issue_items, len(rule_result.issue_items), rule_result.issue_items)
            else:
                self.assertNotEqual(RuleResultStatus.FAILED, rule_result.status,
                                    f'rule result failed and it shouldn\'t have: {rule_result.issue_items}')

            self.assertLess(rule_runtime_seconds, 20,
                            f'The test {self.rule_under_test.get_id()} took {rule_runtime_seconds} seconds to run')

            return rule_result
        finally:
            TerraformRawDataExplorer.reset_working_dir()
            TerraformResourceFinder.destroy()
            if local_account_data:
                shutil.rmtree(local_account_data, ignore_errors=True)

    @abstractmethod
    def build_environment_context(self):
        pass

    @abstractmethod
    def set_default_account_data(self):
        pass

    @abstractmethod
    def get_account_id(self, account_data):
        pass

    @abstractmethod
    def get_supported_service(self):
        pass


class AzureBaseRuleTest(BaseRuleTest, ABC):
    def get_account_id(self, account_data):
        return 'ae7905ce-4577-4a32-934b-9f662c77869d'

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AZURE, IacType.TERRAFORM).build(self.account_data,
                                                                                                  self.output_path,
                                                                                                  self.account_id,
                                                                                                  tenant_id=self.tenant_id)

    def set_default_account_data(self):
        return None

    def get_supported_service(self):
        return SupportedServicesService.list_azure_supported_services()


class AwsBaseRuleTest(BaseRuleTest, ABC):
    def get_supported_service(self):
        return SupportedServicesService.list_aws_supported_services(IacType.TERRAFORM)

    def get_account_id(self, account_data):
        return get_account_id(account_data)

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES,
                                                    IacType.TERRAFORM).build(self.account_data,
                                                                             self.output_path,
                                                                             self.account_id)

    def set_default_account_data(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../', 'testing-accounts-data', 'account-data-vpc-platform')


class GcpBaseRuleTest(BaseRuleTest, ABC):
    def get_account_id(self, account_data):
        return 'dev-tomer'  # TODO: create a project for tests and put project-id here

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.GCP, IacType.TERRAFORM).build(self.account_data,
                                                                                                self.output_path,
                                                                                                self.account_id)

    def set_default_account_data(self):
        return None

    def get_supported_service(self):
        return SupportedServicesService.list_gcp_supported_services()
