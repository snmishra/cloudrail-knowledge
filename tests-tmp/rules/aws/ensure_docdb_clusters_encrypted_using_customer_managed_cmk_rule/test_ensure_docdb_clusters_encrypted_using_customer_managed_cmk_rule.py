from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.\
    ensure_docdb_clusters_encrypted_customer_managed_cmk_rule import \
    EnsureDocdbClustersEncryptedCustomerManagedCmkRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureDocdbClustersEncryptedCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDocdbClustersEncryptedCustomerManagedCmkRule()

    def test_docdb_cluster_encrypted_at_rest_using_cmk_not_customer_managed(self):
        self.run_test_case('docdb_cluster_encrypted_at_rest_using_cmk_not_customer_managed', True, always_use_cache_on_jenkins=True)

    def test_docdb_cluster_encrypted_at_rest_using_customer_managed_cmk_already_defined(self):
        self.run_test_case('docdb_cluster_encrypted_at_rest_using_customer_managed_cmk_already_defined', False, always_use_cache_on_jenkins=True)

    def test_docdb_cluster_encrypted_at_rest_using_not_customer_managed_cmk_already_defined(self):
        self.run_test_case('docdb_cluster_encrypted_at_rest_using_not_customer_managed_cmk_already_defined', True, always_use_cache_on_jenkins=True)

    def test_docdb_cluster_encrypted_without_kms_key(self):
        self.run_test_case('docdb_cluster_encrypted_without_kms_key', True, always_use_cache_on_jenkins=True)
