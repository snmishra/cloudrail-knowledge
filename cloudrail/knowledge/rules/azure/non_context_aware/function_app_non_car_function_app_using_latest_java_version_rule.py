from typing import List, Dict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class FunctionAppUsingLatestJavaVersionRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_function_app_using_latest_java_version'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        java = False
        version = ''
        for func_app in env_context.function_apps:
            if func_app.app_service_config.linux_fx_version or func_app.app_service_config.java_version:
                if func_app.app_service_config.linux_fx_version and func_app.app_service_config.linux_fx_version.split('|')[0] == 'JAVA':
                    if func_app.app_service_config.linux_fx_version.split('|')[0] == 'JAVA':
                        version = func_app.app_service_config.linux_fx_version.split('|')[1]
                        java = True
                elif func_app.app_service_config.java_version:
                    version = func_app.app_service_config.java_version
                    java = True
                if java:
                    if version != '11':
                        issues.append(
                            Issue(
                                f'The {func_app.get_type()} `{func_app.get_friendly_name()}` does not use the latest Azure supported Java version (11).',
                                func_app,
                                func_app))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.function_apps)
