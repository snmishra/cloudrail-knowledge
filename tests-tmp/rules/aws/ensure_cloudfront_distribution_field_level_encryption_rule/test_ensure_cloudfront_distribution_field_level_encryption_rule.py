from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_in_transit.ensure_cloudfront_distribution_field_level_encryption_rule import \
    EnsureCloudfrontDistributionFieldLevelEncryptionRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureCloudfrontDistributionFieldLevelEncryptionRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudfrontDistributionFieldLevelEncryptionRule()

    def test_field_level_encryption_enabled(self):
        self.run_test_case('field_level_encryption_enabled', False)

    def test_protocol_viewer_policy_allow_all(self):
        rule_result = self.run_test_case('protocol_viewer_policy_allow_all', True, always_use_cache_on_jenkins=True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("is not set to use Field Level Encryption to protect data in transit in default_cache_behavior and in"
                        " [\'ordered_cache_behavior #1\', \'ordered_cache_behavior #2\']" in rule_result.issue_items[0].evidence)
        self.assertEqual(rule_result.issue_items[0].exposed.type, 'CloudFront Distribution')
        self.assertEqual(rule_result.issue_items[0].exposed.iac_entity_id, 'aws_cloudfront_distribution.s3_distribution')
        self.assertEqual(rule_result.issue_items[0].violating.type, 'CloudFront Distribution')
        self.assertEqual(rule_result.issue_items[0].violating.iac_entity_id, 'aws_cloudfront_distribution.s3_distribution')
