import logging
from abc import abstractmethod, ABC
from collections.abc import Iterable

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.iac_resource_metadata import IacResourceMetadata
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.iac_action_type import IacActionType

from cloudrail.knowledge.context.environment_context.terraform_resource_finder import TerraformResourceFinder


class BaseTerraformBuilder(ABC):

    def __init__(self, resources: dict):
        self.resources = resources

    def _build_and_map_action(self, attributes):
        for key, value in attributes.items():
            if value and isinstance(value, str) and '{' not in value:
                attributes[key] = value.replace('"', '')
        address = attributes.get('tf_address')
        try:
            action = IacActionType(attributes['tf_action'])
            is_new: bool = attributes.get('is_new', False)
            metadata: IacResourceMetadata = attributes['metadata']
            if metadata:
                metadata.resource_type = metadata.iac_entity_id.split(".")[0]
            build_result = self.do_build(attributes)
            iac_state = IacState(address,
                                 action, metadata,
                                 is_new,
                                 metadata and metadata.get_iac_resource_url(attributes.get('iac_url_template')))
            if isinstance(build_result, list):
                for instance in build_result:
                    self._finalize_component(instance, iac_state)
            elif build_result:
                self._finalize_component(build_result, iac_state, attributes)
            return build_result
        except Exception as ex:
            self._report_error(address, ex)
            return None

    def _report_error(self, resource_address: str, ex: Exception):
        key_name = str(ex) if isinstance(ex, KeyError) else None
        key_message = '\nexpected to have missing key {}'.format(key_name) if key_name else ''
        message = 'build component failed.\ntype:: {}\naddress:: {}{}'.format(self.get_service_name().value, resource_address, key_message)
        # report_error(message, type(ex).__name__) # TODO how to report error to lumigo
        logging.exception(f'{message}\n{str(ex)}', exc_info=ex)

    @staticmethod
    def _finalize_component(instance: Mergeable, iac_state: IacState, attributes: dict = None):
        instance.iac_state = iac_state
        TerraformResourceFinder.add_resource(instance)
        for tag_key in ('tags_all', 'tags', 'tag'):
            if instance.is_tagable and attributes and isinstance(attributes.get(tag_key), dict):
                instance.tags = attributes[tag_key] or {}
                break

    @abstractmethod
    def do_build(self, attributes: dict):
        pass

    @abstractmethod
    def get_service_name(self) -> AzureResourceType:
        pass

    @staticmethod
    def _is_known_value(attributes: dict, key: str) -> bool:
        address = attributes.get('tf_address', '')
        value = attributes.get(key)
        return isinstance(value, (bool, int)) or (value and (not isinstance(value, Iterable)
                                                             or not address or address not in value))

    @staticmethod
    def _get_known_value(attributes: dict, key: str, default=None):
        return attributes.get(key) if BaseTerraformBuilder._is_known_value(attributes, key) else default
