from typing import cast, Union, List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName

from cloudrail.knowledge.context.base_context_builders.base_pulumi_builder import (
    BasePulumiBuilder,
)
from cloudrail.knowledge.pulumi_utils import AwsProviderInfo


class AwsPulumiBuilder(BasePulumiBuilder):
    provider_info = AwsProviderInfo()
    def do_build(self, attributes: dict):
        pass

    def get_service_name(self) -> AwsServiceName:  # type: ignore
        pass

    def get_terraform_name(self):
        terraform_name = self.get_service_name().value
        return terraform_name

    def get_pulumi_name(self):
        terraform_name = self.get_service_name().value
        info = self.provider_info.Resources.get(terraform_name)
        if info is None or "Tok" not in info:
            raise Exception(f"Unknown resource name: {terraform_name}")

        pulumi_name = info["Tok"]
        return pulumi_name

    def build(self):
        all_attributes = self.resources.get(self.get_pulumi_name())
        # resource_info = self.provider_info.Resources.get(self.get_terraform_name())
        if not all_attributes:
            return []

        result = []
        for attributes in all_attributes:
            build_result = cast(
                "Union[None, AwsResource, List[AwsResource]]",
                self._build_and_map_action(attributes),
            )
            if build_result:
                if isinstance(build_result, list):
                    for item in build_result:
                        self._set_common_attributes(item, attributes)
                        result.append(item)
                else:
                    self._set_common_attributes(build_result, attributes)
                    result.append(build_result)

        return result

    @staticmethod
    def _set_common_attributes(resource: AwsResource, attributes: dict):
        if not isinstance(resource, AwsResource):
            return
        if not resource.region:
            resource.region = attributes["region"]
        resource.account = attributes["account_id"]
