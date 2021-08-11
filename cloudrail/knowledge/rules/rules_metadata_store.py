import os
from cloudrail.knowledge.rules.base_rules_metadata_store import BaseRulesMetadataStore, read_metadata_file

class RulesMetadataStore(BaseRulesMetadataStore):
    def __init__(self):
        super().__init__({})
        self.add_rules_metadata(read_metadata_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aws/aws_rules_metadata.yaml')))
        self.add_rules_metadata(read_metadata_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'azure/azure_rules_metadata.yaml')))
        self.add_rules_metadata(read_metadata_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gcp/gcp_rules_metadata.yaml')))
