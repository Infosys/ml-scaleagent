import unittest
from app.schemas import __init__


class TestSchemasInit(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(__init__)
