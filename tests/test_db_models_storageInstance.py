import unittest
from app.db.models import storageInstance


class TestDbModelsStorageInstance(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(storageInstance)
