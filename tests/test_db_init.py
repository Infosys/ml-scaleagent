import unittest
from app.db import __init__


class TestDbInit(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(__init__)
