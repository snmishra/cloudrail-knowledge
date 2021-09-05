import os
import shutil
import unittest
from datetime import datetime
from typing import List

from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.utils.utils import get_account_id

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
from core.entities.rule_result import RuleResultStatus
from core.environment_context.environment_context_builder_factory import EnvironmentContextBuilderFactory
from core.environment_context.terraform_resource_finder import TerraformResourceFinder
from core.rules.aws_rules_loader import AwsRulesLoader
from core.rules.rules_runner import RulesRunner, RuleExecution
from test.helpers.cli_output_helper import print_cli_output
from test.helpers.custom_terraform_helper import create_plan_json


class BaseTestScenarios(unittest.TestCase):

    def tearDown(self) -> None:
        for file in self.test_files:
            if os.path.exists(file):
                os.remove(file)

    def setUp(self) -> None:
        self.test_files = []
        self.rules_under_test = AwsRulesLoader().load().values()
        self.supported_aws_service = SupportedServicesService.list_aws_supported_services(IacType.TERRAFORM)
        self.checkov_checks = AllRulesMetadataStoreInstance.list_checkov_rule_ids()

    @staticmethod
    def _get_full_path(dir_path: str) -> str:
        abs_path = os.path.abspath(dir_path)
        if os.path.isdir(abs_path):
            return abs_path
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), dir_path)
        if os.path.isdir(dir_path):
            return dir_path
        else:
            raise Exception('cannot find dir path {}'.format(dir_path))

    @staticmethod
    def _save_result_to_file(result, dest_path):
        with open(dest_path, 'w+') as file:
            file.write(result)
        return dest_path

    def run_test_case(self, test_case_folder: str,
                      failed_rule_ids: List[str] = None,
                      show_cli_output=False,
                      always_use_cache_on_jenkins: bool = False,
                      use_cached_plan_data_ratio: int = int(os.getenv("TESTS_CACHED_PLAN_RATIO", "100")),
                      use_state_file: bool = False):
        # Arrange
        try:
            local_account_data = None
            test_case_folder_full_path = self._get_full_path(test_case_folder)
            plan_json = create_plan_json(use_cached_plan_data_ratio,
                                         test_case_folder_full_path,
                                         test_case_folder_full_path,
                                         always_use_cache_on_jenkins,
                                         use_state_file)
            self.test_files.append(plan_json)
            TerraformResourceFinder.initialize()
            TerraformRawDataExplorer.update_working_dir(test_case_folder_full_path)

            local_account_data = os.path.join(test_case_folder_full_path, 'account-data')

            account_data_zip = f'{local_account_data}.zip'

            if os.path.isfile(account_data_zip):
                shutil.unpack_archive(account_data_zip, extract_dir=local_account_data, format='zip')
                account_data = local_account_data
            else:
                current_path = os.path.dirname(os.path.abspath(__file__))
                account_data = os.path.join(current_path, '..', 'testing-accounts-data', 'account-data-vpc-platform')

            account_id = get_account_id(account_data)
            customer_id = '00000000-0000-0000-0000-000000000000'
            CustomerStringUtils.set_hashcode_salt(customer_id)
            context_service = TerraformContextService(TerraformPlanConverter())
            checkov_results = context_service.run_checkov_checks(test_case_folder_full_path, self.checkov_checks)
            terraform_result = context_service.process_json_result(plan_json,
                                                                   self.supported_aws_service,
                                                                   checkov_results.result,
                                                                   customer_id,
                                                                   '',
                                                                   '',
                                                                   CloudProviderDTO.AMAZON_WEB_SERVICES)

            output_path = self._save_result_to_file(terraform_result.result, os.path.join(test_case_folder_full_path, 'output.json'))
            encode_ips_in_file(output_path, customer_id, EncryptionMode.DECRYPT)
            self.test_files.append(output_path)

            context = EnvironmentContextBuilderFactory.get(CloudProvider.AMAZON_WEB_SERVICES, IacType.TERRAFORM).build(account_data,
                                                                                                                       output_path,
                                                                                                                       account_id)

            # Act
            rules_results = []
            for rule_under_test in self.rules_under_test:
                rule_id = rule_under_test.get_id()
                rule_start_time = datetime.now()
                rule_result = RulesRunner.run_rules({rule_id: RuleExecution(rule_under_test,
                                                                            None,
                                                                            RuleEnforcementMode.MANDATE_ALL_RESOURCES,
                                                                            None)},
                                                    context,
                                                    None,
                                                    CloudProvider.AMAZON_WEB_SERVICES)[0]
                rules_results.append(rule_result)
                rule_end_time = datetime.now()
                rule_runtime_seconds = (rule_end_time - rule_start_time).total_seconds()

                # Assert
                if failed_rule_ids and rule_id in failed_rule_ids:
                    self.assertEqual(RuleResultStatus.FAILED, rule_result.status)
                    failed_rule_ids.remove(rule_id)
                self.assertLess(rule_runtime_seconds, 60, f'The test {rule_id} took {rule_runtime_seconds} seconds to run')

            self.assertFalse(failed_rule_ids, 'not all requested rules ran: {}'.format(failed_rule_ids))

            if show_cli_output:
                print_cli_output(rules_results)
        finally:
            TerraformResourceFinder.destroy()
            TerraformRawDataExplorer.reset_working_dir()
            shutil.rmtree(local_account_data, ignore_errors=True)
