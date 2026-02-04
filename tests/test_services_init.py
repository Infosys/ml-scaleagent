import unittest
from app.services import __init__


class TestServicesInit(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(__init__)
