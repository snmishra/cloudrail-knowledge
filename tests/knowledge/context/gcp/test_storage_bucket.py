from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket import GcpStorageBucket, GcpStorageBucketStorageClass
from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestStorageBucket(GcpContextTest):
    def get_component(self):
        return 'storage_bucket'

    @context(module_path="default_bucket")
    def test_basic(self, ctx: GcpEnvironmentContext):
        self._assert_bucket(ctx, 'test-bucket-3767')

    def _assert_bucket(self, ctx: GcpEnvironmentContext, bucket_name: str):
        self.assertEqual(len(ctx.storage_buckets), 1)
        storage_bucket: GcpStorageBucket = ctx.storage_buckets.get(bucket_name)
        self.assertIsNotNone(storage_bucket)
        self.assertEqual(storage_bucket.region, 'EU')
        self.assertEqual(storage_bucket.get_id(), bucket_name)
        self.assertEqual(storage_bucket.get_name(), bucket_name)
        self.assertEqual(storage_bucket.storage_class, GcpStorageBucketStorageClass.STANDARD)
        self.assertEqual(storage_bucket.uniform_bucket_level_access, False)
