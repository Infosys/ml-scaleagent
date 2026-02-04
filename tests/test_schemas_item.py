import unittest
from app.schemas import item


class TestSchemasItem(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(item)
