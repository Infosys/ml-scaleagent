import unittest
from app.schemas import eventSourceDefnInstance


class TestSchemasEventSourceDefnInstance(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(eventSourceDefnInstance)
