import unittest
import importlib


class TestServicesListDeployments(unittest.TestCase):
    def test_import(self):
        # list_deployments is a file, not a module, so import as a module
        module = importlib.import_module('app.services.list_deployments')
        self.assertIsNotNone(module)
