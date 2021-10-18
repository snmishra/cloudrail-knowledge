from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import BaseAwsDriftTest, drift_test


class TestEc2Drifts(BaseAwsDriftTest):

    def get_component(self):
        return 'ec2'

    @drift_test(module_path="ec2_instance/changing_default_sg")
    def test_tracing_drift(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
