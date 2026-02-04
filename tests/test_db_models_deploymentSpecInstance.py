import unittest
from app.db.models import deploymentSpecInstance


class TestDbModelsDeploymentSpecInstance(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(deploymentSpecInstance)
