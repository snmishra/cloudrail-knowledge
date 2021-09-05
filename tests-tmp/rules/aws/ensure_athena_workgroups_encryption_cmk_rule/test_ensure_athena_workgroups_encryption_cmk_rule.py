from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_athena_workgroups_encryption_cmk_rule import \
    EnsureAthenaWorkgroupsEncryptionCmkRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureAthenaWorkgroupsEncryptionCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureAthenaWorkgroupsEncryptionCmkRule()

    def test_encrypted_sse_kms_cmk(self):
        self.run_test_case('encrypted_sse_kms_cmk', False, always_use_cache_on_jenkins=True)

    def test_encrypted_cse_kms_cmk(self):
        self.run_test_case('encrypted_cse_kms_cmk', False, always_use_cache_on_jenkins=True)

    def test_encrypted_sse_kms_s3(self):
        self.run_test_case('encrypted_sse_kms_s3', True, always_use_cache_on_jenkins=True)

    def test_encrypted_work_groups(self):
        self.run_test_case('encrypted_work_groups', True, 2, always_use_cache_on_jenkins=True)

    def test_encrypted_sse_s3(self):
        self.run_test_case('encrypted_sse_s3', True)

    def test_encrypted_cse_kms_alias_s3(self):
        self.run_test_case('encrypted_cse_kms_alias_s3', True, always_use_cache_on_jenkins=True)

    def test_encrypted_sse_kms_existing_key_alias(self):
        self.run_test_case('encrypted_sse_kms_existing_key_alias', False, always_use_cache_on_jenkins=True)

    def test_encrypted_sse_kms_alias_s3(self):
        self.run_test_case('encrypted_sse_kms_alias_s3', True, always_use_cache_on_jenkins=True)

    def test_encrypted_cse_kms_existing_key_alias(self):
        self.run_test_case('encrypted_cse_kms_existing_key_alias', False, always_use_cache_on_jenkins=True)
