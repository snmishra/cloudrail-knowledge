import unittest
from cloudrail.knowledge.rules.aws.aws_rules_metadata_store import AwsRulesMetadataStore
from cloudrail.knowledge.rules.azure.azure_rules_metadata_store import AzureRulesMetadataStore
from cloudrail.knowledge.rules.gcp.gcp_rules_metadata_store import GcpRulesMetadataStore
from cloudrail.knowledge.rules.rules_metadata_store import RulesMetadataStore
from cloudrail.knowledge.context.cloud_provider import CloudProvider

class TestRuleMetadataStore(unittest.TestCase):

    def test_aws_rule_metadata_store(self):
        aws_rule_metadata_store: RulesMetadataStore = AwsRulesMetadataStore()

        self.assertIsNotNone(aws_rule_metadata_store.rules_metadata)
        self.assertIsNotNone(aws_rule_metadata_store.list_rules_metadata())
        self.assertEqual(aws_rule_metadata_store.list_rules_metadata()[0].cloud_provider, CloudProvider.AMAZON_WEB_SERVICES)

    def test_azure_rule_metadata_store(self):
        azure_rule_metadata_store: RulesMetadataStore = AzureRulesMetadataStore()

        self.assertIsNotNone(azure_rule_metadata_store.rules_metadata)
        self.assertIsNotNone(azure_rule_metadata_store.list_rules_metadata())
        self.assertEqual(azure_rule_metadata_store.list_rules_metadata()[0].cloud_provider, CloudProvider.AZURE)

    def test_gcp_rule_metadata_store(self):
        gcp_rule_metadata_store: RulesMetadataStore = GcpRulesMetadataStore()

        self.assertIsNotNone(gcp_rule_metadata_store.rules_metadata)
        self.assertIsNotNone(gcp_rule_metadata_store.list_rules_metadata())
