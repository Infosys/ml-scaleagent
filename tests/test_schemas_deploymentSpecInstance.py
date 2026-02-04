import unittest
from app.schemas import deploymentSpecInstance


class TestSchemasDeploymentSpecInstance(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(deploymentSpecInstance)
