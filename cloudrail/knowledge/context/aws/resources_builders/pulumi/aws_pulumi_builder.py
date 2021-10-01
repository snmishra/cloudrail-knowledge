from typing import cast, Union, List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName

from cloudrail.knowledge.context.base_context_builders.base_pulumi_builder import (
    BasePulumiBuilder,
)


class AwsPulumiBuilder(BasePulumiBuilder):
    def do_build(self, attributes: dict):
        pass

    def get_service_name(self) -> AwsServiceName:  # type: ignore
        pass

    def build(self):
        all_attributes = self.resources.get(self.get_service_name().value)
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
