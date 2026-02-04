import unittest
from app.db.repositories import __init__


class TestDbRepositoriesInit(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(__init__)
