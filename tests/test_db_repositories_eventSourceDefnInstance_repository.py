import unittest
from app.db.repositories import eventSourceDefnInstance_repository


class TestDbRepositoriesEventSourceDefnInstanceRepository(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(eventSourceDefnInstance_repository)
