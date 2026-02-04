import unittest
from app.schemas import storageInstance


class TestSchemasStorageInstance(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(storageInstance)
