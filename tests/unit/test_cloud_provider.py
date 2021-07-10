import unittest

from parameterized import parameterized

from cloudrail.knowledge.context.cloud_provider import CloudProvider


class TestCloudProvider(unittest.TestCase):
    @parameterized.expand(
        [
            [CloudProvider.AMAZON_WEB_SERVICES, 'aws'],
            [CloudProvider.AZURE, 'azure'],
            [CloudProvider.GCP, 'gcp'],
        ]
    )
    def test_to_shorthand_string(self, cloud_provider: CloudProvider, expected_result: str):
        self.assertEqual(cloud_provider.to_shorthand_string(), expected_result)

    @parameterized.expand(
        [
            [CloudProvider.AMAZON_WEB_SERVICES, 'aws'],
            [CloudProvider.AMAZON_WEB_SERVICES, 'AMAZON_WEB_SERVICES'],
            [CloudProvider.AMAZON_WEB_SERVICES, 'amazon_web_services'],
            [CloudProvider.AMAZON_WEB_SERVICES, 'AmaZon_WeB_services'],
            [CloudProvider.AZURE, 'azure'],
            [CloudProvider.AZURE, 'AZURE'],
            [CloudProvider.AZURE, 'AzUrE'],
            [CloudProvider.GCP, 'gcp'],
            [CloudProvider.GCP, 'GCP'],
            [CloudProvider.GCP, 'GcP'],
            [CloudProvider.GCP, 'google_cloud_provider'],
            [CloudProvider.GCP, 'GoOgLE_cloud_provider'],
        ]
    )
    def test_from_string(self, expected_cloud_provider: CloudProvider, value: str):
        self.assertEqual(CloudProvider.from_string(value), expected_cloud_provider)
