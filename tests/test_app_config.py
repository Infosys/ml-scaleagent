import unittest
from app import config


class TestAppConfig(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(config)
