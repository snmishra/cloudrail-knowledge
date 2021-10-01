from typing import Dict, List, Optional, TypedDict

from cloudrail.knowledge.context.iac_resource_metadata import IacResourceMetadata


class PulumiMetadata(TypedDict):
    iac_entity_id: str
    oldState: dict
    newState: dict


class PulumiResourcesMetadataParser:
    @classmethod
    def parse(cls, steps: List[dict]) -> Dict[str, PulumiMetadata]:
        # We don't have any metadata in Pulumi IaC file, just pass
        return {}
        result = {}
        cls._fill_module_content(steps, None, result)
        return result

    @classmethod
    def _fill_module_content(
        cls,
        content: List[dict],
        module_metadata: Optional[PulumiMetadata],
        result: Dict[str, PulumiMetadata],
    ):
        cls._add_resources(content, module_metadata, result)

    @classmethod
    def _add_resources(
        cls,
        content: List[dict],
        module_metadata: Optional[PulumiMetadata],
        result: Dict[str, PulumiMetadata],
    ):
        for resource in content:
            metadata = cls._create_resource_metadata(resource, resource["urn"])
            result[metadata["iac_entity_id"]] = metadata

    @classmethod
    def _create_resource_metadata(cls, data: dict, address: str) -> PulumiMetadata:
        metadata: PulumiMetadata = {
            "iac_entity_id": address,
            "oldState": data.get("oldState", {}),
            "newState": data.get("newState", {}),
        }
        return metadata
