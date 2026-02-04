import unittest
from app.db.repositories import item_repository


class TestDbRepositoriesItemRepository(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(item_repository)
