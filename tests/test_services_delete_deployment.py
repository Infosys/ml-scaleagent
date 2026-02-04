import unittest
from app.services import delete_deployment


class TestServicesDeleteDeployment(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(delete_deployment)
