from cloudrail.knowledge.context.environment_context.pulumi_resources_metadata_parser import (
    PulumiMetadata,
)
from typing import Any, Dict, Generic, List, TypeVar

from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.iac_resource_metadata import IacResourceMetadata
from cloudrail.knowledge.pulumi_utils import ResourceInfo, terraform_to_pulumi_name

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class ResourceDict(Dict[_KT, _VT]):
    """A special dict class that snakeCase keys also as snake_case"""

    pulumi_schema = None

    def _k(self, k: _KT) -> _KT:
        if isinstance(k, str) and k not in self:
            new_key = terraform_to_pulumi_name(k, pulumi_schema=self.pulumi_schema)
            if new_key in self:
                return type(k)(new_key)
        return k

    def __getitem__(self, k: _KT) -> _VT:
        return super().__getitem__(self._k(k))


def resource_dict_factory(provider_name, provider_info):
    return type(ResourceDict)(
        f"{provider_name}ResourceDict",
        (ResourceDict,),
        {"pulumi_schema": provider_info.Resources},
    )


def get_before_raw_resources_by_type(
    raw_data,
    resources_metadata: Dict[str, PulumiMetadata],
    pulumi_resource_info: Dict[str, ResourceInfo] = {},
) -> Dict[str, List[Dict[str, Any]]]:
    resources = ResourceDict()
    for resource in raw_data:
        # Pulumi doesn't report anything not managed, IIUC
        # if resource["mode"] != "managed":
        #     continue

        before_att = resource.get("oldState", ResourceDict())
        if not before_att:
            continue
        resource_type = before_att["type"]
        if resource_type not in resources:
            resources[resource_type] = []
        address = resource["urn"]
        metadata = resources_metadata.get(address)
        attributes = before_att
        op = resource["op"]
        attributes["address"] = before_att["urn"]
        attributes["action"] = op
        attributes["metadata"] = metadata
        attributes["is_new"] = False
        resource_info = pulumi_resource_info.get(resource_type)
        resources[resource_type].append(attributes)
    return resources


def get_after_raw_resources_by_type(
    raw_data,
    resources_metadata: Dict[str, PulumiMetadata],
    keep_deleted_entities=True,
):
    resources = ResourceDict()
    for resource in raw_data:
        address = resource["urn"]  # IacState requires address key
        before_att = resource.get("oldState", ResourceDict())
        after_att = resource.get("newState", ResourceDict())
        resource_type = before_att.get("type") or after_att.get("type")
        if resource_type is None:
            raise Exception(f"Incorrect resource type {address}")

        if resource_type not in resources:
            resources[resource_type] = []

        # This bit gets the terraform properties of the object, not available in Pulumi file
        # if after_att:
        #     if resource["change"]["after_unknown"]:
        #         for key in resource["change"]["after_unknown"]:
        #             after_att[key] = after_att.get(key, "{}.{}".format(address, key))
        #     after_att["tf_address"] = address

        metadata = resources_metadata.get(address)
        if resource["op"] != "update":
            attributes = after_att or before_att
            attributes["address"] = address
            attributes["action"] = resource["op"]
            attributes["metadata"] = metadata
            attributes["is_new"] = bool((not before_att) and after_att)
            resources[resource_type].append(attributes)
        elif resource["op"] == "update":
            if keep_deleted_entities:
                before_att["action"] = IacActionType.DELETE.value
                before_att["metadata"] = metadata
                before_att["is_new"] = False
                before_att["address"] = address
                resources[resource_type].append(before_att)
            after_att["action"] = IacActionType.CREATE.value
            after_att["metadata"] = metadata
            after_att["is_new"] = resource["op"] == "update-replace"
            after_att["address"] = address
            resources[resource_type].append(after_att)

    return resources


def get_raw_resources_by_type(
    raw_data,
    resources_metadata: Dict[str, PulumiMetadata],
    use_after_data=True,
    keep_deleted_entities=True,
):
    if use_after_data:
        return get_after_raw_resources_by_type(
            raw_data, resources_metadata, keep_deleted_entities
        )
    else:
        return get_before_raw_resources_by_type(raw_data, resources_metadata)
