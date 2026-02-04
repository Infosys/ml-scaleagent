import unittest
from app.db.models import item


class TestDbModelsItem(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(item)
