import inspect
import json
import os
import shutil
import unittest
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, Optional
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.context.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from cloudrail.knowledge.context.environment_context.terraform_resource_finder import TerraformResourceFinder
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.utils.terraform_show_output_transformer import TerraformShowOutputTransformer
from cloudrail.knowledge.rules.base_rule import RuleResponse, RuleResultType
from cloudrail.knowledge.rules.rules_executor import RulesExecutor
from cloudrail.knowledge.utils.iac_fields_store import IacFieldsStore
from cloudrail.knowledge.utils.utils import get_account_id


def rule_test_wrapper(*args, **kwargs) -> Callable:
    def _rules_tests_wrapper(test_case_func: Callable) -> Callable:
        def test_case_wrapper(self) -> None:
            # todo - support iac types executions
            rule_response: RuleResponse = self.run_test_case(*args, **kwargs)
            test_case_func(self, rule_response)
        return test_case_wrapper
    return _rules_tests_wrapper


class BaseRuleTest(unittest.TestCase):

    DUMMY_CUSTOMER_ID: str = '00000000-0000-0000-0000-000000000000'

    def __init__(self, *args, **kwargs):
        # pylint: disable=super-with-arguments
        super(BaseRuleTest, self).__init__(*args, **kwargs)
        self.account_id = None
        self.account_data = None
        self.output_path = None
        self.salt = None
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
            file.write(json.dumps(result))
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
                      number_of_issue_items: int = 1) -> RuleResponse:

        local_account_data = None
        try:
            # Arrange
            TerraformResourceFinder.initialize()
            test_case_folder_full_path = self._get_full_path(test_case_folder)
            local_account_data = os.path.join(test_case_folder_full_path, 'account-data')
            account_data_zip = f'{local_account_data}.zip'

            if os.path.isfile(account_data_zip):
                shutil.unpack_archive(account_data_zip, extract_dir=local_account_data, format='zip')
                self.account_data = local_account_data
            else:
                self.account_data = self.set_default_account_data()

            self.account_id = self.get_account_id(self.account_data)
            self.salt = self.DUMMY_CUSTOMER_ID
            plan_json = os.path.join(test_case_folder_full_path, 'cached_plan.json')
            result = TerraformShowOutputTransformer.transform(plan_json,
                                                                    '',
                                                                    self.get_supported_service(),
                                                                    self.salt)
            self.output_path = self._save_result_to_file(result,
                                                         os.path.join(test_case_folder_full_path, 'output.json'))
            self.test_files.append(self.output_path)
            context = self.build_environment_context()
            return self._execute_rule_and_assert(iac_type=IacType.TERRAFORM, env_context=context,
                                                 should_alert=should_alert,
                                                 number_of_issue_items=number_of_issue_items)
        finally:
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

    @abstractmethod
    def get_cloud_provider(self):
        pass

    def _execute_rule_and_assert(self, iac_type: IacType, env_context: BaseEnvironmentContext, should_alert: bool,
                                 number_of_issue_items: int) -> RuleResponse:
        rule_start_time: datetime = datetime.now()
        rule_result: RuleResponse = RulesExecutor.execute(self.get_cloud_provider(), env_context, [self.rule_under_test.get_id()])[0]
        rule_result.iac_type = iac_type
        self._assert_rule(rule_result=rule_result, should_alert=should_alert,
                          number_of_issue_items=number_of_issue_items, rule_start_time=rule_start_time)
        return rule_result

    def _assert_rule(self, rule_result: RuleResponse, should_alert: bool,
                     number_of_issue_items: int, rule_start_time: datetime) -> None:
        rule_end_time = datetime.now()
        rule_runtime_seconds = (rule_end_time - rule_start_time).total_seconds()
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, rule_result.status)
            self.assertEqual(number_of_issue_items, len(rule_result.issues), rule_result.issues)
        else:
            self.assertNotEqual(RuleResultType.FAILED, rule_result.status,
                                f'rule result failed and it shouldn\'t have: {rule_result.issues}')

        self.assertLess(rule_runtime_seconds, 20,
                        f'The test {self.rule_under_test.get_id()} took {rule_runtime_seconds} seconds to run')


class AzureBaseRuleTest(BaseRuleTest, ABC):

    def get_cloud_provider(self):
        return CloudProvider.AZURE

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
        return IacFieldsStore.get_azure_supported_services()


class AwsBaseRuleTest(BaseRuleTest, ABC):

    def get_cloud_provider(self):
        return CloudProvider.AMAZON_WEB_SERVICES

    def get_supported_service(self):
        return IacFieldsStore.get_terraform_aws_supported_services()

    def get_account_id(self, account_data):
        return get_account_id(account_data)

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES,
                                                    IacType.TERRAFORM).build(self.account_data,
                                                                             self.output_path,
                                                                             self.account_id,
                                                                             self.salt)

    def set_default_account_data(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../', 'testing-accounts-data', 'account-data-vpc-platform')

    def _run_cloudformation_test_case(self, test_case_folder: str,
                                      should_alert: bool = True,
                                      number_of_issue_items: int = 1) -> RuleResponse:

        test_case_folder_full_path = self._get_full_path(test_case_folder)
        local_account_data = os.path.join(test_case_folder_full_path, 'cfn-account-data')
        cfn_template_yaml_file: str = os.path.join(test_case_folder_full_path, 'cloudformation.yaml')
        account_data_zip = f'{local_account_data}.zip'
        rule_result: Optional[RuleResponse] = None

        if os.path.exists(cfn_template_yaml_file):
            if os.path.isfile(account_data_zip):
                shutil.unpack_archive(account_data_zip, extract_dir=local_account_data, format='zip')
                self.account_data = local_account_data
            else:
                self.account_data = self.set_default_account_data()

            self.account_id = self.get_account_id(self.account_data)
            self.customer_id = self.DUMMY_CUSTOMER_ID

            context = EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES,
                                                           IacType.CLOUDFORMATION) \
                .build(account_data_dir_path=self.account_data,
                       iac_file_path=cfn_template_yaml_file, account_id=self.account_id,
                       salt=self.customer_id, **{'region': 'us-east-1'})

            rule_result = self._execute_rule_and_assert(iac_type=IacType.CLOUDFORMATION, env_context=context,
                                                        should_alert=should_alert,
                                                        number_of_issue_items=number_of_issue_items)
        return rule_result


class GcpBaseRuleTest(BaseRuleTest, ABC):

    def get_cloud_provider(self):
        return CloudProvider.GCP

    def get_account_id(self, account_data):
        return 'dev-tomer'  # TODO: create a project for tests and put project-id here

    def build_environment_context(self):
        return EnvironmentContextBuilderFactory.get(CloudProvider.GCP, IacType.TERRAFORM).build(self.account_data,
                                                                                                self.output_path,
                                                                                                self.account_id)

    def set_default_account_data(self):
        return None

    def get_supported_service(self):
        return IacFieldsStore.get_terraform_gcp_supported_services()
