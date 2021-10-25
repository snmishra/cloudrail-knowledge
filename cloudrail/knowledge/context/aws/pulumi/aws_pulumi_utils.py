import functools
import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, TypedDict

if TYPE_CHECKING:
    from cloudrail.knowledge.context.aws.pulumi.aws_pulumi_context_builder import (
        PulumiPreviewOutput,
    )


@dataclass
class ResourcesData:
    resources: List[dict]
    modules: List[str]


class ProgramInfo(TypedDict):
    program: str


class AwsPulumiUtils:
    def __init__(
        self,
        preview_json: "PulumiPreviewOutput",
        resources: Dict[str, List[Dict[str, Any]]],
    ):
        # The primal default region. Will be replaced by the region specified in "aws" provider, or will be the region of "aws" provider if a
        # region was not set.
        self.config: dict = preview_json["config"]
        self.default_region: str = self.config.get("aws:region", "us-east-1")
        self.resources = resources
        self.provider_region_map: Dict[str, str] = {}

    def get_resource_region(self, urn: str) -> str:
        try:
            return self._get_resource_region(urn)
        except Exception as ex:
            logging.exception(
                f"An error occurred while trying to get the region of {urn}. "
                f'Will set the default region "{self.default_region}" Instead.\n{str(ex)}'
            )
            return self.default_region

    def _get_resource_region(self, urn: str) -> str:
        resource_type = urn.split("::")[2]
        resource = {}
        for res in self.resources[resource_type]:
            if res["urn"] == urn:
                resource = res
                break
        provider = resource.get("provider")

        if not provider:
            return self.default_region

        region = self.provider_region_map.get(provider, self.default_region)

        return region
