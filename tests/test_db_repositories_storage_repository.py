import unittest
from app.db.repositories import storage_repository


class TestDbRepositoriesStorageRepository(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(storage_repository)
