import unittest
from app.db.models import computeinstance


class TestDbModelsComputeInstance(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(computeinstance)
