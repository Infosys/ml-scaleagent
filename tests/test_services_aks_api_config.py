import unittest
from app.services import aks_api_config


class TestServicesAksApiConfig(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(aks_api_config)
