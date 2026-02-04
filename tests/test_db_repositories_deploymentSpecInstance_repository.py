import unittest
from app.db.repositories import deploymentSpecInstance_repository


class TestDbRepositoriesDeploymentSpecInstanceRepository(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(deploymentSpecInstance_repository)
