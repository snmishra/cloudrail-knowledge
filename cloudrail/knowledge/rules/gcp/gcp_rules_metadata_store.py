import os

from cloudrail.knowledge.rules.rules_metadata_store import RulesMetadataStore, read_metadata_file


class GcpRulesMetadataStore(RulesMetadataStore):
    def __init__(self):
        raw_data = read_metadata_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gcp_rules_metadata.yaml'))
        super().__init__(raw_data)
