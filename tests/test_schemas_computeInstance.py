import unittest
from app.schemas import computeInstance


class TestSchemasComputeInstance(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(computeInstance)
