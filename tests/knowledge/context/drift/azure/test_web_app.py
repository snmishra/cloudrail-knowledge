from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from tests.knowledge.context.drift.base_drift_test import drift_test, BaseAzureDriftTest


class TestWebApp(BaseAzureDriftTest):

    def get_component(self):
        return 'web_app'

    @drift_test(module_path="ftps_state")
    def test_ftps_state(self, results: List[Drift]):
        self.assertEqual(len(results), 1)
        web_app = next(res for res in results if res.resource_id == 'azurerm_app_service.webapp')
        self.assertEqual(web_app.resource_iac['app_service_config']['ftps_state'], 'FtpsOnly')
        self.assertEqual(web_app.resource_live['app_service_config']['ftps_state'], 'AllAllowed')
