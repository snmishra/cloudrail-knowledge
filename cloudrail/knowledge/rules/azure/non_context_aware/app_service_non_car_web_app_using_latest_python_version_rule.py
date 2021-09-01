from typing import List, Dict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from packaging import version

class AppServiceUseLatestPythonVersionRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_web_app_using_latest_python_version'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for app_service in env_context.app_services:
            if app_service.app_service_config and app_service.app_service_config.linux_fx_version:
                framework_type, framework_version = app_service.app_service_config.linux_fx_version.split("|")
                if str(framework_type).lower() == 'python':
                    framework_version = version.parse(framework_version)
                    if framework_version < version.parse('3.9'):
                        issues.append(
                            Issue(
                                f'The {app_service.get_type()} `{app_service.get_friendly_name()}`does not use the latest Azure supported Python version (3.9).',
                                app_service, app_service))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.app_services)
