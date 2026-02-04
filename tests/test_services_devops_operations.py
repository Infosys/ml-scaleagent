import unittest
from app.services.devops import devops_operations


class TestServicesDevopsOperations(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(devops_operations)
