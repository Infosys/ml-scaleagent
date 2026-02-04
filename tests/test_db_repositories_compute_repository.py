import unittest
from app.db.repositories import compute_repository


class TestDbRepositoriesComputeRepository(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(compute_repository)
