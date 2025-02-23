import json
from typing import Optional

from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from cloudrail.knowledge.utils.terraform_output_validator import TerraformOutputValidator
from cloudrail.knowledge.context.environment_context.terraform_resources_helper import get_raw_resources_by_type
from cloudrail.knowledge.context.environment_context.terraform_resources_metadata_parser import TerraformResourcesMetadataParser
from cloudrail.knowledge.context.gcp.resources_builders.terraform.sql_database_instance_builder import SqlDatabaseInstanceBuilder
from cloudrail.knowledge.context.environment_context.iac_context_builder import IacContextBuilder
from cloudrail.knowledge.utils.checkov_utils import to_checkov_results


class GcpTerraformContextBuilder(IacContextBuilder):

    @staticmethod
    def build(iac_file: str,
              account_id: str,
              scanner_environment_context: Optional[BaseEnvironmentContext] = None,
              salt: Optional[str] = None,
              **extra_args) -> GcpEnvironmentContext:
        if not iac_file:
            return GcpEnvironmentContext()
        iac_url_template: Optional[str] = extra_args.get('iac_url_template')
        with open(iac_file, 'r+') as file:
            data = file.read()
            TerraformOutputValidator.validate(data)
            dic = json.loads(data)
            resources_metadata = TerraformResourcesMetadataParser.parse(dic['configuration'])
            resources = get_raw_resources_by_type(dic['resource_changes'], resources_metadata)
            for resource in resources.values():
                for entity in resource:
                    entity['_project_id'] = account_id
                    entity['iac_url_template'] = iac_url_template

            context: GcpEnvironmentContext = GcpEnvironmentContext()
            context.checkov_results = to_checkov_results(dic.get('checkov_results', {}))

            context.sql_database_instances = SqlDatabaseInstanceBuilder(resources).build()
            return context
