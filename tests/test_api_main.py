import unittest
from app.api import main


class TestMain(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(main)
