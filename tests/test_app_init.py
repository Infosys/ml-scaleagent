import unittest
from app import __init__


class TestAppInit(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(__init__)
