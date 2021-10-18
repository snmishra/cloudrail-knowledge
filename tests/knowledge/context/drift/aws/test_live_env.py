from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import drift_test, BaseAwsDriftTest


class TestLiveEnv(BaseAwsDriftTest):

    def get_component(self):
        return 'live_env_test'

    @drift_test(module_path="from_develop", from_live_env=True, live_customer_id='ed52db48-5253-45f6-9933-aa77a42d9f6c')
    def test_live_env_drift(self, results: List[Drift]):
        self.assertEqual(len(results), 13)
        for result in results:
            self.assertTrue(result.resource_type in ('ECS task definition', 'KMS alias', 'KMS key', 'KMS key resource policy'))

    @drift_test(module_path="from_prod", from_live_env=True, live_customer_id='245470b8-398f-4606-a413-e4b2f5f9c6ae')
    def test_live_env_prod(self, results: List[Drift]):
        self.assertEqual(len(results), 13)
