from typing import List
import unittest

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import drift_test, BaseAwsDriftTest


class TestLiveEnv(BaseAwsDriftTest):

    def get_component(self):
        return 'live_env_test'

    @unittest.skip('Skipping this test, until we will fix the function: "get_account_id_from_account_data" to return relevant data and not 0000')
    @drift_test(module_path="from_develop", from_live_env=True, live_customer_id='ed52db48-5253-45f6-9933-aa77a42d9f6c')
    def test_live_env_drift(self, results: List[Drift]):
        self.assertEqual(len(results), 12)
        for result in results:
            self.assertTrue(result.resource_type in ('KMS alias', 'KMS key', 'KMS key resource policy'))
