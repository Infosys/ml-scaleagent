import unittest
from app.db.models import eventSourceDefnInstance


class TestDbModelsEventSourceDefnInstance(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(eventSourceDefnInstance)
